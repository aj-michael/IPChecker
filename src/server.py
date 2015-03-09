from sseclient import SSEClient
from threading import Thread
import requests
import socket
import json
import sys


class IPChecker(Thread):

    def __init__(self,firebase_url):
        self.firebase_url = firebase_url
        super(IPChecker, self).__init__()


    # this is sucky, but I'm in a rush
    def get_ip(self,endpoint='http://www.whatsmyip.net'):
        r = requests.get(endpoint)
        return r.content.split('value="')[1].split('"')[0]


    def run(self):
        try:
            self.sse = SSEClient(self.firebase_url)
            for msg in self.sse:
                msg_data = json.loads(msg.data)
                if msg_data is None:    #This will be most of them
                    continue
                path = msg_data['path']
                data = msg_data['data']
                if type(data) == dict and 'status' in data and data['status'] == 1:
                    ip = self.get_ip()
                    requests.patch(self.firebase_url,'{"ip":"'+ip+'"}')
                    requests.patch(self.firebase_url,'{"status":0}')
        except socket.error:
            pass




if __name__ == '__main__':
    if not len(sys.argv) == 2:
        print 'USAGE: python server.py <DATABASE>'
        exit(1)
    firebase_url = 'https://'+sys.argv[1]+'.firebaseio.com/.json'
    ip_thread = IPChecker(firebase_url)
    ip_thread.start()
