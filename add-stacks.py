import boto3
import yaml
from pprint import pprint

def read_yaml ():
    with open(r'test.yaml') as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        my_list = yaml.load(file, Loader=yaml.FullLoader)
        for item in my_list:
            print(item['AccountId'])
            print(item['Regions'])

        print(my_list)

session = boto3.session.Session(profile_name='my_account')
cf_client = session.client('cloudformation')

response = cf_client.list_stack_instances(
    StackSetName = 'AWSControlTowerBP-BASELINE-ROLES'
)

pprint(response)
read_yaml()
