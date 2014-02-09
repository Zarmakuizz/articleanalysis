from model.resource import Master, MapReduce, Article, Author, ArtiAuth, ArtCitedBib
from controller.mapReduce import mapper, reducer
from controller.pdfProcess import convert_pdf_to_txt
import re

def deleteData():
    '''
        Delete all the data
    '''
    masters = Master.all()
    for master in masters:
        Master.delete(master)
        
    mapReduces = MapReduce.all()
    for mapReduce in mapReduces:
        MapReduce.delete(mapReduce)

    articles = Article.all()
    for article in articles:
        Article.delete(article)
        
    authors = Author.all()
    for author in authors:
        Author.delete(author)
        
    artCitedBibs = ArtCitedBib.all()
    for artCitedBib in artCitedBibs:
        ArtCitedBib.delete(artCitedBib)
        
def saveMapReduce(namefic):
    '''
        Converted the pdf file in text
        Do the mapper and reduce in the text
        Get the references cited in the article
        Save data Author, Article, ArtCitedBib, MapReduce, Master
        :param namefic : the name file
    '''
    #save_pdf(namefic)
    fic = convert_pdf_to_txt(namefic)
    
    dataDict = mapper(fic)
    dataDict = reducer(dataDict)
    
    lines = re.split( r'\n', fic)
    
    author = Author (name = lines[4])
    author.put()
    
    article = Article(name = lines[0],file = namefic)
    article.put()
    
    getReferences(fic, article)
    
    artiAuth = ArtiAuth (keyAuthor = author, keyArticle = article)
    artiAuth.put()
    
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
            
def getReferences (fic, articlePrinc):
    '''
        Get the references of the article
    '''
    fic = fic.replace('\n', ' ') 
    objFic = re.match( r'(.*)REFERENCES(.*)', fic)
    if objFic :
        references = re.split('(\[[0-9]+\])', objFic.group(2))
        for oneRef in references:
            sepAuthName = oneRef.split(',')
            authorsArt = []
            for l in sepAuthName:
                matchAuth = re.match( r' ([A-Z]\..*)', l) 
                if matchAuth :
                    author = re.sub( r'[^a-zA-Z\s\.]', "", matchAuth.group(1))
                    authorsArt.append(author)
                else :
                    derMatchAuth = re.match( r' and (.*)', l)
                    if derMatchAuth :
                        author = re.sub( r'[^a-zA-Z\s\.]', "", derMatchAuth.group(1))
                        authorsArt.append(author)
                    else :
                        nameMatch = re.match( r'(.*)\..*', l)
                        if nameMatch:
                            nameArt = nameMatch.group(1)
                        else:
                            nameArt = l
                        nameArt = re.sub( r'[^a-zA-Z\s]', "", nameArt)
                        if nameArt == "" or len(authorsArt) == 0:
                            break
                        articleCitedBib = ArtCitedBib.all()
                        articleCitedBib.filter('nameArticle =', nameArt)
                        if articleCitedBib.count() > 0:
                            artCitedBib = articleCitedBib.get()
                            artCitedBib.count = artCitedBib.count + 1
                        else :    
                            artCitedBib = ArtCitedBib(keyArticle=articlePrinc, nameArticle=nameArt, authors=authorsArt, count=1)
                        artCitedBib.put()
                        break
    else :
        print 'pas de references'