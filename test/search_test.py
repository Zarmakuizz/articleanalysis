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
    
    nameArticle = "Article sur les saucisses"
    nameAuthor = "Tomtom"
    
    def setUp(self):
        '''This method is run BEFORE EACH test.
        So we could initialize the database here.'''
        
        article = Article(name = nameArticle)
        article.put()
        
        author = Author(name = nameAuthor)
        author.put()
        artiAuth = ArtiAuth(keyAuthor= author, keyArticle=article)
        artiAuth.put()
        
        text = "La mère du maire est dans la mer; Le vers dans le verre est vert; j'ai mon thé sur la table;"
        dataDict = mapper(text)
        dataDict = reduce(dataDict)
        
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
        #nameArticle = "Article sur les saucisses"
        #Article(name = nameArticle).put()
        result = getArticle(nameArticle)
        self.assertEquals(nameArticle,result.name)
        
    def testgetAuthorsByWords(self):
        '''Check if the good author is return'''
        words = "vers, verre"
        result = getPaperByWords(words, 1)
        self.assertEquals(result[0], author)
