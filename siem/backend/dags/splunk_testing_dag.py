# PATH_DIR is important for a proper DAGs import into Apache Airflow
import sys, os
from dags_settings import * 
sys.path.append(PATH_DIR)
sys.path.append(os.getcwd())

# Django
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siem.settings')
django.setup()

# Airflow
from airflow.decorators import dag, task
import pendulum

from backend.api.api_settings import *
from backend.api.splunk import *
import pendulum
from datetime import  timedelta

from siem.settings import INSTALLED_APPS

if 'testing' in INSTALLED_APPS:
    from testing.models import *

    def insert_of_variables_into_testing_query(testing_query, variables):
        '''
        Testing query can have variables to insert. Depending on the query, the variables can represent special testing cases, customers, etc.
        '''
        return testing_query

    @dag(
        schedule_interval="0 0 * * *",
        start_date=pendulum.datetime(2022, 1, 1, tz=TIMEZONE),
        catchup=False,
        dagrun_timeout=timedelta(minutes=60),
    )
    def UCR_TESTING_WORKFLOW():

        @task(task_id="UCR_Test_Run")
        def create_notables_for_ucrs():
            testing_ucrs = UCR_Testing.objects.all()

            testing = API()
            testing.login_to_api()

            for testing_case in testing_ucrs:
                testing_query = insert_of_variables_into_testing_query(testing_case.testing_query, testing_case.variables)
                testing.paste_results_to_api(index=testing_case.index, sourcetype=testing_case.sourcetype, source=testing_case.title, data=testing_query)

        create_notables_for_ucrs()

    dag = UCR_TESTING_WORKFLOW()