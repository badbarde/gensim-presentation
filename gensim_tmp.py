#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 20:47:31 2017
"""
import logging
import sys
import glob
import re
import json as js
from gensim import corpora
from gensim import models
from gensim import similarities

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)

def index_files(corpus_path):
    """indexes a corpus of files and returns a bag of words as a list
    """
    doc_map = dict(enumerate(glob.glob(corpus_path + "/**" + ".txt", recursive=True)))
    ignorechars = re.compile("[:.,;:!?\"-()]\n")

    documents = []
    for file in doc_map.values():
        with open(file, encoding="utf-8", mode="r") as doc:
            documents.append(ignorechars.sub('', doc.read()))

    with open("stopwords.de.json") as stop_js:
        stopwords = js.load(stop_js)

    bags_of_words = [[word for word in doc.lower().split()
                      if word not in stopwords] for doc in documents]

    return (bags_of_words, doc_map)

def search_docs(corpus_path, query, num_results=10, model="tfidf"):
    """searches the corpus for words from the query
    """
    logging.info("looking for " + query + " in " + corpus_path)
    words, mapping = index_files(corpus_path)

    tales_dict = corpora.Dictionary(words)
    corpus = [tales_dict.doc2bow(text) for text in words]

    _model = None
    if model == "lsi":
        _model = models.LsiModel(corpus)
    elif model == "tfidf":
        _model = models.TfidfModel(corpus)
    elif model == "lda":
        _model = models.LdaModel(corpus)

    if _model != None:
        index = similarities.MatrixSimilarity(_model[corpus])
        vec_query = _model[tales_dict.doc2bow(query.lower().split())]
        sorted_result = sorted(enumerate(index[vec_query]), key=lambda i: -i[1])
        retval = [mapping.get(i[0]) for i in sorted_result]
        return retval[:num_results]
    raise ValueError

if __name__ == "__main__":
    for _doc in search_docs(sys.argv[1], sys.argv[2], model=sys.argv[3]):
        print(_doc)
