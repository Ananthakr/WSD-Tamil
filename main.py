#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient

#make the given word and object to be used in find() by pymongo
def makeSearchObject(w):
    obj={
        'pkey':w
    }
    return obj

#scores each given meaning's related words and sentence
def scoreMeaning(rel_list,sent):
    score=0
    for str in sent:
        for wd in rel_list:
            for r in wd:
                if(r==str):
                    score=score+wd[r]
    return score

#returns the index of meaning which has high score and selected
def selectMeaning(ms):
    scr=[]
    i=0
    for z in ms:
        for y in z:
            scr.append(z[y])
        i=i+1
    #print scr
    mx_val=max(scr)
    mx_indx=scr.index(mx_val)
    #print mx_indx
    return mx_indx

#find relative word from sentence
def findInList(w,sent):
        f=0
        for str in sent:
           if(str==w):
               f=f+1
        return f

#update the dict with new scores for rel. words
def updateDict(dict,wd,indx,mean,sent):
    for rel in dict[wd][indx][mean]:
        for q in rel:
            found=findInList(q,sent)
            if(found==0):
                rel[q]=rel[q]-0.25
            else :
                rel[q]=rel[q]+0.25


    return dict

#make found words from sent to obj
def newKeyObj(re):
    obj={
        re:0.5
    }
    return obj

#duplicates in new keys found
def duplicateKeysRemoval(newKeys,ex_list):
     dummy=newKeys
     x=[]
     for key in dummy:
         f=findInList(key,ex_list)
         if(f==0):
             x.append(key)
     return x

#get two words from the sentence
def findKeySent(pos,sent,ex_list):
    newKeys=[]
    if(pos==len(sent)-1):
        #print sent[pos-1]+" "+sent[pos-2]
        newKeys.append(sent[pos-1])
        newKeys.append(sent[pos-2])
    elif(pos==0):
        #print sent[pos+1]+" "+sent[pos+2]
        newKeys.append(sent[pos + 1])
        newKeys.append(sent[pos + 2])
    else:
        #print sent[pos-1]+" "+sent[pos+1]
        newKeys.append(sent[pos - 1])
        newKeys.append(sent[pos + 1])

    return duplicateKeysRemoval(newKeys,ex_list)

#for removing low value rel. words when count >8
def removeUnrelated(dict,word,sel_indx,sel_mean,c):
    vals=[]
    if(c==0):
        return vals
    for i in dict[word][sel_indx][sel_mean]:
        for x in i:
            vals.append(i[x])

    if(not vals):
        rm=vals.index(min(vals))
    print rm
    dict[word][sel_indx][sel_mean].pop(rm)
    print dict[word][sel_indx][sel_mean]
    if(c==1):
        return dict
    else:
        return removeUnrelated(dict,word,sel_indx,sel_mean,c-1)


#connect to mongodb
client = MongoClient('localhost', 27017)
db = client.wsd
words=db.words

#dummy sentence and word for testing
#sent=u"சூரியன் மாலை மறை".split()
#word=u"மாலை"

word=raw_input("Enter the word: ").decode("utf-8")
sent=raw_input("Enter the sentence: ").decode("utf-8").split()

if(findInList(word,sent)==0):
    print "given sentence doesnt contain the word. plz recheck the data"
else :
    #to find the position of ambiguited word in the sentence
    pos=0
    for i in range(len(sent)):
        if(word==sent[i]):
            pos=i

    #get the word data as a dictionary
    cur=words.find(makeSearchObject(word))
    if(cur.count()<=0):
        print "Word is nt found in our database.kindly update via word_db.py"
    else:
        meanings=[]

        #get all meanings as object from dictionary
        for doc in cur:
            dict=doc

        #print dict[word]
        ms=dict[word]

        #extract each meanings and find scores with relative words list for each
        for m in ms:
            for n in m.keys():
                x=m[n]
                meanings.append({n:scoreMeaning(m[n],sent)})

        print meanings
        #get index and word of selected meaning
        sel_indx=selectMeaning(meanings)
        for p in meanings[sel_indx]:
            sel_mean=p
        print sel_mean

        #get relw as list for the selected meaning
        sel_relw_mlist=[]
        for s in dict[word][sel_indx][sel_mean]:
            for l in s:
                sel_relw_mlist.append(l)
        #print sel_relw_mlist


        #print dict[word][sel_indx][sel_mean]
        rescored_dict=updateDict(dict,word,sel_indx,sel_mean,sent)
        #print rescored_dict

        '''#for testing count>8 for rel.words
        inx=0
        for inx in range(6):
            rescored_dict[word][sel_indx][sel_mean].append(newKeyObj("dummy%s" % (inx)))'''

        newKeys=findKeySent(pos,sent,sel_relw_mlist)

        #if rel. words list is full remove low score values
        if(len(rescored_dict[word][sel_indx][sel_mean])>=8):
            removeUnrelated(rescored_dict, word, sel_indx, sel_mean, len(newKeys))

        #append new rel words
        for i in newKeys:
            rescored_dict[word][sel_indx][sel_mean].append(newKeyObj(i))

        #print rescored_dict
        #save changes to db
        words.save(rescored_dict)
