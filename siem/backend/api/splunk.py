if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.getcwd())

from backend.api.api_methods import API_Methods
from backend.api.api_settings import *
import splunklib.client as client
import splunklib.results as results
import json
from random import randrange
from datetime import datetime

# Splunk API use standard class API_Methods config saved in api_methods.py file
# It is used to standartize API call funktions across different APIs
# Every new API have to use API_Methods class mandatory
class API(API_Methods):
    def __init__(self):
        super().__init__()

    # Login to the Splunk API
    def login(self):
        self.service = client.connect(
            host=SPLUNK_API_HOST, 
            port=SPUNK_API_PORT, 
            splunkToken=SPLUNK_API_TOKEN, 
            autologin=SPLUNK_API_AUTOLOGIN, 
            version=SPLUNK_API_VERSION, 
            scheme=SPLUNK_API_SCHEME, 
            app=SPLUNK_API_APP)
        return self.service
    
    # Search the Query
    def search(self, search_query, options_dict = {"output_mode": 'json'}):

        # Every search query has to start with "search" command
        if search_query.startswith("search") == False:
            search_query = "search " + search_query

        self.search_results = self.service.jobs.oneshot(search_query, **options_dict)
        return self.search_results

    # Return resutls
    def results(self, print_results=False):
        byteObj = self.search_results.readall()
        utf_string = byteObj.decode('utf-8')
        self.results_raw = json.loads(utf_string)
        self.results_dict_list = self.results_raw['results']
        self.results_number_of_results = len(self.results_raw['results'])

        # Check if the number of results is 0
        # If so, return ...
        if self.results_number_of_results == 0:
            self.results_number_of_results = 0
            self.results_dict_list = []
        else:            
            self.results_fields_list = []
            for field in self.results_raw['fields']:
                self.results_fields_list.append(field['name'])

            self.results_preview = self.results_raw['preview']
            self.results_messages = self.results_raw['messages']
            
            
            if print_results == True:
                for item in self.results_dict_list:
                    print(item)
        return self.results_dict_list

    # Write results back in Splunk
    def write_results(self, index=SPLUNK_RESULTS_INDEX, sourcetype=SPLUNK_RESULTS_SOURCETYPE, source="API", host="local", Event=""):
        if Event == "":
            pass
        else:
            Event = bytes(Event, 'utf-8')
            connection_index = self.service.indexes[index]
            connection_index.submit(Event, sourcetype=sourcetype, host=host, source=source)


def sp_login():
    '''
    Login to the Splunk API.
    '''
    service = client.connect(
        host=SPLUNK_API_HOST, 
        port=SPUNK_API_PORT, 
        splunkToken=SPLUNK_API_TOKEN, 
        autologin=SPLUNK_API_AUTOLOGIN, 
        version=SPLUNK_API_VERSION, 
        scheme=SPLUNK_API_SCHEME, 
        app=SPLUNK_API_APP)
    return service

def sp_create_search_job(service, search_query, options_dict = {"output_mode": 'json'}):
    '''
    Create a search job. Every search query has to start with "search" command.
    '''
    if search_query.startswith("search") == False:
        search_query = "search " + search_query

    service.search_job = service.jobs.create(search_query, **options_dict)
    return service.search_job

def sp_check_if_job_ready(service):
    '''
    Check if the job is finished.
    '''
    if hasattr(service, "search_job"):
        return service.search_job.is_done()
    else:
        return False

def sp_results(service, print_results=False):
    ''' 
    Check for search results. Return a list of dictionaries with results (key:value) in it.
    '''
    byteObj = service.search_job.results(output_mode='json').readall()
    utf_string = byteObj.decode('utf-8')
    results_raw = json.loads(utf_string)
    results_dict_list = results_raw['results']
    results_number_of_results = len(results_raw['results'])

    # Check if the number of results is 0
    # If so, return ...
    if results_number_of_results == 0:
        results_number_of_results = 0
        results_dict_list = []
    else:            
        results_fields_list = []
        for field in results_raw['fields']:
            results_fields_list.append(field['name'])

        results_preview = results_raw['preview']
        results_messages = results_raw['messages']
        
        
        if print_results == True:
            for item in results_dict_list:
                print(item)
    return results_dict_list

def sp_add_id_to_results(results_list: list):
    for result_item in results_list:
        id = str(randrange(1000000000, 9999999999))
        id = ''.join(("id=", id))
        result_item["id"] = id
    return results_list

def sp_dict_to_event(results_list: list):
    result_event_list = []
    timestamp = datetime.now()
    timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%S.000+00:00')
    for result_item in results_list:
        if "_raw" in result_item:
            result_event_list.append(''.join((result_item["id"], ' _time=', timestamp, ' Event="', result_item["_raw"], '" ')))
            continue
        result_event_list.append(str(result_item)) 
    return result_event_list 


def sp_write_results(service, index=SPLUNK_RESULTS_INDEX, sourcetype=SPLUNK_RESULTS_SOURCETYPE, source="API", host="local", Event=""):
    '''
    Write results to Splunk index.
    '''
    connection_index = service.indexes[index]
    if isinstance(Event, list) and len(Event) > 0:
        for event in Event:
            event = bytes(event, 'utf-8')
            connection_index.submit(event, sourcetype=sourcetype, host=host, source=source)
    elif isinstance(Event, str) and len(Event) > 0:
        Event = bytes(Event, 'utf-8')
        connection_index = service.indexes[index]
        connection_index.submit(Event, sourcetype=sourcetype, host=host, source=source)
    


# Local testing
if __name__ == "__main__":
    service=API()
    service.login()
    service.search("index=* qid=n38H08hb016055")
    service.results(print_results=True)
    service.write_results(Event="GK Event Testing RAWs")