import os
import requests
TOKEN=''
HEADERS=''

API_ENDPOINT='http://localhost:8080/api/v1/configmaps?fieldSelector=metadata.name=kube-proxy'

def get_token():
        try:
            global TOKEN, HEADERS
            if(os.path.isfile('/var/run/secrets/kubernetes.io/serviceaccount/token')):
                token=open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r')
                tokenRead=token.read()
                TOKEN=tokenRead.rstrip()
                HEADERS={
                    'Authorization': 'Bearer '+TOKEN
                }
                token.close()
        except Exception as e:
            print(e)

def get_config():
    get_token()
    json=requests.get(API_ENDPOINT, headers=HEADERS, verify=False)
    data=json.json()
    print(data)


get_config()