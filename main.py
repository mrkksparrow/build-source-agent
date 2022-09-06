#Global Variables
TOKEN=''
HEADER=''


#Filterations
nodeFilter=[
    'TerminatedAllPods', 'NodeNotSchedulable', 'CIDRNotAvailable', 
    'RegisteredNode', 'Starting', 'KubeletSetupFailed', 
    'RemovingNode', 'NodeSelectorMismatching', 'InsufficientFreeCPU',
    'DeletingNode', 'CIDRAssignmentFailed', 'FailedMount',
    'DeletingAllPods', 'InsufficientFreeMemory', 'OutOfDisk',
    'TerminatingEvictedPod', 'HostNetworkNotSupported', 'NilShaper',
    'NodeReady', 'Rebooted', 'NodeHasSufficientDisk',
    'NodeNotReady', 'NodeOutOfDisk', 'InvalidDiskCapacity',
    'NodeSchedulable', 'FreeDiskSpaceFailed'
]
podFilter=[
    'Pulling', 'Pulled', 'Failed',
    'InspectFailed', 'ErrImageNeverPull', 'BackOff',
    'Created', 'Started', 'Killing',
    'Unhealthy', 'FailedSync', 'FailedValidation',
    'OutOfDisk', 'HostPortConflict'
]
rcFilter=[
    'SuccessfulCreate', 'FailedCreate', 'SuccessfulDelete', 'FailedDelete'
]


#Endurl and paths
endpoint='https://kubernetes'   #http://localhost:8080
apiPath='/apis/events.k8s.io/v1/events?watch=true' #or /api/v1/watch/events


class Events:
    def __init__(self):
        self.nodeFilter=nodeFilter
        self.podFilter=podFilter
        self.rcFilter=rcFilter
        self.send_request()


    def get_token(self):
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


    def send_request(self):
        try:
            self.get_token()
            import requests
            import json
            req=requests.Session()
            with req.get(endpoint+apiPath, headers=HEADER, verify=False, stream=True) as res:
                for line in res.iter_lines():
                    if(line):
                        lineJSON=json.loads(line)
                        lineJSON=json.dumps(lineJSON, indent=4)
                        self.filter_events(lineJSON)
        except Exception as e:
            print(e)
        

    def filter_events(self, lineJSON):
        try:
            keys=lineJSON.keys()
            if "object" in keys:
                kind=lineJSON["object"]["regarding"]["kind"]
                reason=lineJSON["object"]["reason"]
                
                if kind=="Pod" and reason in self.podFilter:
                    print(lineJSON)
                elif kind=="Node" and reason in self.nodeFilter:
                    print(lineJSON)
                elif kind=="ReplicationController" and reason in self.rcFilter:
                    print(lineJSON)   

        except Exception as e:
            print(e)


if __name__=='__main__':
    eve=Events()