from abc import ABC, abstractmethod

# Ultimate class for every Database API connection (Splunk, ELK, etc.)
# Every method must be overwritten with the specific methods of each API
# It is used to standartize API call funktions across different APIs
# Every new API have to use API_Methods class mandatory
class API_Methods(ABC):
    
    def __init__(self):
        pass

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def search(self, string):
        pass

    @abstractmethod
    def results(self):
        pass

    @abstractmethod
    def write_results(self):
        pass