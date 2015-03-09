from sseclient import SSEClient
import requests
import json
import sys


if not len(sys.argv) == 2:
    print 'USAGE: python client.py <DATABASE>'
    exit(1)
base_url = 'https://'+sys.argv[1]+'.firebaseio.com/'
firebase_url = base_url+'.json'
requests.patch(firebase_url,'{"status":0}')
requests.delete(base_url+'ip/.json')
requests.patch(firebase_url,'{"status":1}')
sse = SSEClient(firebase_url)
for msg in sse:
    msg_data = json.loads(msg.data)
    if msg_data is None:
        continue
    path = msg_data['path']
    data = msg_data['data']
    if 'ip' in data:
        ip = data['ip']
        print 'IP is '+ip
        exit(1)
