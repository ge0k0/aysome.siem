if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.getcwd())

from backend.api.api_methods import API_Methods
from backend.api.api_settings import *
import splunklib.client as client
import splunklib.results as results
import json

class API(API_Methods):
    def __init__(self):
        super().__init__()

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
    
    def search(self, search_query, options_dict = {"output_mode": 'json'}):
        if search_query.startswith("search") == False:
            search_query = "search " + search_query

        self.search_results = self.service.jobs.oneshot(search_query, **options_dict)
        return self.search_results

    def results(self, print_results=False):
        print(self.search_results.empty)
        if self.search_results.empty:
            self.results_number_of_results = 0
            self.results_dict_list = []
        else:
            byteObj = self.search_results.readall()
            utf_string = byteObj.decode('utf-8')
            self.results_raw = json.loads(utf_string)
            self.results_dict_list = self.results_raw['results']
            
            self.results_fields_list = []
            for field in self.results_raw['fields']:
                self.results_fields_list.append(field['name'])

            self.results_preview = self.results_raw['preview']
            self.results_messages = self.results_raw['messages']
            self.results_number_of_results = len(self.results_raw['results'])
            
            if print_results == True:
                for item in self.results_dict_list:
                    print(item)
        return self.results_dict_list

    def write_results(self, index=SPLUNK_RESULTS_INDEX, sourcetype=SPLUNK_RESULTS_SOURCETYPE, source="API", host="local", Event=""):
        if Event == "":
            pass
        else:
            Event = bytes(Event, 'utf-8')
            connection_index = self.service.indexes[index]
            connection_index.submit(Event, sourcetype=sourcetype, host=host, source=source)

if __name__ == "__main__":
    service=API()
    service.login()
    service.search("index=* qid=n38H08hb0160556")
    service.results(print_results=True)
    service.write_results(Event="GK Event Testing RAWs")