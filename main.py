from dotenv import load_dotenv
import json
import ldclient
from ldclient.config import Config
import os
import time
from utils.create_context import *
from utils.apiHandler import checkRateLimit as api_call

'''
Get environment variables
'''
load_dotenv()

SDK_LIST = json.loads(os.environ.get('SDK_LIST'))
API_KEY = os.environ.get('API_KEY')
PROJECT_KEY = os.environ.get('PROJECT_KEY')

'''
Define API call to get list of flags
'''
flag_list_url = f'/flags/{PROJECT_KEY}'

def get_flag_list():
    response = api_call("GET", flag_list_url, API_KEY, {}).json()
    response_list = response['items']
    number_of_flags = len(response_list)
    flag_list = []

    for i in range(number_of_flags):
        flag_list.append(response['items'][i]['key'])
    
    return flag_list

'''
Evaluate all flags in an environment
'''
def evaluate_all_flags(flag_list, context):
    for flag in flag_list:
        flag_value = ldclient.get().variation(flag, context, False)

'''
Main loop to evaluate flags across multiple environments
'''
def evaluate_flags(environments):
    flags = get_flag_list()
    context = create_multi_context()
    for env in environments:
        print(f'Evaluating environment: sdk-****-{env[-4:]}')
        ldclient.set_config(Config(env))
        evaluate_all_flags(flags, context)
        time.sleep(1)
        ldclient.get().flush()
        time.sleep(1)
        ldclient.get().close()
        time.sleep(1)

        
if __name__ == '__main__':
    while True:
        evaluate_flags(SDK_LIST)