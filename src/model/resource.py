
from google.appengine.ext import db

class Author(db.Model):
    name = db.StringProperty(required=True)

class Article(db.Model):
#    keyArticle = db.IntegerProperty(required=True)
    name = db.StringProperty(required=True)
    fileName = db.StringProperty(required=True)
    
class ArtiAuth(db.Model):
    keyAuthor = db.ReferenceProperty(Author)
    keyArticle = db.ReferenceProperty(Article)
    
#class Word(db.Model):
#    keyWord = db.IntegerProperty(required=True)
    #word = db.StringProperty(required=True)
    
class MapReduce(db.Model):
    keyArticle = db.ReferenceProperty(Article)
    #keyWord = db.ReferenceProperty(Word)
    keyWord = db.StringProperty(required=True)
    count = db.IntegerProperty(required=True)

class Master(db.Model):
#    keyMaster = db.IntegerProperty(required=True)
    #keyWord = db.ReferenceProperty(Word)
    keyWord = db.StringProperty(required=True)
    count = db.IntegerProperty(required=True)

class ArtCitedBib(db.Model):
    keyArticle = db.ReferenceProperty(Article, collection_name="article_princ")
    #articleRef = db.ReferenceProperty(Article, collection_name="article_cited")
    nameArticle = db.StringProperty()
    authors = db.StringListProperty(required=True)
    count = db.IntegerProperty(required=True)  
    
#class ForbiddenWord(db.Model):
    #word = db.StringProperty(required=True)
