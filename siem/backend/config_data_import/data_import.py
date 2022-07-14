import yaml
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

from backend.models import *
from django.db.models import Exists

# Data import is created to simplify import and migration of Use Case Rules, Groups, Enrichments and Correlations.
# The User can import only relevant cases in to the system and use templates to create his own searches.
class Data_Import:
    def __init__(self):
        self.available_config_files = os.listdir(current_dir)

        self.available_ucrs = []
        self.available_groups = []
        self.available_enrichments = []
        self.available_correlations = []

        for config_file in self.available_config_files:
            if config_file.startswith("UCR_"):
                self.available_ucrs.append(config_file)
            elif config_file.startswith("GROUP_"):
                self.available_groups.append(config_file)
            elif config_file.startswith("ENRICHMENT_"):
                self.available_enrichments.append(config_file)
            elif config_file.startswith("CORRELATION_"):
                self.available_correlations.append(config_file)


    def __import_group_into_db(self):
        if self.filename in self.available_groups:
            Group.objects.update_or_create(**self.yaml_object)
        else:
            pass

    def __import_ucr_into_db(self):
        # Check if the Group exists, since Group dependency is mandatory
        if Group.objects.filter(Exists(Group.objects.get(title=self.yaml_object["group"]))):
            self.groupObj = Group.objects.get(title=self.yaml_object["group"])
        else:
            self.__import_group_into_db(self.filename)
            self.groupObj = Group.objects.get(title=self.yaml_object["group"])
        
        # Use update_or_create() method, since Object might already exist
        if hasattr(self, 'groupObj'):
            self.yaml_object["group"] = self.groupObj
            UCR.objects.update_or_create(**self.yaml_object)
        else:
            pass

    def __import_enrichment_into_db(self):
        Enrichment.objects.update_or_create(**self.yaml_object)
        
    def __import_correlation_into_db(self):
        Correlation.objects.update_or_create(**self.yaml_object)
   
    # Function imports .yml files from the same directory into Django DB
    def import_file(self, filename=None):
        self.filename = filename
        if self.filename in self.available_config_files:
            full_filename = os.path.join(current_dir, self.filename)
            with open(full_filename, 'r') as file:
                self.yaml_object = yaml.safe_load(file)

            if self.filename in self.available_groups:
                self.__import_group_into_db()

            if self.filename in self.available_ucrs:
                self.__import_ucr_into_db()

            if self.filename in self.available_enrichments:
                self.__import_enrichment_into_db()
        
            if self.filename in self.available_correlations:
                self.__import_correlation_into_db()

            return self.yaml_object
        else:
            pass
    
    # Function imports multiple .yml files from the same directory into Django DB. 
    # Variable self.filename_contains specifies a part of the title of the file, which should be imported. 
    def import_multiple_files(self, filename_contains = "*"):
        imported_config_files = []
        for config_file in self.available_config_files:
            if config_file.__contains__(self.filename_contains):
                imported_config_files.append(config_file)
                self.import_file(filename=config_file)
        return imported_config_files
    
    # To skip corrupt config files, validation process should be used 
    def validate_file(self):
        pass
    
    # To skip config files with corrupt dependencies, validation process should be used
    def validate_dependencies(self):
        pass



if __name__ == "__main__":
    ucr_import = Data_Import()
    data = ucr_import.import_file(filename="UCR_AV_Symantec_01_Single_Alert.yml")
    print(data)
    mdata = ucr_import.import_multiple_files(filename_contains="_AV_")
    print(mdata)