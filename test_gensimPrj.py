#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 20:47:46 2017

@author: rene
"""
import unittest
import gensimprj as gp


class TestInrSys(unittest.TestCase):
    """tests for gensimprj
    """

    def test_index(self):
        """test the returnvalue of index_files
        """
        self.assertIsInstance(list(), gp.index_files())
        self.countTestCases

if __name__ == '__main__':
    unittest.main()
