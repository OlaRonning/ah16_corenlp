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
    before = [sent['string'] for sent in example['before']]
    match = example['match']['sentence']['string']
    candidates = before+[match]
    return candidates[-2:]

    sent = sent.split(' ')
    deps_out = []
    for dt,w1,w2 in deps:
        deps_out.append([dt,w1+idx(w1,sent),w2+idx(w2,sent)])
    return deps_out


def get_article(example):


if __name__ == '__main__':
    nlp = StanfordNLP()
    ## linesWithAnnotations110716_onlyannotated.json
    # Assumes linesep json dumps of examples
    anno_path = sys.argv[1]

    ## For testing features are the same as in article
    anno_data = {} 
    ids = []

    with open('sluice.ids','r') as in_:
        for id_ in in_:
            ids.append(id_.strip())


    print(ids[0])
    with open(anno_path,'r') as in_:
        for example in in_:
            dict_ = json.loads(example)
            try:
                sluice_id = "{0[file]}_{0[line]}_{0[treeNode]}".format(dict_['metadata'])
                #only need article
                if not sluice_id in ids:
                    continue
                article = get_article(dict_)
            except:
                continue
            anno_data[sluice_id] = article

    with open('dep_lemma.jsons','w') as out_:
        for sluice_id,article in anno_data.items():
            for sent in article:
                try:
                    result = nlp.parse(sent)
                except:
                    print('error in parsing',file=sys.stderr)
                    print(sluice_id,file=sys.stderr)
                    print(sent,file=sys.stderr)
                    continue
                lemmas = [word[-1]['Lemma'] for word in result['sentences'][-1]['words']]
                try:
                    dict_ = {'sluiceId':sluice_id, 'deps': list(map(sub_one,result['sentences'][0]['dependencies'])),'string':sent,'lemmas':lemmas}
                except:
                    print('error in dict',file=sys.stderr)
                    print(sluice_id,file=sys.stderr)
                    print(sent,file=sys.stderr)
                    continue
                print(json.dumps(dict_),file=out_)
