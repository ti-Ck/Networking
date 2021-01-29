import csv
import json
import sys
import requests
import os

server = "https://192.168.45.45"
username = "api"
password = "ciscoAPI"

headers = {'Content-Type': 'application/json'}
api_auth_path = "/api/fmc_platform/v1/auth/generatetoken"
auth_url = server + api_auth_path
r = None

def yes_or_no(question):
    answer = raw_input(question + "(y/n): ").lower().strip()
    print("")
    while not(answer == "y" or answer == "yes" or \
    answer == "n" or answer == "no"):
        print("Input yes or no")
        answer = raw_input(question + "(y/n):").lower().strip()
        print("")
    if answer[0] == "y":
        return True
    else:
        return False
        
csvfile = open(sys.argv[1])
objects = csv.DictReader(csvfile)
print('\nThis script will attempt to create objects via an API call')
if yes_or_no('\nDo you want to continue?'):
    ()
else:
    quit()
    
try:
    print('\n\nAttempting connection to FMC...')
    requests.packages.urllib3.disable_warnings()
    r = requests.post(auth_url, headers=headers,
    auth=requests.auth.HTTPBasicAuth(username,password), verify=False)
    auth_headers = r.headers
    auth_token = auth_headers.get('X-auth-access-token', default=None)
    if auth_token == None:
        print("auth_token not found. Exiting...")
        sys.exit()
except Exception as err:
    print ("Error in generating auth token --> "+str(err))
    sys.exit()
    
headers['X-auth-access-token'] = auth_token
print('...Connected! Auth token collected successfully (' + auth_token + (')\n'))
api_path = "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/object/hosts"
url = server + api_path

if (url[-1] == '/'):
    url = url[:-1]
    
for object in objects:
    post_data = {
        "name": object["name"],
        "type": object["type"],
        "value": object["value"],
        "description": object["description"],
    }
    
    print('\n*************************************')
    print('Creating object: ' + object["name"])
    try:
        r = requests.post(url, data=json.dumps(post_data), headers=headers, verify=False)
        status_code = r.status_code
        resp = r.text
        log = open('post_objects.log', 'a')
        print(" Status code: "+str(status_code))
        json_resp = json.loads(resp)
        log.write('\n---------------------------------------------------------------------\n')
        log.write(json.dumps(json_resp,sort_keys=True,indent=4, separators=(',', ': ')))
        
        if status_code == 201 or status_code == 202:
            print (" SUCCESS ")
        elif status_code == 400:
            print (" Message: ")  + resp + ('\n')
        else:
            r.raise_for_status()
            print (" Message: ")  + resp + ('\n')
            
    except requests.exceptions.HTTPError as err:
        print ("Error in connection --> "+str(err))
        
    finally:
        if r: r.close()
        
print('\nLog file "post_objects.log" appended\n')
