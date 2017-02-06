#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient

#connect to db
client = MongoClient('localhost', 27017)
db = client.wsd

#to create a meaning object
def createMeaning(m,rel):
    obj={
        m:[
        ]
    }
    for i in range(len(rel)):
        obj[m].append({rel[i]:1})
    return obj

#to create an array of meanings
def createMeanings(means,rels):
    arr=[]
    for i in range(len(means)):
        arr.append(createMeaning(means[i],rels[i]))
    return arr

#to create an object for a word to be inserted to db
def createWord(w,means):
    obj={
        'pkey': w,
        w:[
        ]
    }
    for i in range(len(means)):
        obj[w].append(means[i])
    return obj

re=[]
re1=[]
w=raw_input("Enter the word:")
m=raw_input("Enter all meanings of word (delimited with space):").split()
print m
if not w:
    print "Enter a word to store not enter key/spacekey"
elif not m:
        print "Enter a meanings to store not enter key/spacekey"
else:
        for i in range(len(m)):
            re1 = raw_input("Enter rel. words of meaning (delimited with space) " + str(i) + " :").split()
            re.append(re1)
        # create object for word and given data
        o = createWord(w, createMeanings(m, re))
        words = db.words
        print db.collection_names()
        # insert into db
        wid = words.insert(o)
        print wid