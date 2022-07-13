import yaml
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

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
        
    def import_file(self, filename=None):
        if filename in self.available_config_files:
            filename = os.path.join(current_dir, filename)
            with open(filename, 'r') as file:
                yaml_object = yaml.safe_load(file)
            return yaml_object
        else:
            pass
    
    def import_multiple_files(self, filename_contains = "*"):
        imported_config_files = []
        for config_file in self.available_config_files:
            if config_file.__contains__(filename_contains):
                imported_config_files.append(config_file)
                self.import_file(filename=config_file)
        return imported_config_files


if __name__ == "__main__":
    ucr_import = Data_Import()
    data = ucr_import.import_file(filename="UCR_AV_Symantec_01_Single_Alert.yml")
    print(data)
    mdata = ucr_import.import_multiple_files(filename_contains="_AV_")
    print(mdata)