from backend.models import *
from backend.api.api_settings import PRIMARY_API
import importlib

api_string = "backend.api." + PRIMARY_API
PRIMARY_API = importlib.import_module(api_string)

# Initial event search class
class Event_Search:
    def __init__(self, title, PRIMARY_API=PRIMARY_API):
        self.title = title
        self.api = PRIMARY_API.API()
    
    def search_string_creation(self):
        ucr = UCR.objects.get(title=self.title)
        self.search_query = ucr.search_query
        return self.search_query

    def search_initial_to_api(self):
        service=self.api
        service.login()
        service.search(self.search_query)
        service.results(print_results=True)
        return self.results_dict_list

    def search_enrichments_to_api(self):
        pass

    def search_correlations_to_api(self):
        pass

    def search_alert_to_api(self):
        pass

    def search_alert_to_db(self):
        pass