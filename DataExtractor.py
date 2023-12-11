import urllib
import json
import base64
import requests
import sys
import os
from requests.auth import HTTPBasicAuth
from InformationCommands import *
from urllib3.exceptions import InsecureRequestWarning
 
# Suppress the warnings from urllib3
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


#Tarras Weir - December, 2023
#The InformationCommands file is a custom module. 
#It is to be stored in the same directory/folder as this file.

#Define a debug string for the user to read.
debug_string = ("The script must be called in the following format!\n\nscript_name server port username " + \
        "password api_key\n\nserver - The ip of the server.\nport - The port number.\nusername - The authenticated username given to you.\n" + \
            "password - The authenticated password given to you.\napi_key - the Api key you have been given in a separate file.")

#Send debug information.
if len(sys.argv) != 6 or not sys.argv[2].isnumeric():
    print(debug_string)
    sys.exit()

#Define the variables from the input on command line for the Gallagher endpoint.
server = sys.argv[1]
port = sys.argv[2]
username = sys.argv[3]
password = sys.argv[4]
api_key = sys.argv[5]
api_url = f"https://{server}:{port}/api"

#Interestingly enough, this is never required to be used? Send an email regarding this.
#Encode the credentials in base64
credentials = f"{username}:{password}"
encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

#Create request headers with above information.
headers = {
    'username': username,
    'password': password,
    'Authorization': f'GGL-API-KEY {api_key}'
}

#Get an alarm response using the provided credentials. You can use response length for debugging.
alarm_response, alarms = get_alarms(api_url, headers)

#Check if the request was successful (status code 200)
if alarm_response.status_code == 200:
    try:
        #Try to parse the JSON response.
        data = alarm_response.json()
        print("\nResponse successful\n")
        json_file_path = "DataExtractorOutput.json"
        
        # Now make a separate request to the alarms href to get the actual alarms data.
        for alarm_link in alarms:
            alarms_data_response = requests.get(alarm_link, headers=headers, verify=False)
            alarms_data = alarms_data_response.json()
        
            # Write the entire response JSON to the file
            with open(json_file_path, 'a') as json_file:
                json.dump(alarms_data, json_file)
                print(f"JSON data written to {json_file_path}")
                
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
else:
    # Print the error status code and content.
    print(f"Error: {alarm_response.status_code}")
    print(alarm_response.text)