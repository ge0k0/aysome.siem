from api_methods import API_Methods
from api_settings import *
import splunklib.client as client
import splunklib.results as results

class Splunk_API(API_Methods):
    def __init__(self):
        super().__init__()
        pass

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
        self.results_json = results.JSONResultsReader(self.search_results)

        if print_results == True:
            for item in self.results_json:
                print(item)
        return self.results_json


if __name__ == "__main__":
    service=Splunk_API()
    service.login()
    service.search("index=* qid=n38H08hb016055")
    service.results(print_results=True)