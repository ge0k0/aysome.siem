import yaml

class Data_Import:
    def __init__(self):
        pass

    def import_file(self, filename=None):
        if __name__ == "__main__":
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(current_dir, filename)

        with open(filename, 'r') as file:
            yaml_object = yaml.safe_load(file)
        return yaml_object

if __name__ == "__main__":
    ucr_import = Data_Import()
    data = ucr_import.import_file(filename="UCR_AV_Symantec_01_Single_Alert.yml")
    print(data)