'''
service, freeswitch gsr.
main process in loop, load work information from database; start worker with work information

google credential is hard coded and set as global variable
'''
import argparse
import datetime
import pprint

import os

from google.cloud import storage
import google.auth


if __name__ == '__main__' :
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ :
        print("no google credential defined, hard coded")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "e:\\xyj\\journal\\_all.blue.solutions\\google.service.account\\james-freeswtich-gsr-f2fafcbb54f6.json"
        print("env GOOGLE_APPLICATION_CREDENTIALS : ", os.environ["GOOGLE_APPLICATION_CREDENTIALS"])

    while True :
        # sql access database, find recording file to process
        # call_cdrs + call_records
