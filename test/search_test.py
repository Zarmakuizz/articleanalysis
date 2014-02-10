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
    
    def setUp(self):
        '''This method is run BEFORE EACH test.
        So we could initialize the database here.'''
        
        text = "Voici le texte : La mère du maire est dans la mer; Le vers dans le verre vert; j'ai mon thé sur la table; La mer est bleu"
        
        savePdfInDB(nameArticle, nameAuthor, text)
        
        #pass # j'ai pas d'idée quoi initialiser pôur l'instant
    
    def tearDown(self):
        '''This method is run AFTER EACH test.
        So we could clean the database after each test.'''
        deleteData()
        #pass # j'ai pas d'idée quoi vider pour l'instant
        
    def savePdfInDB(nameArticle, nameAuthor, text):
        article = Article(name = self.nameArticle)
        article.put()
        
        author = Author(name = self.nameAuthor)
        author.put()
        artiAuth = ArtiAuth(keyAuthor= author, keyArticle=article)
        artiAuth.put()
        
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
    
    def testGetArticle(self):
        '''Test the getArticle() search.'''
        result = getArticle(self.nameArticle)
        self.assertEquals(self.nameArticle,result.name)
        
    def testGetAuthorsByWords(self):
        '''Test the getAuthorsByWords() search'''
        results = getAuthorsByWords(self.nameAuthor)
        self.assertEquals(self.nameAuthor,results[0].name)
    
    def testGetWordsMostFreq(self):
        '''Test that the words are ordered from most to few count
        and that the forbidden words are not taken into account.'''
        results = getWordsMostFreq(99) # high value just because
        for i in range(0,len(results)):
            if i==0:
                self.assertTrue(results[i].count >= results[i-1].count)
            else:
                self.assertTrue(results[i].count <= results[i-1].count)
            self.assertTrue(results[i].keyWord != "what") # one forbidden word
    
    def testGetWordsMostFreqByDoc(self):
        '''Test that the words are ordered from most to few count
        and that the forbidden words are not taken into account.'''
        results = getWordsMostFreqByDoc(self.nameArticle,99) # high value just because
        for i in range(0,len(results)):
            if i==0:
                self.assertTrue(results[i].count >= results[i-1].count)
            else:
                self.assertTrue(results[i].count <= results[i-1].count)
            self.assertTrue(results[i].keyWord != "what") # one forbidden word

    def testGetPaperByWords(self):
        '''Test that the docs returns are
        '''
        newNameArticle = "nouveau article"
        savePdfInDB(newNameArticle, "blabla", 
                    "Je suis un texte qui va être vérifié!\n" +
                    "Car le but est d'analyser un texte selon le nombre d'occurence ")
        words = ['mer', 'texte', 'occurence']
        results = getPaperByWords(words, 3)
        nbOccurNewArticle  = [0, 2, 1]
        nbOccurOldArticle = [2, 1, 0]
        self.assertTrue(results[newNameArticle], nbOccurNewArticle)
        self.assertTrue(results[nameArticle], nbOccurOldArticle)
