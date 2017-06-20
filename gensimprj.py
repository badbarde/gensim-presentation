#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 20:47:31 2017
"""
import logging
import glob
import re
import json
from gensim import corpora
from gensim import models

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def get_stopwords():
    """read in stoplistfile and return list of stopwords
    """
    #remove stopwords
    stoplist = []
    with open("stopwords.de.json") as stopdoc:
        stoplist = json.load(stopdoc)
    return stoplist

def index_files():
    """indexes a corpus of files and returns a bag of words as a list
    """
    files = glob.glob("CorpusUTF8/**" + ".txt", recursive=True)
    documents = []
    for file in files:
        with open(file, encoding="utf-8", mode="r") as doc:
            documents.append(doc.readlines())

    ignorechars = re.compile("[:.,;:!?\"-()]")


    texts = []
    stopcnt = 0
    for doc in documents:
        doctext = []
        for line in doc:
            line = ignorechars.sub('', line)
            for word in line.split():
                if word.lower() not in get_stopwords():
                    doctext.append(word.lower())
                else:
                    stopcnt += 1
        texts.append(doctext)
    logging.info("stopwords removed: " + str(stopcnt))
    return texts

dictionary = corpora.Dictionary(index_files())
tfidf = models.TfidfModel(dictionary)
#get a mapping form tokens to ids
tokenidmapping = dictionary.token2id
#create query vector
query = dictionary.doc2bow("Hexe Frosch".lower().split())
print(tfidf[query])

#tfidfi_dict = tfidf[dictionary]
tfidf.save("tfidf")

print(len(index_files()))
#texts = [[[word for word in line.split() if word not in stoplist]
#          for line in document]
#         for document in documents]
