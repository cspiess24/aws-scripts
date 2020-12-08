# TODO: Update your var naming
import boto3
import yaml
from pprint import pprint

def read_yaml ():
    with open(r'test.yaml') as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        my_list = yaml.load(file, Loader=yaml.FullLoader)
        pprint(my_list)
        # for item in my_list:
            # print(item)
            # print(my_list[item]['Regions'])
        return my_list

session = boto3.session.Session(profile_name='my_account')
cf_client = session.client('cloudformation')

def check_region():
    pass


def get_stack_instance(stack_instance):
    response = cf_client.list_stack_instances(
        StackSetName = stack_instance
    )
    # pprint(response)
    return response

def is_account_in_stackset(accounts, stackset):
    print("Accounts: {}".format(accounts))
    for account in stackset['Summaries']:
        print("Account: {}".format(account['Account']))
        if account['Account'] in accounts:
            print("Stackset: {} - Account: {}".format(account['Account'], accounts))


stack_sets = read_yaml()

for stack in stack_sets:
    stack_set = get_stack_instance(stack)
    pprint(stack_set)
    is_account_in_stackset(stack_sets[stack], stack_set)
