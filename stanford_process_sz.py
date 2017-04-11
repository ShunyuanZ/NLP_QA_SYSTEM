"""
Connect to stanford NLP server, process given strings/documents
Extract information:
1. pos tagging, NE recognition, tokens, and relation

If NLTK was unable to find the java file, then do the following:
import os
java_path = "C:/Program Files (x86)/Java/jre1.8.0_121/bin/java.exe"
os.environ['JAVAHOME'] = java_path
----To start the server on cmd:
cd StanfordNLP\stanford-corenlp-full-2016-10-31
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer
"""

from pycorenlp import StanfordCoreNLP
import time
import copy
nlp = StanfordCoreNLP('http://localhost:9000')

def StanfordNLP_Process(sentence):
    # t1 = time.time()
    output = nlp.annotate(sentence, properties={
        'annotators': 'tokenize, pos, parse,openie,ner',
        'outputFormat': 'json'
    })
    # print ('finished parsing string and extracting information using %s seconds' % (time.time() - t1))
    # print (output['sentences'][0].keys())

    # <editor-fold desc="Extract Relations">
    relations = output['sentences'][0]['openie']
    sub_obj_rel, subs, objs, rels = [], [], [], []
    for item in relations:
        sub = item['subject']
        relation = item['relation']
        obj = item['object']
        # print '%s----%s----%s' %(sub,relation,obj)
        subs.append(sub)
        objs.append(obj)
        rels.append(relation)
        d = dict()
        d['sub'] = sub
        d['obj'] = obj
        d['rel'] = relation
        sub_obj_rel.append(d)
        del d, sub, relation, obj
    # </editor-fold>

    # <editor-fold desc="For each word, get the NE and POS tagging">
    tokens = output['sentences'][0][
        'tokens']  # the length is total item/token/word in the string, including puncutation
    tags = []
    pre_ner, pre_word = None, None
    for token in tokens:
        word = token['word']
        ner = token['ner']
        lemma = token['lemma']
        pos = token['pos']
        # print '%s----%s----%s----%s' % (word,lemma, pos, ner)
        if ner != 'O' and ner == pre_ner:
            word = ' '.join([pre_word, word])
            del tags[-1]
            # print 'found same NE: %s and %s are both %s' %(pre_word,word,ner)
        d = dict()
        d['input'] = word
        d['POS'] = pos
        d['NE'] = ner
        d['lemma'] = lemma
        tags.append(d)

        pre_word = copy.copy(word)
        pre_ner = copy.copy(ner)
        del d, word, pos, ner, lemma

    return tags, tokens, subs, objs, rels, sub_obj_rel, relations
    # </editor-fold>
