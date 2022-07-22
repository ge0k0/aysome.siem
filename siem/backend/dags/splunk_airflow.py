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
from datetime import datetime, timezone, timedelta

from airflow.decorators import dag, task, task_group
from airflow.operators.python import PythonOperator

import importlib

# PRIMARY_API is the key in api_settings.py file.
# This function imnport standartized API connector for the whole application
# Currently only Splunk and ElasticSearch are supported
api_string = "backend.api." + PRIMARY_API
PRIMARY_API = importlib.import_module(api_string)

def ucrs_for_current_run():
    # Update cron_netx_run for the next run
    local_date = datetime.now(timezone.utc)
    ucrs = UCR.objects.all()
#    ucrs = UCR.objects.filter(cron_next_run__lt = local_date)
#    for ucr in ucrs:
#        cron_new_value = croniter(ucr.cron, local_date).get_next(datetime)
#        ucr.cron_next_run = cron_new_value
#        ucr.save()

    # Create a search query
    search_queries = {}
    for ucr in ucrs:
        group_search_prefix = ucr.group.search_query_prefix
        # str to list. [1:-1] is used to remove leading and final "
        ucr_search_terms = ucr.search_terms[1:-1].split('", "')
        search_query = group_search_prefix
        for term in ucr_search_terms:
            search_query = f'{search_query} TERM({term}) '
    
        search_queries[ucr.title] = search_query
    
    return search_queries        


def search_data(search_query, title):
    '''
    Function to search for notables. Results are returned to the API into the results index.
    '''
    service = PRIMARY_API.API()
    service.login()
    service.create_search_job(search_query=search_query)

    while service.check_if_job_ready() == False:
        sleep(1)

    service.results()
    service.add_id_to_results(alarm_name=title)
    service.dict_to_event()
    service.write_results()
    return service.ids


@dag(
    schedule_interval="0 0 * * *",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=timedelta(minutes=60),
)
def UCR_Notables_Run():

    @task(task_id="Django_Requests")
    def call_for_current_ucrs():
        search_queries = ucrs_for_current_run()
        return search_queries

    @task(task_id="Search_Notables")
    def search_for_notables(search_queries):
        title, query = search_queries
        ids = search_data(query, title)
        return ids

    @task(task_id="Enrich_Notables")
    def enrich_current_notables():
        pass

    @task(task_id="Correlate_Notables")
    def correlate_current_notables():
        pass

    @task(task_id="Create_Alarms_from_Notables")
    def create_alarms_from_notables():
        pass

    search_for_notables.expand(search_queries=call_for_current_ucrs()) >> enrich_current_notables() >> correlate_current_notables() >> create_alarms_from_notables() 

dag = UCR_Notables_Run()