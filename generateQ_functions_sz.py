"""
Self define functions to generate question for extracted information from a sentence
Information extracted using Stanford nlp, including
1. pos tagging, NE recognition, tokens, and relation
2. ask questions
Question types:
1. What, Where, Who, When, What
2. Yes/No
"""


def return_verbs(rel,tokens):
    be = {'is', 'was', 'are', 'were'}
    VBformats = {'VBZ', 'VBP', 'VBD', 'VBG', 'VBN'}

    seq = rel.split()
    verbs = []
    for w in seq:
        # print w
        verb=None
        # get pos tag for each word
        if w in be:
            verb=[w]
            verbs.append(verb)
        else:
            pos = [t['pos'] for t in tokens if t['word'] == w][0]
            lemma = [t['lemma'] for t in tokens if t['word'] == w][0]
            if pos=='VBZ':
                verb=['does',lemma]
                verbs.append(verb)
            elif pos=='VBD' or pos=='VBN':
                verb = ['did', lemma]
                verbs.append(verb)
            elif pos=='VBP' or pos=='VBG':
                verb = [lemma]
                verbs.append(verb)
            else:
                verb=[w]
                verbs.append(verb)
        del verb
    return verbs


def ask_who(tags,subs,rels,objs,tokens):
    persons=[entry['input'] for entry in tags if entry['NE']=='PERSON']
    Q_who=[]
    for person in persons:
        # print person
        question=None
        # see if this person is a subject
        try:
            ind=subs.index(person)
            rel,obj=rels[ind],objs[ind]
            # print rel,obj
            q = ' '.join(['Who', rel, obj])
            question = q + '?'
            # add question mark
            dates = [entry['input'] for entry in tags if entry['NE'] == 'DATE']
            if len(dates) > 0:
                date = dates[0]
                question = q + ' ' + date.lower() + '?'
            Q_who.append(question)
        except Exception as e:
            pass
        #     print '---------during generating WHO question------'
        #     print e
            # print 'did not find %s  in the subjects list' %(person)
        # see if this person is an object
        try:
            ind=objs.index(person)
            rel,sub=rels[ind],subs[ind]
            # print rel,sub
            verbs=return_verbs(rel,tokens)
            verbs=sum(verbs,[])
            vb1=verbs[0]
            temp_vb2=verbs[1:]
            vb2=' '.join(temp_vb2)
            q = ' '.join(['Who',vb1,sub,vb2])
            question=q+'?'
             # add time_stamp
            dates = [entry['input'] for entry in tags if entry['NE'] == 'DATE']
            if len(dates)>0:
                date=dates[0]
                question=q+' '+date.lower()+'?'
            Q_who.append(question)
            del question
        except Exception as e:
            pass
        #     print '---------during generating WHO question------'
        #     print e
    return Q_who


def ask_where_1(tags,subs,rels,objs,tokens):
    locations=[entry['input'] for entry in tags if entry['NE']=='LOCATION']
    Q_where=[]
    for location in locations:
        # print location
        # question=None
        # see if this location is a subject
        try:
            ind=subs.index(location)
            rel,obj=rels[ind],objs[ind]
            # print rel,obj
            verbs=return_verbs(rel,tokens)
            verbs=sum(verbs,[])
            vb1=verbs[0]
            temp_vb2=verbs[1:]
            vb2=' '.join(temp_vb2)
            q = ' '.join(['Where',vb1,vb2,obj])
            question = q + '?' # add question mark
            # add time_stamp
            dates = [entry['input'] for entry in tags if entry['NE'] == 'DATE']
            if len(dates) > 0:
                date = dates[0]
                question = q + ' ' + date.lower() + '?'
            Q_where.append(question)
        except Exception as e:
            pass
        #     print '---------during generating WHERE question------'
        #     print e
        # see if this location is an object
        try:
            ind=objs.index(location)
            rel,sub=rels[ind],subs[ind]
            # print rel,sub
            verbs=return_verbs(rel,tokens)
            verbs=sum(verbs,[])
            vb1=verbs[0]
            temp_vb2=verbs[1:]
            vb2=' '.join(temp_vb2)
            q = ' '.join(['Where',vb1,sub,vb2])
            question=q+'?'
            # add time_stamp
            dates = [entry['input'] for entry in tags if entry['NE'] == 'DATE']
            if len(dates) > 0:
                date = dates[0]
                question = q + ' ' + date.lower() + '?'
            Q_where.append(question)
        except Exception as e:
            pass
        #     print '---------during generating WHERE question------'
        #     print e
    return Q_where


def ask_where_2(tags,subs,rels,objs,tokens):
    organizations=[entry['input'] for entry in tags if entry['NE']=='ORGANIZATION']
    Q_where_2=[]
    for location in organizations:
        # print organization
        # question=None
        # see if this location is a subject
        try:
            ind=subs.index(location)
            rel,obj=rels[ind],objs[ind]
            # print rel,obj
            verbs=return_verbs(rel,tokens)
            verbs=sum(verbs,[])
            vb1=verbs[0]
            temp_vb2=verbs[1:]
            vb2=' '.join(temp_vb2)
            q = ' '.join(['Where',vb1,vb2,obj])
            question = q + '?' # add question mark
            # add time_stamp
            dates = [entry['input'] for entry in tags if entry['NE'] == 'DATE']
            if len(dates) > 0:
                date = dates[0]
                question = q + ' ' + date.lower() + '?'
                Q_where_2.append(question)
        except Exception as e:
            pass
        #     print '---------during generating WHERE-2 question------'
        #     print e
        # see if this organization is an object
        try:
            ind=objs.index(location)
            rel,sub=rels[ind],subs[ind]
            # print rel,sub
            verbs=return_verbs(rel,tokens)
            verbs=sum(verbs,[])
            vb1=verbs[0]
            temp_vb2=verbs[1:]
            vb2=' '.join(temp_vb2)
            q = ' '.join(['Where', vb1,sub, vb2])
            question=q+'?'
            # add time_stamp
            dates = [entry['input'] for entry in tags if entry['NE'] == 'DATE']
            if len(dates) > 0:
                date = dates[0]
                question = q + ' ' + date.lower() + '?'
                Q_where_2.append(question)
        except Exception as e:
            pass
        #     print '---------during generating WHERE-2 question------'
        #     print e
    return Q_where_2


def ask_when(tags,tokens,sub_obj_rel):
    dates=[entry['input'] for entry in tags if entry['NE']=='DATE']
    Q_when=[]
    for date in dates:
        # print date
        # try each sub-ojb relationship
        for tuple3 in sub_obj_rel:
            question = None
            sub, obj, rel=tuple3['sub'],tuple3['obj'],tuple3['rel']
            verbs = return_verbs(rel, tokens)
            verbs=sum(verbs,[])
            vb1=verbs[0]
            temp_vb2=verbs[1:]
            vb2=' '.join(temp_vb2)
            q = ' '.join(['When',vb1,sub, vb2,obj])
            question = q + '?'
            Q_when.append(question)
    return Q_when


def ask_what(tags,tokens,sub_obj_rel):
    nouns_tag=['NN','NNS','NNP','NNPS'] # want to look at nouns
    nouns_ne=['LOCATION','PERSON'] # not to look at person or locations for "WHAT" question generation
    Q_what=[]
    question=None
    dates = [entry['input'] for entry in tags if entry['NE'] == 'DATE']
    for tuple3 in sub_obj_rel:
        sub, obj, rel=tuple3['sub'],tuple3['obj'],tuple3['rel'] # get pos tagging
        try:
            sub_tag=[t['POS'] for t in tags if t['input']==sub][0]
            obj_tag = [t['POS'] for t in tags if t['input'] == obj][0]
            sub_ne=[t['NE'] for t in tags if t['input']==sub][0] # get named entity label
            obj_ne = [t['NE'] for t in tags if t['input'] == obj][0]
            ## look at if obj is a noun (and not person or location)
            if obj_tag in nouns_tag and obj_ne not in nouns_ne:
                verbs = return_verbs(rel, tokens)
                verbs=sum(verbs,[])
                vb1=verbs[0]
                temp_vb2=verbs[1:]
                vb2=' '.join(temp_vb2)
                q = ' '.join(['What',vb1,sub,vb2])
                question = q + '?'
                if len(dates) > 0:
                    date = dates[0]
                    question = q + ' ' + date.lower() + '?'
                Q_what.append(question)

                ## look at if sub is a noun (and not person or location)
                if sub_tag in nouns_tag and sub_ne not in nouns_ne:
                    q = ' '.join(['What', rel, obj])
                    question = q + '?'
                    if len(dates) > 0:
                        date = dates[0]
                        question = q + ' ' + date.lower() + '?'
                    Q_what.append(question)
        except Exception as e:
            pass
        #     print '---------during generating WHAT question------'
        #     print e
    return Q_what


def ask_yesno(tags,tokens,sub_obj_rel):
    Q_YN=[]
    question=None
    dates = [entry['input'] for entry in tags if entry['NE'] == 'DATE']
    for tuple3 in sub_obj_rel:
        sub, obj, rel=tuple3['sub'],tuple3['obj'],tuple3['rel'] # get pos tagging
        try:
            verbs = return_verbs(rel, tokens)
            verbs=sum(verbs,[])
            vb1=verbs[0]
            temp_vb2=verbs[1:]
            vb2=' '.join(temp_vb2)
            q = ' '.join([vb1.title(),sub,vb2,obj]) #
            question = q + '?'
            if len(dates) > 0:
                date = dates[0]
                question = q + ' ' + date.lower() + '?'
            Q_YN.append(question)
        except Exception as e:
            pass
            # print '---------during generating WHAT question------'
            # print e
    return Q_YN

