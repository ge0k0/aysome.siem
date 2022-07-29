if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.getcwd())

from splunk import *
from datetime import datetime

timestamp = datetime.now()
timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%S')

collect_query = [f'''
message="hello world" some_field=123123 another_field="wie ist das, dudee :) !!"
''']



if __name__ == '__main__':
    service = API()
    service.login_to_api()
    service.paste_results_to_api(index='testing', sourcetype='testing_sourcetype', source="splunk_testing.py", data=collect_query)