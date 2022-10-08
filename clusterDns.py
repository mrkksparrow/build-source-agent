import os
import requests
TOKEN=''
HEADERS=''

API_ENDPOINT='https://kubernetes/api/v1/configmaps?fieldSelector=metadata.name=kube-proxy'

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
    s=data.get("items")[0].get("data").get("kubeconfig").split("\n")
    for i in s:
        if "server:" in i:
            print(i.strip().split(': ')[1])



get_config()
