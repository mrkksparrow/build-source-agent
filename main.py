import requests
import json
from datetime import datetime

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


# def get_token():
#     try:
#         import os   
#         global TOKEN, HEADER
#         TOKEN=os.system('cat /var/run/secrets/kubernetes.io/serviceaccount/token')
#         HEADER='Authorization: Bearer '+str(TOKEN)
#     except Exception as e:
#         print(e)



def sendRequest(path):
    try:
        global RESP_DATA
        req=requests.Session()
        fileRead=open("./sample.json", "r")
        jsonRead=json.load(fileRead)
        fileRead.close()
        with req.get(endpoint+path, stream=True) as res:
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



# def fetchByMin(min):
#     try:
#         global RESP_JSON, RES_JSON
#         now=str(datetime.utcnow())
#         now=datetime.strptime(now, "%Y-%m-%d %H:%M:%S.%f")
#         for i in RESP_JSON:
#             ts=dtSplit(i["metadata"]["creationTimestamp"])
#             ts=datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f")
#             print(now-ts)
#             timeRes=str(now-ts).split(",")
#             if(len(timeRes)==1):
#                 timeRes=timeRes[0].split(":")
#                 if((timeRes[0]=='0' or timeRes[0]=='00') and int(timeRes[1])<=min):
#                     RES_JSON["items"].append(i)
#     except Exception as e:
#         print(e)


# #Split the Timestamp format
# def dtSplit(dt):
#     try:
#         date, time=dt.split('T')
#         s=slice(0, -1)
#         time=time[s]
#         return date+" "+time+".00"
#     except Exception as e:
#         print(e)



if __name__=='__main__':
    sendRequest(eventV1)