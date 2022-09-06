import requests
import json

#Global Variables
TOKEN=''
HEADER=''
RESP_DATA=''
RESP_JSON=''
TIME=27

#Endurl and paths
endpoint='https://kubernetes'   #http://localhost:8080
eventV1='/apis/events.k8s.io/v1/events?watch=true'
# endpoint='http://localhost:8080'


def get_token():
    try:
        import os   
        global TOKEN, HEADER
        TOKEN=os.system('cat /var/run/secrets/kubernetes.io/serviceaccount/token')
        HEADER='Authorization: Bearer '+str(TOKEN)
    except Exception as e:
        print(e)



def sendRequest(path):
    try:
        global RESP_DATA
        req=requests.Session()
        fileRead=open("./sample.json", "r")
        jsonRead=json.load(fileRead)
        fileRead.close()
        with req.get(endpoint+path, headers=HEADER,stream=True, verify=False) as res:
            for line in res.iter_lines():
                if(line):
                    lineJSON=json.loads(line)
                    jsonRead["items"].append(lineJSON)
                    jsonWrite=json.dumps(jsonRead, indent=4)
                    fileWrite=open("./sample.json", "w")
                    fileWrite.write(jsonWrite)
                    fileWrite.close()
    except Exception as e:
        print(e)



if __name__=='__main__':
    get_token()
    sendRequest(eventV1)