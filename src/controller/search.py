from model.resource import Master, MapReduce, Article, Author, ArtiAuth, ArtCitedBib
from google.appengine.ext import db
from google.appengine.ext.db import ReferencePropertyResolveError
from collections import OrderedDict
import collections
import operator
import logging

def getArticle(articleName):
    '''Get article by its name.
    :returns: an Article object.'''
    query = db.Query(Article)
    query.filter('name =',articleName)
    return query.get()

def getAuthorsByWords(words):
    '''Get authors by their names.
    :param words: A string containing words.
    :returns: a list of Authors.'''
    dico = words.split(' ')
    query = Author.all()
    results = []
    for author in query:
        for w in dico:
            if (w in author.name):
                results.append(author)
    return list(set(results))
    
def getWordsMostFreq(wordNumber = 10):
    '''Get the most used words.
    @param wordNumber count. Default is 10.
    @return list of Master, which contains keyWord object and count'''
    master = db.Query(Master)
    master.order('-count')
    dataDict = []
    results = master.fetch(limit=wordNumber)
    for mast in results:
        dataDict.append(mast)
    return dataDict

def getWordsMostFreqByDoc(paper, wordNumber = 10):
    '''Get the most frequent words (and count) for a given article.
    :returns: a list of Master'''
    article = db.Query(Article)
    article.filter('name = ', paper)
    mapReduce = db.Query(MapReduce)
    mapReduce.filter('keyArticle = ', article.get())
    mapReduce.order('-count')
    dataDict = []
    results = mapReduce.fetch(limit=wordNumber)
    for mapRed in results:
        dataDict.append(mapRed)
    return dataDict

def getPaperByWords(words, docNumber = 3):
    '''Get a list of articles for a given request.
    :param words: list of words for the query.
    :param docNumber: count of max nomber of results to get.
    :returns: a list of strings being each Article's name.'''
    article = Article.all()
    data = collections.defaultdict(list)
    dataNbTotal = collections.defaultdict(list)
    for oneArticle in article:
        nbWord = 0
        nbOccur = []
        for strWord in words:
            mapReduce = MapReduce.all()
            mapReduce.filter('keyArticle = ', oneArticle)
            mapReduce.filter('keyWord =', strWord)
            if mapReduce.count() > 0:
                mR = mapReduce.get()
                nbWord += mR.count
                nbOccur.append(mR.count)
            else :
                nbOccur.append(0)
        data[oneArticle.name] = nbOccur
        dataNbTotal[oneArticle.name] = nbWord
        
    returnData = collections.defaultdict(list)
    OrderedDict(sorted(dataNbTotal.items(), key=lambda t: -t[1]))
    i = 0
    for cle in data.keys():
        if i < docNumber:
            i += 1
            returnData[cle] = data[cle]
        
    return returnData

def listAuthor():
    '''Returns a list of all authors.
    :returns: a list of strings being the authors's names '''
    authors = Author.all()
    data = []
    logging.info("scout authors")
    for aut in authors:
        logging.info(aut.name)
        if(aut.name == ' '):
            continue # Filtrer les auteurs vides
        data.append(aut.name)
    return data

def getArticleByAuthor (authorName, artNumber = 10) :
    '''Get the articles from a given author.
    :param authorName: a string which is the author's name.
    :param artNumber: the max count of results to give in the returned list.
    :returns: a list of string being the article's names.'''
    author = Author.all()
    author.filter('name = ', authorName)
    artiAuths = ArtiAuth.all()
    artiAuths.filter('keyAuthor = ', author.get())
    data = []
    results = artiAuths.fetch(limit=artNumber)
    for art in results:
        data.append(art.keyArticle.name)
    return data

def getAuthorByArticle(article):
    '''Give the author of asked article.
    :param article: an Article object.
    :returns: the associated Author object.'''
    query = db.Query(ArtiAuth)
    query.filter('keyArticle =',article)
    return query.get().keyAuthor

def getWordsMostFreqByAuthor(authorName, wordNumber = 10):
    ''' Get the keyword's stats for a given author.
    :param authorName: The asked author's name.
    :param wordNumber: the max number of results.
    :returns: a dictionnary of [word=>count]. example of use: data["lol"] = 42'''
    author = Author.all()
    author.filter('name = ', authorName)
    artiAuths = ArtiAuth.all()
    artiAuths.filter('keyAuthor = ', author.get())
    data = collections.defaultdict(list)
    for article in artiAuths :
        mapReduces = MapReduce.all()
        mapReduces.filter('keyArticle = ', article.keyArticle)
        for mR in mapReduces:
            try:
                if data[mR.keyWord]:
                    data[mR.keyWord] += mR.count
                else:
                    data[mR.keyWord] = mR.count
            except ReferencePropertyResolveError :
                print 'Pas de reference word'
    returnData = collections.defaultdict(list)  
    dico_trie = sorted(data.iteritems(), reverse=True, key=operator.itemgetter(1))
    #OrderedDict(sorted(data.items(), key=lambda t: -t[1]))
    #print data
    i = 0
    for cle in dico_trie:
        if i < wordNumber:
            i += 1
            returnData[cle[0]] = data[cle[0]]
        
    return returnData

def getArtCitedBiblio(wordNumber = 10):
    '''Give name all articles cited
    :param wordNumber: the max number of results.
    :return name of all the article cited, order by number of occurrence
    '''
    artCitedBib = ArtCitedBib.all()
    dataDict = []
    results = artCitedBib.fetch(limit=wordNumber)
    for artCited in results:
        dataDict.append(artCited.nameArticle)
    return dataDict

def getArtMostFreqCited(wordNumber = 10):
    '''Give article most frequently cited
    :param wordNumber: the max number of results.
    :returns: a list of object artCitedBib
    '''
    artCitedBib = ArtCitedBib.all()
    artCitedBib.order('-count')
    dataDict = []
    results = artCitedBib.fetch(limit=wordNumber)
    for artCited in results:
        dataDict.append(artCited)
    return dataDict

def getAuthorByArticleCited(nameArticle):
    #artCitedBib = ArtCitedBib.all()
    #artCitedBib.filter('nameArticle=', nameArticle)
    data = []
    #if artCitedBib.count() > 0:
        #data = artCitedBib.get().authors
    return data

def getArticleCited():
    '''Give all articles cited
    :returns: a list of object artCitedBib 
    '''
    artCitedBib = ArtCitedBib.all()
    data = []
    for artiCited in artCitedBib:
        data.append(artiCited)
    return data
