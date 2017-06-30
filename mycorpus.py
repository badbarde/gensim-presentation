#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 20:47:31 2017
"""
import json
from gensim.corpora import Dictionary

class MyCorpus():
    """Simple implementation of a corpus
    """
    def __init__(self, path):
        """initializes the path variable
        """
        self.path = path
    def __iter__(self):
        """yields a doc per iteration
        """
        with open(self.path) as file_stream:
            for doc in json.load(file_stream):
                yield Dictionary.doc2bow(doc)
