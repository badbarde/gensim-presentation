#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 20:47:31 2017
"""
import logging
import sys
import os
import glob
import re
import argparse
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
    ignorechars = """[:.,;!?"-()]_\\/»«<>$%&@€=+*~"#´`{}|\r\n\t“”‐"""
    for file in doc_map.values():
        with open(file, encoding="utf-8", mode="r") as doc:
            None
            #TODO: dokumente bereinigen und returnen
        yield mydoc

def get_stopwords(stop_word_file):
    """returns a set of stopwords from the given path
    """
    #TODO: Stopwords als set returnen

def index_files(corpus_path):
    """indexes a corpus of files and returns a bag of words as a list
    """
    doc_map = get_file_map(corpus_path)
    stopwords = get_stopwords("resources/stopwords.de.json")

    #TODO: bag of words erstellen
    return (bags_of_words, doc_map)

def search_docs(corpus_path, query, num_results=10, model=models.TfidfModel):
    """searches the corpus for words from the query
    """
    logging.info("looking for " + ", ".join(query) + " in " + corpus_path)
    words, mapping = index_files(corpus_path)

    #TODO: lets gensim
    tales_dict = corpora.Dictionary(words)
    corpus = [tales_dict.doc2bow(text) for text in words]

    tales_dict.save("resources/my_dict.dict")
    tales_dict.save_as_text("resources/my_text_dict.dict")
    save_all_corpi(corpus)

    with open("resources/mycorpus.json", mode="w", encoding="utf-8") as file_stream:
        json.dump(corpus, file_stream)

    #corpus = MyCorpus("mycorpus.json")

    my_model = model(corpus)
    index = similarities.Similarity(my_model[corpus])

    logging.info("returning " + str(num_results))
    return retval[:num_results]

def handle_args(argv):
    """parse given arguments
    """
    parser = argparse.ArgumentParser(description="Seach based on semantica \
                                      similarity trough a directory with textfiles")
    parser.add_argument("corpus", metavar="PATH", type=str,# nargs='+',
                        help="must be a path to a diectory with the documents\
                         that are supposed to be searched through")
    parser.add_argument("query", metavar="QUERY", type=str, nargs='+',
                        help="combination of words that you want to sind similar\
                         documents to")
    parser.add_argument("-n", "--nresults", dest="num_results", type=int,
                        help="specify max number of search results")
    parser.add_argument("-m", "--model", dest="model", default="tfidf",
                        help="optionally define model for representing the corpus")

    parser.add_argument("-q", "--quiet", dest="quiet", action="store_const",
                        const=True, help="supress messages (besides results)")
    parser.add_argument("-d", "--debug", dest="debug", action="store_const",
                        const=True, help="enable debug messages")

    args = parser.parse_args(argv)

    if args.quiet:
        logging.getLogger().setLevel(logging.ERROR)
    elif args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.model.lower() == "tfidf":
        my_model = models.TfidfModel
    elif args.model.lower() == "lsi":
        my_model = models.LsiModel
    elif args.model.lower() == "lda":
        my_model = models.LdaModel
    else:
        logging.error(args + " unknown model")
        sys.exit()

    res = search_docs(args.corpus, args.query, args.num_results, my_model)
    for r in res:
        print(r)

if __name__ == "__main__":
    handle_args(sys.argv[1:])
