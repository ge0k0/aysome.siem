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
from backend.models import *
import pendulum
from time import sleep
from datetime import  timedelta

from siem.settings import INSTALLED_APPS

if 'testing' in INSTALLED_APPS:
    @dag(
        schedule_interval="*/1 * * * *",
        start_date=pendulum.datetime(2022, 1, 1, tz=TIMEZONE),
        catchup=False,
        dagrun_timeout=timedelta(minutes=60),
    )
    def UCR_TESTING_WORKFLOW():

        @task(task_id="Django_Requests")
        def create_notables_for_ucrs():
            testing_ucrs = '...'
            return testing_ucrs

        create_notables_for_ucrs()

    dag = UCR_TESTING_WORKFLOW()