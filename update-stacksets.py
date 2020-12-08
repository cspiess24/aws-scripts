import boto3
import json
import yaml
from pprint import pprint

session = boto3.session.Session(profile_name='my_account')
cf_client = session.client('cloudformation')
region = 'us-east-1'

def read_yaml ():
    with open(r'test2.yaml') as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        my_list = yaml.load(file, Loader=yaml.FullLoader)
        pprint(my_list)
        return my_list

def update_stacksets(stacksets, account):
    stackset_updates = []
    for stackset in stacksets:
        response = cf_client.create_stack_instances(
            StackSetName=stackset,
            Accounts=[account],
            Regions=[region]
        )
        print(response)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            stackset_updates.append(
                {
                    'operationId': response['OperationId'],
                    'account': account,
                    'status': '',
                    'stackset': stackset
                }
            )
        else:
            print("There may have been an issue adding account {} to stackset {}".format(account, stackset))
    return stackset_updates

def add_account_to_stackset(stack_info):
    all_stackset_updates = {}
    for account in stack_info['Accounts']:
        stack_updates = update_stacksets(stack_info['Stacksets'], account)
        all_stackset_updates[account] = stack_updates
    pprint(all_stackset_updates)
    return all_stackset_updates

def _check_status(account):
    print('_check_status')
    for stackset in account:
        if stackset['status'] != 'SUCCEEDED' or stackset['status'] != 'FAILED' or stackset['status'] != 'STOPPED':
            response = cf_client.describe_stack_set_operation(
                    StackSetName = stackset['stackset'],
                    OperationId = stackset['operationId']
                )
            print(response)
            stackset['status'] = response['StackSetOperation']['Status']
    print(account)
    return account

def check_status(all_stackset_updates):
    accounts_pending = True
    while accounts_pending:
        for account in all_stackset_updates:
            account = _check_status(all_stackset_updates[account])
        
        accounts_pending = False


stack_info = read_yaml()
all_stackset_updates = add_account_to_stackset(stack_info)
print(all_stackset_updates)
check_status(all_stackset_updates)
