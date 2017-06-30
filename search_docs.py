#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 20:47:31 2017
"""
import logging
import sys
import glob
import re
from functools import partial
import json
from gensim import corpora
from gensim import models
from gensim import similarities
from mycorpus import MyCorpus

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)

def get_file_map(corpus_path):
    """creates a dictionary that assigns a numerical value to a document
    """
    return dict(enumerate(glob.glob(corpus_path + "/**" + ".txt", recursive=True)))

def get_texts(doc_map):
    """returns a list of texts where each text is a document from doc_map
    """
    ignorechars = re.compile("[:.,;:!?\"-()]\n")
    for file in doc_map.values():
        with open(file, encoding="utf-8", mode="r") as doc:
            yield ignorechars.sub('', doc.read())

def get_stop_words(stop_word_file):
    """returns a set of stopwords from the given path
    """
    with open(stop_word_file) as stop_js:
        stopwords = set(json.load(stop_js))#important !1!!! SET
    return stopwords

def index_files(corpus_path):
    """indexes a corpus of files and returns a bag of words as a list
    """
    doc_map = get_file_map(corpus_path)
    stop_words = get_stop_words("stopwords.de.json")

    bags_of_words = [[word for word in doc.lower().split()
                      if word not in stop_words] for doc in get_texts(doc_map)]

    return (bags_of_words, doc_map)

def search_docs(corpus_path, query, num_results=10, model=models.TfidfModel):
    """searches the corpus for words from the query
    """
    logging.info("looking for " + query + " in " + corpus_path)
    words, mapping = index_files(corpus_path)

    tales_dict = corpora.Dictionary(words)
    corpus = [tales_dict.doc2bow(text) for text in words]

    with open("mycorpus.json", mode="w", encoding="utf-8") as file_stream:
        json.dump(corpus, file_stream)

    #corpus = MyCorpus("mycorpus.json")

    my_model = model(corpus)
    index = similarities.MatrixSimilarity(my_model[corpus])

    vec_query = my_model[tales_dict.doc2bow(query.lower().split())]
    sorted_result = sorted(enumerate(index[vec_query]), key=lambda i: -i[1])
    retval = [mapping.get(i[0]) for i in sorted_result]
    logging.info("returning " + str(num_results))
    return retval[:num_results]

if __name__ == "__main__":
    my_search = partial(search_docs, sys.argv[1])
    my_search = partial(my_search, sys.argv[2])
    my_search = partial(my_search, 10)

    if sys.argv[3].lower() == "tfidf" or sys.argv[3].lower() == None:
        search_results = my_search(models.TfidfModel)
    elif sys.argv[3].lower() == "lsi":
        search_results = my_search(models.LsiModel)
    elif sys.argv[3].lower() == "lda":
        search_results = my_search(models.LdaModel)
    else:
        logging.info(sys.argv[3] + " unknown model")
        sys.exit()

    for result in search_results:
        print(result.replace(sys.argv[1] + "/", ""))
