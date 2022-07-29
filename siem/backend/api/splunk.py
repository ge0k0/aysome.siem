if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.getcwd())

from backend.api.api_methods import API_Methods
from backend.api.api_settings import *
import splunklib.client as client
import splunklib.results as results
import json
from secrets import randbelow
from datetime import datetime

# Splunk API use standard class API_Methods config saved in api_methods.py file
# It is used to standartize API call funktions across different APIs
# Every new API have to use API_Methods class mandatory
class API(API_Methods):
    def __init__(self):
        super().__init__()

    def login_to_api(self):
        '''
        Login to the Splunk API.
        '''
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
    def create_search_job(self, search_query, earliest_time = "-1y", latest_time = "now"):
        '''
        Create a search job. Every search query has to start with "search" command.
        '''
        # Every search query has to start with "search" command
        if search_query.startswith("search") == False:
            search_query = "search " + search_query

        self.service.search_job = self.service.jobs.create(search_query, earliest_time=earliest_time, latest_time=latest_time)
        return self.service.search_job


    def check_if_job_ready(self):
        '''
        Check if the job is finished.
        '''
        if hasattr(self.service, "search_job"):
            return self.service.search_job.is_done()
        else:
            return False


    # Return resutls
    def copy_results_from_api(self, print_results=False):
        ''' 
        Check for search results. Return a list of RAW events with results in it.
        '''
        self.results_list = list()

        byteObj = self.service.search_job.results(output_mode='raw').readall()
        utf_string = byteObj.decode('utf-8')
        self.results_list = utf_string.split('\n')
        self.results_number_of_results = len(self.results_list)

        if print_results == True:
            for item in self.results_list:
                print(item)
        return self.results_list


    def add_fields_to_results(self, sourcetype=None, **kwargs):
        '''
        Add additional information to search results. 
        '''
        self.a_ids = list()
        self.keys = set()
        results_list_copy = self.results_list.copy()
        self.results_list = list()

        add_id = False

        if sourcetype == "ucr":
            add_id = True

        for result_item in results_list_copy:
            if len(result_item) > 0:

                # Create an A_ID if there is none.
                if add_id == True:
                    a_id = str(100000000000 - randbelow(99999999999))
                    self.a_ids.append(a_id)
                    kwargs["a_id"] = a_id

                for key, value in kwargs.items():
                    result_item = ''.join((f'{key}={value} ', result_item))
                    self.keys.add(key)

                self.results_list.append(result_item)
        return self.results_list

    def paste_results_to_api(self, index=SPLUNK_RESULTS_INDEX, sourcetype=SPLUNK_RESULTS_SOURCETYPE, source="API", host="local", data=[]):
        '''
        Write results to Splunk index.
        '''

        if len(data) == 0:
            data = self.results_list

        connection_index = self.service.indexes[index]
        if len(data) > 0 and type(data) == list:
            for event in data:
                if len(event) > 0:
                    event = bytes(event, 'utf-8')
                    connection_index.submit(event, sourcetype=sourcetype, host=host, source=source)

def add_escape_character_to_string(string):
    string = string.replace('"', '\\"')
    string = string.replace("'", "\\'")
    return string

# Local testing
if __name__ == "__main__":
    from time import sleep
    service=API()
    service.login_to_api()
#    service.results_dict_list = [{1:1},{"_raw":"Hello Wolrd", 2:2}]
#    service.add_id_to_results(title="hello")
#    print(service.results_dict_list)
#    service.dict_to_event()
#    print(service.result_event_list)
#    print(service.ids)
    service.create_search_job(search_query="index=_audit TERM(ta_1658926534)")

    while service.check_if_job_ready() == False:
        sleep(1)

    service.copy_results_from_api(print_results=True)
    service.add_fields_to_results(a_id="11000111000", hello="world", x=1, OTHER=123123 )
    print(service.results_list)
    service.paste_results_to_api()