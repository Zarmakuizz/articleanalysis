# -*- coding: utf-8 -*-

'''Tests the search.py collection of search functions through database.
Licensed under the WTFPL
'''
import os
import sys
_pathname = os.path.dirname(__file__)
sys.path.append(os.path.normpath(os.path.join(_pathname, '../src')))
from controller.search import *
from model.resource import *
import unittest


class searchTest(unittest.TestCase):

    def setUp(self):
        '''This method is run BEFORE EACH test.
        So we could initialize the database here.'''
        pass # j'ai pas d'idée quoi initialiser pôur l'instant
    
    def tearDown(self):
        '''This method is run AFTER EACH test.
        So we could clean the database after each test.'''
        pass # j'ai pas d'idée quoi vider pour l'instant
    
    def testGetArticle(self):
        '''Adds articles and test the getArticle() search.'''
        nameArticle = "Article sur les saucisses"
        Article(name = nameArticle).put()
        result = getArticle(nameArticle)
        self.assertEquals(nameArticle,result.name)
