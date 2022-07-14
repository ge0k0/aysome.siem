import yaml
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

from backend.models import *
from django.db.models import Exists

# Data import is created to simplify import and migration of Use Case Rules, Groups, Enrichments and Correlations.
# The User can import only relevant cases in to the system and use templates to create his own searches.
class Data_Import:
    def open_file(self, filename=None):
        if filename in self.available_config_files:
            full_filename = os.path.join(current_dir, filename)
            with open(full_filename, 'r') as file:
                config_file_content = yaml.safe_load(file)
        return config_file_content

    def __import_group_into_db(self, filename=None):
        if filename in self.available_groups:
            config_file_content = self.open_file(filename)
            created_or_updated_group, created_group_boolean = Group.objects.update_or_create(**config_file_content)
        else:
            pass

        return created_or_updated_group, created_group_boolean

    def __import_ucr_into_db(self, filename=None):
        if filename in self.available_ucrs:
            config_file_content = self.open_file(filename)
            
            # Check if the group dependency is satisfied:
            # Check if there are more then one group listed

            groups = Group.objects.filter(Exists(Group.objects.filter(title=config_file_content["group"])))
            groups_count = groups.count()
            if groups_count == 0:
                created_group = self.__import_group_into_db(filename=self.available_groups_title_filename_dict[config_file_content["group"]])
                config_file_content["group"] = created_group
            elif groups_count == 1:
                config_file_content["group"] = groups[0]
            else:
                pass 

            created_or_updated_ucr, created_ucr_boolean = UCR.objects.update_or_create(**config_file_content)
        else:
            pass

        return created_or_updated_ucr, created_ucr_boolean

    def __import_enrichment_into_db(self, filename=None):
        if filename in self.available_enrichments:
            config_file_content = self.open_file(filename)
            created_or_updated_enrichment, created_enrichment_boolean = Enrichment.objects.update_or_create(**config_file_content)
        else:
            pass

        return created_or_updated_enrichment, created_enrichment_boolean
        
    def __import_correlation_into_db(self, filename=None):
        if filename in self.available_correlations:
            config_file_content = self.open_file(filename)
            created_or_updated_correlation, created_correlation_boolean = Correlation.objects.update_or_create(**config_file_content)
        else:
            pass

        return created_or_updated_correlation, created_correlation_boolean

    # Function imports .yml files from the same directory into Django DB
    def import_file(self, filename=None):
        if filename in self.available_groups:
            self.__import_group_into_db(filename)

        if filename in self.available_ucrs:
            self.__import_ucr_into_db(filename)

        if filename in self.available_enrichments:
            self.__import_enrichment_into_db(filename)
    
        if filename in self.available_correlations:
            self.__import_correlation_into_db(filename)

    
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

    def __init__(self):
        self.available_config_files = os.listdir(current_dir)

        self.available_ucrs = []
        self.available_groups = []
        self.available_enrichments = []
        self.available_correlations = []
        self.available_ucrs_title_filename_dict = {}
        self.available_groups_title_filename_dict = {}
        self.available_enrichments_title_filename_dict = {}
        self.available_correlations_title_filename_dict = {}

        for config_file in self.available_config_files:
            if config_file.startswith("UCR_"):
                config_file_title = self.open_file(config_file)["title"]
                self.available_ucrs.append(config_file)
                self.available_ucrs_title_filename_dict[config_file_title] = config_file

            elif config_file.startswith("GROUP_"):
                config_file_title = self.open_file(config_file)["title"]
                self.available_groups.append(config_file)
                self.available_groups_title_filename_dict[config_file_title] = config_file

            elif config_file.startswith("ENRICHMENT_"):
                config_file_title = self.open_file(config_file)["title"]
                self.available_enrichments.append(config_file)
                self.available_enrichments_title_filename_dict[config_file_title] = config_file

            elif config_file.startswith("CORRELATION_"):
                config_file_title = self.open_file(config_file)["title"]
                self.available_correlations.append(config_file)
                self.available_correlations_title_filename_dict[config_file_title] = config_file