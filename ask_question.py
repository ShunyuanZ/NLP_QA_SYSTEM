#!/usr/bin/env python
"""
Connect to stanford NLP server, process given strings/documents, then ask questions
Question types:
1. What, Where, Who, When, What
2. Yes/No
"""
import nltk
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk.parse.stanford import StanfordParser
from nltk.tag.stanford import StanfordPOSTagger
from nltk.parse.stanford import StanfordNeuralDependencyParser
from nltk.parse.stanford import StanfordDependencyParser
from pycorenlp import StanfordCoreNLP
import time
import copy
from generateQ_functions_sz import *
from stanford_process_sz import *
import os
import numpy as np
import itertools
import sys
import json
reload(sys);sys.setdefaultencoding('utf8');sys.getdefaultencoding()

# <editor-fold desc="Read directory and files, connect to stanford corenlp">
# mypath='/pylon1/se4s86p/szhang5/NLP/Project/'
mypath='C:/Users/Yuan_Work/Google Drive/Course/Spring 17/11611 NLP/Project/0410/'
# mypath='D:/Users/shunyuaz/Google Drive/Course/Spring 17/11611 NLP/Project/'  .decode('utf-8')

fname='a1.txt'
document = [line.rstrip('\n') for line in open(fname)]

sentences=[]
for doc in document:
    # print f
    try:
        s=nltk.sent_tokenize(doc)
        sentences.extend(s)
    except Exception as e:
        print e
        # print f

## call stanford nlp to pre-process each sentence in the document
allQ,string_question=[],[]
for sentence in sentences:
    try:
        temp = {}  # store questions for each sentence
        tags, tokens, subs, objs, rels, sub_obj_rel, relations=StanfordNLP_Process(sentence)
        # next, ask questions
        Q_who=ask_who(tags,subs,rels,objs,tokens)
        Q_where1=ask_where_1(tags,subs,rels,objs,tokens)
        Q_where2 = ask_where_2(tags, subs, rels, objs, tokens)
        Q_where=sum([Q_where1,Q_where2],[])
        Q_when=ask_when(tags,tokens,sub_obj_rel)
        Q_what=ask_what(tags, tokens, sub_obj_rel)
        Q_YN=ask_yesno(tags,tokens,sub_obj_rel)
    # record information for each sentence, seperately
        temp['sentence']=sentence
        temp['who']=Q_who
        temp['where']=Q_where
        temp['what']=Q_what
        temp['YN']=Q_YN
        temp['when']=Q_when
        string_question.append(temp)

        allq = itertools.chain(Q_where,Q_YN,Q_when,Q_what,Q_who)
        allQ.extend(list(allq))

    except Exception as e:
        pass
        # print e


# write questions to a text file
file_q = open('generated_questions.txt', 'w')
for q in allQ:
    file_q.write("%s\n" % q)

