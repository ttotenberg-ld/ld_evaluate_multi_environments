import json
import ldclient
from ldclient.config import Config
from ldclient.versioned_data_kind import FEATURES
import os
import requests
import time
from utils.create_context import *


API_KEY = os.environ["LD_API_KEY"]
PROJECT_KEY = ""
NUMBER_OF_ITERATIONS = 1000


"""
It's just fun :)
"""


def show_banner():
    print()
    print("        ██       ")
    print("          ██     ")
    print("      ████████   ")
    print("         ███████ ")
    print("██ LAUNCHDARKLY █")
    print("         ███████ ")
    print("      ████████   ")
    print("          ██     ")
    print("        ██       ")
    print()


"""
Get SDK key list
"""


def get_keys():
    global PROJECT_KEY
    global API_KEY
    url = f"https://app.launchdarkly.com/api/v2/projects/{PROJECT_KEY}/environments"
    response = requests.request(
        "GET",
        url,
        headers={"Authorization": API_KEY, "Content-Type": "application/json"},
    ).json()
    env_list = response["items"]
    sdk_list = []
    for i in env_list:
        sdk_list.append(i["apiKey"])
    print(f"SDK list: {sdk_list}")
    return sdk_list


"""
Evaluate all flags in an environment
"""


def evaluate_all_flags(context):
    # Method to get all flags from the feature store. Taken from https://github.com/launchdarkly/python-server-sdk/blob/d152455b89cb70164d8487a1cc0b47f92017a5c4/ldclient/client.py#L549
    feature_store = ldclient.__client._store.all(FEATURES, lambda x: x)
    for key in feature_store.keys():
        result = ldclient.get().variation(key, context, False)


"""
Main loop to evaluate flags across multiple environments
"""


def evaluate_flags(environments):
    context = create_multi_context()
    for env in environments:
        print(f"Evaluating environment: sdk-****-{env[-4:]}")
        ldclient.set_config(Config(env))
        if not ldclient.get().is_initialized():
            print(
                "*** SDK failed to initialize. Please check your internet connection and SDK credential for any typo."
            )
            exit()
        evaluate_all_flags(context)
        time.sleep(0.5)
        ldclient.get().flush()
        time.sleep(0.5)
        ldclient.get().close()
        time.sleep(0.5)


def lambda_handler(event, context):
    global PROJECT_KEY
    global NUMBER_OF_ITERATIONS
    global ldclient

    body = json.loads(event["body"])

    PROJECT_KEY = body["project_key"]
    NUMBER_OF_ITERATIONS = body["num_iterations"]

    if NUMBER_OF_ITERATIONS > 5000:
        NUMBER_OF_ITERATIONS = 5000

    show_banner()
    sdk_list = get_keys()
    for i in range(NUMBER_OF_ITERATIONS):
        try:
            evaluate_flags(sdk_list)
        except Exception as e:
            print(f"Error: {e}")
            break

    return {"statusCode": 200, "body": json.dumps({"message": "success"})}
