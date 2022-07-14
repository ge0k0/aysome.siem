from backend.models import *
from backend.api.api_settings import PRIMARY_API
import importlib

# PRIMARY_API is the key in api_settings.py file.
# This function imnport standartized API connector for the whole application
# Currently only Splunk and ElasticSearch are supported
api_string = "backend.api." + PRIMARY_API
PRIMARY_API = importlib.import_module(api_string)

# Initial event search class
class Event_Search:
    def __init__(self, title, PRIMARY_API=PRIMARY_API):
        self.title = title
        self.api = PRIMARY_API.API()
    
    # Function creates a search string from the number of configs in the database
    def search_string_creation(self):
        ucr = UCR.objects.get(title=self.title)
        self.search_query = ucr.search_query
        return self.search_query

    # Function handles initial request to the search engine. 
    # Function depends on the self.search_query variable.
    # Search results as a list of dictionaries is returned as a result 
    def search_initial_to_api(self):
        service=self.api
        service.login()
        service.search(self.search_query)
        service.results(print_results=True)
        return self.results_dict_list

    # Function use to enrich data based on the available fields and dependensies to Groups and UCRs
    def search_enrichments_to_api(self):
        pass
    
    # Function use to correlate data with other queries based on the available fields and dependensies to Groups and UCRs
    def search_correlations_to_api(self):
        pass
    
    # Function to return the alerts to the search engine API
    def search_alert_to_api(self):
        pass

    # Function to save alerts in in Django DB 
    def search_alert_to_db(self):
        pass