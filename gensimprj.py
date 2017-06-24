#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 20:47:31 2017
"""
import logging
import os
import json as js
from gensim import corpora
from gensim import models
from gensim import similarities
import loadtexts as lt

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)

if os.path.exists("tales.dict"):
    TALES_DICT = corpora.Dictionary.load("tales.dict")
if os.path.exists("tales_serial.corp"):
    CORPUS = corpora.MmCorpus("tales_serial.corp")
if os.path.exists("tales.mapping"):
    with open("tales.mapping", "r") as fp:
        MAPPING = js.load(fp)
else:
    WORDS, MAPPING = lt.index_files()
    with open("tales.mapping", "w") as fp:
        js.dump(MAPPING, fp)
    TALES_DICT = corpora.Dictionary(WORDS)

    TALES_DICT.save("tales.dict")
    CORPUS = [TALES_DICT.doc2bow(text) for text in WORDS]
    corpora.MmCorpus.serialize("tales_serial.corp", CORPUS)

TFIDF = models.TfidfModel(CORPUS)
CORPUS_TFIDF = TFIDF[CORPUS]
TFIDF.save("tfidf")

#get a mapping form tokens to ids
TOKENIDMAPPING = TALES_DICT.token2id

#create query vector

LSI = models.LsiModel(CORPUS_TFIDF, id2word=TALES_DICT, num_topics=4)
CORPUS_LSI = LSI[CORPUS]#CORPUS_TFIDF
INDEX = similarities.MatrixSimilarity(CORPUS_LSI)

QUERY = "Frosch"
VEC_QUERY = TALES_DICT.doc2bow(QUERY.lower().split())
VEC_LSI = LSI[VEC_QUERY]
RESULT = INDEX[VEC_LSI]
logging.info("result")
for res in RESULT:
    print(res)
SORTED_RESULT = sorted(enumerate(RESULT), key=lambda item: item[1], reverse=True)
logging.info("sorted")
for res in SORTED_RESULT:
    print(res)


logging.info("Results for " + QUERY)
logging.info(MAPPING)
logging.info(SORTED_RESULT)

for res in SORTED_RESULT:
    print(MAPPING.get((str(res[0])), "doc not found"))
#tfidfi_dict = tfidf[dictionary]

#texts = [[[word for word in line.split() if word not in stoplist]
#          for line in document]
#         for document in documents]
