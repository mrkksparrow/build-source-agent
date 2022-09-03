import requests
import json
from datetime import datetime

TOKEN=''
HEADER=''
RESP_DATA=''
RESP_JSON=''
RES_JSON={
    "items":[]
}
TIME=20

endpoint='http://localhost:8080'
eventV1='/apis/events.k8s.io/v1/events'


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
        req=requests.get(endpoint+path)
        RESP_DATA=req.content
    except Exception as e:
        print(e)

def processResp():
    try:
        global RESP_DATA, RESP_JSON
        RESP_JSON=json.loads(RESP_DATA)
        RESP_JSON=RESP_JSON["items"]
        fetchByMin(TIME)
    except Exception as e:
        print(e)

def fetchByMin(min):
    try:
        global RESP_JSON, RES_JSON
        now=str(datetime.utcnow())
        now=datetime.strptime(now, "%Y-%m-%d %H:%M:%S.%f")
        for i in RESP_JSON:
            ts=dtSplit(i["metadata"]["creationTimestamp"])
            ts=datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f")
            print(now-ts)
            timeRes=str(now-ts).split(",")
            if(len(timeRes)==1):
                timeRes=timeRes[0].split(":")
                if((timeRes[0]=='0' or timeRes[0]=='00') and int(timeRes[1])<=min):
                    RES_JSON["items"].append(i)
    except Exception as e:
        print(e)

def dtSplit(dt):
    date, time=dt.split('T')
    s=slice(0, -1)
    time=time[s]
    return date+" "+time+".00"





if __name__=='__main__':
    get_token()
    sendRequest(eventV1)
    processResp()
    print(RES_JSON["items"])