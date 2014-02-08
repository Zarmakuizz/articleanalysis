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
from controller.mapReduce import *
from controller.storeData import *
import unittest


class searchTest(unittest.TestCase):
    
    nameArticle = "Article sur les saucisses"
    nameAuthor = "Tomtom"
    article = None
    author = None
    def setUp(self):
        '''This method is run BEFORE EACH test.
        So we could initialize the database here.'''
        
        article = Article(name = self.nameArticle)
        article.put()
        
        author = Author(name = self.nameAuthor)
        author.put()
        artiAuth = ArtiAuth(keyAuthor= author, keyArticle=article)
        artiAuth.put()
        
        text = "La mère du maire est dans la mer; Le vers dans le verre est vert; j'ai mon thé sur la table;"
        dataDict = mapper(text,"src")
        dataDict = reducer(dataDict)
        
        for cle in dataDict.keys():
            mapReduce = MapReduce(keyWord = cle, keyArticle = article, count = dataDict[cle])
            mapReduce.put()
        
            checkMaster = Master.all()
            checkMaster.filter('keyWord =', cle)
            if checkMaster.count() > 0 :
                master = checkMaster.get()
                master.count = master.count + dataDict[cle]
            else :
                master = Master(keyWord = cle, count=dataDict[cle])
            master.put()
        
        #pass # j'ai pas d'idée quoi initialiser pôur l'instant
    
    def tearDown(self):
        '''This method is run AFTER EACH test.
        So we could clean the database after each test.'''
        deleteData()
        #pass # j'ai pas d'idée quoi vider pour l'instant
    
    def testGetArticle(self):
        '''Adds articles and test the getArticle() search.'''
        result = getArticle(self.nameArticle)
        self.assertEquals(self.nameArticle,result.name)
        
    def testGetAuthorsByWords(self):
        '''Check if the good author is returned'''
        words = "tom"
        results = getAuthorsByWords(words)
        self.assertEquals(self.nameAuthor,results[0].name)
