from backend.models import *

# Initial event search class
class Event_Search:
    def __init__(self, title):
        self.title = title
    
    def search_string_creation(self):
        ucr = UCR.objects.get(title=self.title)
        self.search_query = ucr.search_query
        return self.search_query

    def search_initial_to_api(self):
        pass

    def search_enrichments_to_api(self):
        pass

    def search_correlations_to_api(self):
        pass

    def search_alert_to_api(self):
        pass

    def search_alert_to_db(self):
        pass