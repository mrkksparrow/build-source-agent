import requests
import os
import json


HOST='kubernetes'
PROTOCOL='https'
TOKEN=''
HEADERS={}
NODES=[]
kubernetesApiEp=PROTOCOL+'://'+HOST+'/api/v1/nodes/'
kubeletEp='/proxy/stats/summary'




class Kubelet:
    def __init__(self):
        self.get_token()
        self.getNodesMetrics()


    def get_token(self):
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
    

    def getNodesMetrics(self):
        try:
            self.getNodes()
            nodeMetrics={}
            for i in NODES:
                nodeRes=self.getReq(kubernetesApiEp+i+kubeletEp)
                nodeMetrics.setdefault(i, nodeRes)
            nodeMetrics=json.dumps(nodeMetrics, indent=4)
            js=open('./Kubelet.json', 'w')
            js.write(nodeMetrics)
            js.close()
        except Exception as e:
            print(e)


    def getNodes(self):
        try:
            global NODES
            nodeData=self.getReq(kubernetesApiEp)
            nodeData=nodeData.get('items')
            for i in nodeData:
                NODES.append(i.get('metadata').get('name'))
            # print(NODES)
        except Exception as e:
            print(e)


    def getReq(self, url):
        try:
            js=requests.get(url, headers=HEADERS, verify=False)
            return js.json()
        except Exception as e:
            print(e)




if __name__=='__main__':
    kubeObj=Kubelet()
