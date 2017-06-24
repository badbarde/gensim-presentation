#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
load corpus and return words
"""
import json
import re
import glob
import logging

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
    filemapping = dict(enumerate(files))
    for file in filemapping.values():
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
    return (texts, filemapping)
