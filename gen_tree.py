from __future__ import print_function
import json
from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
from pprint import pprint
import sys
import time
import itertools
from collections import OrderedDict


class StanfordNLP:
    def __init__(self):
        self.server = ServerProxy(JsonRpc20(),
                                  TransportTcpIp(addr=("127.0.0.1", 8080)))
    
    def parse(self, text):
        return json.loads(self.server.parse(text))

def chain(*args):
    ''' flattens arguemtents into single list '''
    if len(args) == 1:
        l = itertools.chain.from_iterable(*args)
    else:
        l = itertools.chain(*args)
    return list(l)

def sub_one(w):
    def f(w):
        return chain([w,[str(int(w[-1])-1)]])

    rel,w1,w2 = w
    w1 = f(w1.split('-'))
    w2 = f(w2.split('-'))
    return [rel,w1,w2]

def get_article(example):
    match = example['sluice']
    before = example['entire_sluice_utterance'].split('\n')[4]
    return [before,match]


if __name__ == '__main__':
    nlp = StanfordNLP()
    ## linesWithAnnotations110716_onlyannotated.json
    # Assumes linesep json dumps of examples
    anno_path = sys.argv[1]

    ## For testing features are the same as in article
    anno_data = {} 

    with open(anno_path,'r') as in_:
        for id_,example in enumerate(in_):
            dict_ = json.loads(example)
            try:
                article = get_article(dict_)
            except:
                continue
            anno_data[id_] = article

    with open('trees.jsons','w') as out_:
        for sluice_id,article in anno_data.items():
            for sent in article:
                try:
                    result = nlp.parse(sent)
                except:
                    print('error in parsing',file=sys.stderr)
                    print(sluice_id,file=sys.stderr)
                    print(sent,file=sys.stderr)
                    continue
                try:
                    dict_ = {'sluiceId':sluice_id, 'trees': result['sentences'][-1]['parsetree']}
                except:
                    print('error in dict',file=sys.stderr)
                    print(sluice_id,file=sys.stderr)
                    print(sent,file=sys.stderr)
                    continue
                print(json.dumps(dict_),file=out_)
