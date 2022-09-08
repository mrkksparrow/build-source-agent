#Global Variables
TOKEN=''
HEADER=''
FINAL=[] #Streaming responses from all resouces were stored in this FINAL list

fieldSelector=['Pod', 'StatefulSet']

import threading
import time


#Endurl and paths
endpoint='https://kubernetes/apis/events.k8s.io/v1/events?watch=true&fieldSelector=regarding.kind='   #http://localhost:8080
# endpoint='http://localhost:8080/apis/events.k8s.io/v1/events?watch=true&fieldSelector=regarding.kind='


def get_token():
    try:
        import os   
        global TOKEN, HEADER
        if(os.path.isfile('/var/run/secrets/kubernetes.io/serviceaccount/token')):
            fileOPEN=open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r')
            fileRead=fileOPEN.read()
            TOKEN=fileRead.rstrip()
            fileOPEN.close()
            HEADER={
                'Authorization': 'Bearer '+str(TOKEN)
            }
    except Exception as e:
        print(e)


class Events(threading.Thread):
    def __init__(self, fs):
        try:
            threading.Thread.__init__(self)
            self.fs=fs
        except Exception as e:
            print(e)


    def run(self):
        try:
            self.send_request()
        except Exception as e:
            print(e)


    def send_request(self):
        try:
            import requests
            import json
            req=requests.Session()
            with req.get(endpoint+self.fs, headers=HEADER, verify=False, stream=True) as res:
                for line in res.iter_lines():
                    if(line):
                        lineJSON=json.loads(line)
                        lineJSON=json.dumps(lineJSON, indent=4)
                        lock=threading.Lock()
                        lock.acquire()
                        print("This Thread is runs for " +self.fs, time.ctime(time.time()))
                        FINAL.append(lineJSON)
                        print(lineJSON)
                        lock.release()
        except Exception as e:
            print(e)



if __name__=='__main__':
    try:
        get_token()
        threadObject=[]
        for i in fieldSelector:
            insTemp=Events(i)
            threadObject.append(insTemp)
        for i in threadObject:
            i.start()
    except Exception as e:
        print(e)