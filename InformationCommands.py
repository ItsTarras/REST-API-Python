import urllib
import json
import base64
import requests
import certifi
import sys
import os
from requests.auth import HTTPBasicAuth
import time
from urllib3.exceptions import InsecureRequestWarning
 
# Suppress the warnings from urllib3
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def get_alarms(api_url, headers):
    """This gets alarms and the assocated information with them, via a get request"""
    alarms = []
    itemInList = 1
    json_file_path = "DataExtractorOutput.json"
    json_file = open(json_file_path, 'a')
    json_file.truncate(0)
    
    #Add the first url to the list
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        # Try to parse the JSON response
        data = response.json()
        json_link = data.get('features', {}).get('alarms', {}).get('alarms', {}).get('href')
        #print(f"json string: {json_link}")
    else:
        # Print the error status code and content
        print(f"Error: {response.status_code}")

    while True:
        # Check if the request was successful (status code 200)
        try:
            #Try to recursively connect to the json_links. There are 2 layers.
            alarms_data_response = requests.get(json_link, headers=headers, verify=False)
            alarms_data = alarms_data_response.json()
            alarms.append(json_link)
            print("\n", alarms_data)
            
            # Check if there is a link for the next set of alarms
            #print(f"data: {data}")
            next_link = alarms_data.get('next', {}).get('href')
            if next_link:
                print("A new link has been grabbed!!!")
                json_link = next_link
            else:
                break
        
        except requests.exceptions.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            break
        
    print(alarms)
    print("Processing alarms...")
    time.sleep(1)
    return response, alarms