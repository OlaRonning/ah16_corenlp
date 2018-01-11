#!/bin/python2
"""
    Basic script for communicating with CoreNLP server
    Output:
        Prints parse structures from coreNLP to terminal

    To use the script:
        1) Run coreNLP server in seperate process 
           > python2 coreNLP.py &
        2) Run client script (ie this)
           > python2 client.py
"""
import json
from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
from pprint import pprint

class StanfordNLP:
    def __init__(self):
        self.server = ServerProxy(JsonRpc20(),
                                  TransportTcpIp(addr=("127.0.0.1", 8080)))
    
    def parse(self, text):
        return json.loads(self.server.parse(text))

nlp = StanfordNLP()
result = nlp.parse("He could n't fully explain why , but ventured that `` people have a summer rally in July and August and then it 's just profit-taking . ''")
pprint(result)

