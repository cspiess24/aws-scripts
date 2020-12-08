import boto3
import time

def add_account_to_stackset(stackset, account, cf_client, region):
    response = cf_client.create_stack_instances(
        StackSetName=stackset,
        Accounts=[account],
        Regions=[region]
    )
    print(response)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return response['OperationId']
    else:
        print("There may have been an issue adding account {} to stackset {}".format(account, stackset))

def check_status(operation_id, stackset, cf_client):
    i = 0
    while i < 30:
        i += 1
        response = cf_client.describe_stack_set_operation(
                    StackSetName = stackset,
                    OperationId = operation_id
            )
        status = response['StackSetOperation']['Status']
        
        if status == 'SUCCEEDED' or status == 'FAILED' or status == 'STOPPED':
            print(f'Stackset update {status} for stackset {stackset} via Operation Id: {operation_id}')
            break
        if i < 30:
            print(f'Stackset {stackset} current Status is: {status} for Operation Id: {operation_id}')
            time.sleep(10)
        if i == 30:
            print(f'Looks like there was an issue updating stackset: {stackset}')

def update_stacksets(stacksets, account, cf_client, region):
    for stackset in stacksets:
        OperationId = add_account_to_stackset(stackset, account, cf_client, region)
        check_status(OperationId, stackset, cf_client)


if __name__ == '__main__':
    session = boto3.session.Session(profile_name='my_account')
    cf_client = session.client('cloudformation')
    region = 'us-east-1'
    account = '037898436774'
    stacksets = ['test']
    update_stacksets(stacksets, account, cf_client, region)
