# ToDo List:
# - Logs
# - Errors
# - Functions
# - Enrichments
# - Correlations

import yaml
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

import logging
logger = logging.getLogger(__name__)

from backend.models import *
from django.db.models import Exists

from backend.helpers.logs_and_errors import *

# Data import is created to simplify import and migration of Use Case Rules, Groups, Enrichments and Correlations.
# The User can import only relevant cases in to the system and use templates to create his own searches.
class Data_Import:
    def open_file(self, filename=None):
        if filename in self.available_config_files:
            full_filename = os.path.join(current_dir, filename)
            with open(full_filename, 'r') as file:
                config_file_content = yaml.safe_load(file)
            logger.info('File %s is opened and configuration returned', filename)
        else:
            logger.critical('File %s is not available', filename)
        return config_file_content

    def __import_group_into_db(self, filename=None):
        if filename in self.available_groups:
            config_file_content = self.open_file(filename)
            created_or_updated_group, created_group_boolean = Group.objects.update_or_create(**config_file_content)
            if created_group_boolean:
                logger.info('Group %s created', created_or_updated_group)
            else:
                logger.info('Group %s updated', created_or_updated_group)
        else:
            logger.critical('File is not available. Group could not be created.')

        return created_or_updated_group, created_group_boolean
    def __validate_dependency_for_groups(self, filename=None):

            # Check if the group dependency is satisfied:
            # Check if there are more then one group listed
            # Return Groups Object
            
            dependency_satisfied = bool()
            groups_results = None

            config_file_content = self.open_file(filename)
            if type(config_file_content["group"]) is str:
                groups_count_config_file = 1
                groups = Group.objects.filter(Exists(Group.objects.filter(title=config_file_content["group"])))
            elif type(config_file_content["group"]) is list:
                groups_count_config_file = len(config_file_content["group"])
                groups = Group.objects.filter(Exists(Group.objects.filter(title__in=config_file_content["group"])))

            # Create a string, if there is only one item in the list
                if groups_count_config_file == 1:
                    config_file_content["group"] = str(config_file_content["group"][0])
                    groups = Group.objects.filter(Exists(Group.objects.filter(title=config_file_content["group"])))
            else:
                logger.critical('Configuration variable %s is not a string or list.', config_file_content["group"])

            groups_count = groups.count()
            print(groups_count)
            print(groups_count_config_file)

            if groups_count == 0 and groups_count_config_file == 0:
                dependency_satisfied = True
                groups_results = None
                logger.warning('No group dependecies have been returned')
            
            if groups_count == 0 and groups_count_config_file == 1:
                created_group, dependency_satisfied = self.__import_group_into_db(filename=self.available_groups_title_filename_dict[config_file_content["group"]])
                groups_results = created_group
                logger.info('Group dependency has beed satisfied')

            elif groups_count == 1 and groups_count_config_file == 1:
                dependency_satisfied = True
                groups_results = groups[0]
                logger.info('Group dependency has beed satisfied')

            elif groups_count > 1 and groups_count_config_file == groups_count:
                dependency_satisfied = True
                groups_results = groups
                logger.info('Group dependency has beed satisfied')
            
            elif groups_count_config_file > 1:
                for group in config_file_content["group"]:
                    created_group, dependency_satisfied = self.__import_group_into_db(filename=self.available_groups_title_filename_dict[group])
                
                groups = Group.objects.filter(Exists(Group.objects.filter(title__in=config_file_content["group"])))
                groups_count = groups.count()

                if groups_count_config_file == groups_count:
                    dependency_satisfied = True
                    groups_results = groups
                    logger.info('Group dependency has beed satisfied')
                else:
                    dependency_satisfied = False
                    groups_results = groups
                    logger.warning('Group dependencies were not satisfied. Some groups could not be imported.')

            return groups_results, dependency_satisfied


    def __import_ucr_into_db(self, filename=None):
        if filename in self.available_ucrs:
            config_file_content = self.open_file(filename)
            config_file_content["group"], dependency_satisfied = self.__validate_dependency_for_groups(filename)
            created_or_updated_ucr, created_ucr_boolean = UCR.objects.update_or_create(**config_file_content)
            if created_ucr_boolean:
                logger.info('Group %s created', created_or_updated_ucr)
            else:
                logger.info('Group %s updated', created_or_updated_ucr)
        else:
            logger.critical('File is not available. UCR could not be created.')

        return created_or_updated_ucr, created_ucr_boolean

    def __import_enrichment_into_db(self, filename=None):
        if filename in self.available_enrichments:
            config_file_content = self.open_file(filename)

            dependent_groups, dependency_satisfied = self.__validate_dependency_for_groups(filename)
            print(dependent_groups)
            config_groups = config_file_content.pop("group")

            created_or_updated_enrichment, created_enrichment_boolean = Enrichment.objects.update_or_create(**config_file_content)
            if len(dependent_groups) > 1:
                for group_item in dependent_groups:
                    created_or_updated_enrichment.group.add(group_item)
            else:
                created_or_updated_enrichment.group.add(dependent_groups)

            if created_enrichment_boolean:
                logger.info('Enrichment %s created', created_or_updated_enrichment)
            else:
                logger.info('Enrichment %s updated', created_or_updated_enrichment)
        else:
            logger.critical('File is not available. Enrichment could not be created.')

        return created_or_updated_enrichment, created_enrichment_boolean
        
    def __import_correlation_into_db(self, filename=None):
        if filename in self.available_correlations:
            config_file_content = self.open_file(filename)
            created_or_updated_correlation, created_correlation_boolean = Correlation.objects.update_or_create(**config_file_content)
            if created_correlation_boolean:
                logger.info('Correlation %s created', created_or_updated_correlation)
            else:
                logger.info('Correlation %s updated', created_or_updated_correlation)
        else:
            logger.critical('File is not available. Enrichment could not be created.')

        return created_or_updated_correlation, created_correlation_boolean

    # Function imports .yml files from the same directory into Django DB
    def import_file(self, filename=None):
        if filename in self.available_groups:
            self.__import_group_into_db(filename)

        elif filename in self.available_ucrs:
            self.__import_ucr_into_db(filename)

        elif filename in self.available_enrichments:
            self.__import_enrichment_into_db(filename)
    
        elif filename in self.available_correlations:
            self.__import_correlation_into_db(filename)
        else:
            logger.critical('File is not available')

    
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