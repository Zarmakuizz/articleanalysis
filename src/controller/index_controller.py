import webapp2
from model.resource import *
from view.index import Index
import logging
import os
import sys


class INDEX(webapp2.RequestHandler):
    '''Displays index for testing purposes.'''
    ind = Index()
    def get(self):
        # Watch the request to give the right resource
        self.request_path = self.request.path.split('/')[1:]
        logging.info("request_path : %s"%self.request_path)
        #logging.info("you wrote: %s"%self.request.get('s'))
        # GET css
        if len(self.request_path) > 0 and self.request_path[0] == 'css':
            '''Exploring content in src/'''
            try:
                f = open('css/%s' %self.request_path[1],'r')
                content = f.read()
                f.close()
                self.response.headers['Content-Type'] = 'text/css'
                self.response.out.write(content)
            except:
                self.response.headers['Content-Type'] = 'text/plain'
                self.response.out.write("404");
                print "unexpected error while loadin css:", sys.exc_info()
        # GET img
        elif len(self.request_path) > 0 and self.request_path[0] == 'img':
            '''Exploring content in src/'''
            try:
                f = open('img/%s' %self.request_path[1],'r')
                content = f.read()
                f.close()
                ext = self.request_path[-1].split('.')[1]
                if(ext == 'gif'):
                    self.response.headers['Content-Type'] = 'image/gif'
                elif(ext == 'jpg' or ext == 'jpeg'):
                    self.response.headers['Content-Type'] = 'image/jpeg'
                elif(ext == 'png'):
                    self.response.headers['Content-Type'] = 'image/png'
                elif(ext == 'svg'):
                    self.response.headers['Content-Type'] = 'image/svg+xml'
                elif(ext == 'ico'):
                    self.response.headers['Content-Type'] = 'image/vnd.microsoft.icon'
                elif(ext == 'tif' or ext == 'tiff'):
                    self.response.headers['Content-Type'] = 'image/tiff'
                self.response.out.write(content)
            except:
                self.response.headers['Content-Type'] = 'text/plain'
                self.response.out.write("404");
                print "unexpected error while loadin css:", sys.exc_info()
        #  GET /download/name
        elif len(self.request_path) > 0 and self.request_path[0] == 'download':
            print os.getcwd()
            self.response.headers['Content-Type'] = 'application/pdf'
            f = open('datasetpdf/%s.pdf'%self.request_path[1])
            content = f.read()
            self.response.out.write(content)
            f.close()
        #  GET /articles/
        elif len(self.request_path) > 0 and self.request_path[0] == 'articles' and self.request.get('s') == '':
            self.response.out.write(self.ind.articles())
        #  GET /articles/search
        elif len(self.request_path) > 0 and self.request_path[0] == 'articles' and self.request.get('s') != '':
            self.response.out.write(self.ind.articles_search(self.request.get('s')))
        # GET /article/xdxdxd
        elif len(self.request_path) > 0 and self.request_path[0] == 'article':
            self.response.out.write(self.ind.article(self.request_path[1].replace('%20',' ')))
        #  GET /authors/
        elif len(self.request_path) > 0 and self.request_path[0] == 'authors' and self.request.get('s') == '':
            self.response.out.write(self.ind.authors())
        #  GET /authors/search
        elif len(self.request_path) > 0 and self.request_path[0] == 'authors' and self.request.get('s') != '':
            self.response.out.write(self.ind.authors_search(self.request.get('s')))
        # GET /author/xdxdxd
        elif len(self.request_path) > 0 and self.request_path[0] == 'author':
            self.response.out.write(self.ind.author(self.request_path[1].replace('%20',' ')))
        #  GET /stats/
        elif len(self.request_path) > 0 and self.request_path[0] == 'stats':
            self.response.out.write(self.ind.stats())
        #  GET /upload/
        elif len(self.request_path) > 0 and self.request_path[0] == 'upload':
            self.response.out.write(self.ind.upload())
        #  GET /about/
        elif len(self.request_path) > 0 and self.request_path[0] == 'about':
            self.response.out.write(self.ind.about())
        # GET / (index)
        else:
            self.response.out.write(self.ind.index())
    
