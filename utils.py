#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""utils module
"""
import os
import json
from gensim import corpora

def load_saves():
    """tries to load saved data from disc returns none if none was found
    """
    if os.path.exists("mydict.dict"):
        my_dict = corpora.Dictionary.load("mydict.dict")
    if os.path.exists("mycorpus.corp"):
        my_corpus = corpora.MmCorpus("mycorpus.corp")
    if os.path.exists("mydocs.json"):
        with open("tales.json", "r") as afile:
            doc_map = json.load(afile)
    else:
        return None
    return (doc_map, my_dict, my_corpus)
