
import os
import sys
sys.path.append(os.getcwd())
sys.path.append("/home/geko/Working/siem-clean/aysome.siem/siem")

from backend.api.api_settings import *
from backend.api.splunk import sp_login, sp_create_search_job, sp_check_if_job_ready, sp_results, sp_write_results, sp_add_id_to_results, sp_dict_to_event
import datetime
import pendulum
from time import sleep

from airflow.decorators import dag, task
from airflow.operators.python import PythonOperator

def search_data(search_Q):
    service = sp_login()
    service.search_job = sp_create_search_job(service, search_query=search_Q)

    while sp_check_if_job_ready(service) == False:
        sleep(1)
    service.results = sp_results(service)
    service.results = sp_add_id_to_results(service.results)
    service.string_results = sp_dict_to_event(service.results)
    sp_write_results(service, Event=service.string_results)

@dag(
    schedule_interval="0 0 * * *",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
)
def Etl():
    queries = {"first":"index=* qid=n38H08hb016055", "second":"index=* qid=n38H08hb016056"}
    for i, j in queries.items():

        @task(task_id=f'create_employees_table_{i}')
        def callable(q):
            search_data(q)
        
        callable_task = callable(j)


    @task
    def hello_world():
        print("hello world")

    callable_task >> hello_world()

dag = Etl()