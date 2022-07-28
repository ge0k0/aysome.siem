from abc import ABC, abstractmethod

# Ultimate class for every Database API connection (Splunk, ELK, etc.)
# Every method must be overwritten with the specific methods of each API
# It is used to standartize API call funktions across different APIs
# Every new API have to use API_Methods class mandatory
class API_Methods(ABC):
    
    def __init__(self):
        pass

    @abstractmethod
    def login_to_api(self):
        pass

    @abstractmethod
    def create_search_job(self, string):
        pass

    @abstractmethod
    def copy_results_from_api(self):
        pass

    @abstractmethod
    def paste_results_to_api(self):
        pass

    def add_fields_to_results(self):
        pass