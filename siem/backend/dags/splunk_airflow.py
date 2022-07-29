# PATH_DIR is important for a proper DAGs import into Apache Airflow
import sys

from dags_settings import * 
sys.path.append(PATH_DIR)

# Django
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siem.settings')
django.setup()

#Standard Libs
from backend.api.api_settings import *
from backend.models import *
import pendulum
from time import sleep
from croniter import croniter
from datetime import datetime, timedelta
import pytz
import importlib
import itertools
from string import Template

# Airflow
from airflow.decorators import dag, task


# PRIMARY_API is the key in api_settings.py file.
# This function imnport standartized API connector for the whole application
# Currently only Splunk and ElasticSearch are supported
api_string = "backend.api." + PRIMARY_API
PRIMARY_API = importlib.import_module(api_string)

def ucrs_for_current_run():
    # Update cron_netx_run for the next run
    tz = pytz.timezone(TIMEZONE)
    local_date = datetime.now(tz)
#    ucrs = UCR.objects.all()
    ucrs = UCR.objects.filter(cron_next_run__lt = local_date)
    ucr_info = dict()
    for ucr in ucrs:
        earliest_latests_timestamp = dict()
        earliest_latests_timestamp['earliest'] = ucr.cron_previous_run.astimezone().strftime('%Y-%m-%dT%H:%M:%S')
        earliest_latests_timestamp['latest'] = ucr.cron_next_run.astimezone().strftime('%Y-%m-%dT%H:%M:%S')
        cron_new_value = croniter(ucr.cron, local_date).get_next(datetime)
        ucr.cron_previous_run = ucr.cron_next_run
        ucr.cron_next_run = cron_new_value
        ucr.save()
        ucr_info[ucr.title] = earliest_latests_timestamp

    # Create a search query
    for ucr in ucrs:
        group_search_prefix = ucr.group.search_query_prefix
        ucr_search_terms = ucr.search_terms[1:-1].split('", "')
        search_query = group_search_prefix
        for term in ucr_search_terms:
            search_query = f'{search_query} TERM({term})'
            search_query = PRIMARY_API.add_escape_character_to_string(search_query)
    
        ucr_info[ucr.title]['search_query'] = search_query
    return ucr_info

def enrichment_for_current_id(enrichment, a_ids):
    # Primary search
    primary_search = ''.join(("index=", SPLUNK_RESULTS_INDEX, ' sourcetype=ucr', ' a_id IN (', ", ".join(str(id) for id in a_ids), ')'))
    enrichment_required_fields = enrichment.required_fields.split(', ')
    for field in enrichment_required_fields:
        primary_search = ''.join((primary_search, f' {field}=*'))
    # Secondary map search
    search_query = PRIMARY_API.add_escape_character_to_string(enrichment.search_query) 
    search_query = ''.join((primary_search, f' | map maxsearches=10000000000 search=" search {search_query}" | eval a_id=$a_id$'))
    return search_query


def search_data(search_query, earliest_time = "-1y", latest_time = "now", **kwargs):
    '''
    Function to search for notables. Results are returned to the API into the results index.
    '''
    service = PRIMARY_API.API()
    service.login_to_api()
    service.create_search_job(search_query, earliest_time=earliest_time, latest_time=latest_time)

    while service.check_if_job_ready() == False:
        sleep(1)

    if kwargs.get('title') == None:
        source = "API"
    else:
        source = kwargs.pop('title')

    if kwargs.get('sourcetype') == None:
        kwargs['sourcetype'] = "API"
    else:
        sourcetype = kwargs.pop('sourcetype')

    service.copy_results_from_api(print_results=True)
    service.add_fields_to_results(sourcetype=sourcetype, **kwargs)
    service.paste_results_to_api(source=source, sourcetype=sourcetype)
    return service.a_ids


@dag(
    schedule_interval="*/1 * * * *",
    start_date=pendulum.datetime(2022, 1, 1, tz=TIMEZONE),
    catchup=False,
    dagrun_timeout=timedelta(minutes=60),
)
def UCR_CORE_WORKFLOW():

    @task(task_id="Django_Requests")
    def call_for_current_ucrs():
        search_queries = ucrs_for_current_run()
        return search_queries

    @task(task_id="Search_Notables")
    def search_for_notables(ucr_info):
        title, infos = ucr_info
        a_ids = search_data(infos['search_query'], earliest_time=infos['earliest'], latest_time=infos['latest'], title=title, alarm_title=title, alarm_status="Pending", sourcetype="ucr")
        return a_ids

    @task(task_id="Enrich_Notables")
    def enrich_current_notables(**kwargs):
        a_ids = kwargs["ti"].xcom_pull(task_ids=['Search_Notables'])
        # Multiple lists of lists to simple list 
        a_ids = list(itertools.chain(*a_ids))
        # No empty searches needed
        if len(a_ids) > 0:
            enrichments = Enrichment.objects.all()
            for enrichment in enrichments:
                search_query = enrichment_for_current_id(enrichment, a_ids)
                search_data(search_query, title=enrichment.title, sourcetype="enrichment")
        return a_ids

    @task(task_id="Correlate_Notables")
    def correlate_current_notables(**kwargs):
        a_ids = kwargs["ti"].xcom_pull(task_ids=['Enrich_Notables'])
        # Multiple lists of lists to simple list 
        a_ids = list(itertools.chain(*a_ids))
        # No empty searches needed
        if len(a_ids) > 0:
            correlations = Correlation.objects.all()
            for correlation in correlations:
                search_query = enrichment_for_current_id(correlation, a_ids)
                search_data(search_query, title=correlation.title, sourcetype="correlation")
        return a_ids

#    @task(task_id="Create_Alarms_from_Notables")
#    def create_alarms_from_notables():
#        pass

    search_for_notables.expand(ucr_info = call_for_current_ucrs()) >> enrich_current_notables() >> correlate_current_notables() # >> create_alarms_from_notables() 

dag = UCR_CORE_WORKFLOW()