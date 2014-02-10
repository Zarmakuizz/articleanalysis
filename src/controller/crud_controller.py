import webapp2
from controller.storeData import *

from model.resource import *
from google.appengine.ext.db import ReferencePropertyResolveError
from controller.search import *
from controller.mapReduce import *
from controller.pdfProcess import *
import time

class CRUD(webapp2.RequestHandler):
    '''Manages datastore access.'''
    def get(self):

        #deleteData()

        saveMapReduce('11_coginfocom2013')
        saveMapReduce('13_coginfocom2013')
        #saveMapReduce('14_coginfocom2013')
        saveMapReduce('17_coginfocom2013')
        saveMapReduce('18_coginfocom2013')
        saveMapReduce('19_coginfocom2013')
        
        self.response.out.write('''
<html>
    <body>
        ''')
        
        data = None
        words = ['different', 'called']
        data = getPaperByWords(words, 3)
        self.response.out.write('''
        <h1>Document ou il y a le plus les mots different et called</h1>
        <table border=1>
            <tr>
                <td>Document</td>
                <td>Nombre different</td>
                <td>Nombre called</td>
            </tr>
        ''')
        for song in data:
            self.response.out.write('''
            <tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
            </tr>
            ''' % (song, data[song][0], data[song][1]))
        self.response.out.write('''
        </table>
        ''')
        
        self.response.out.write('''
    </body>
</html>
        ''')
        
    def post(self):
        '''Handles methods which change the datastore contents.
        Creates and updates entities via HTTP POST.'''
        request_path = self.request.path.split('/')[2:]
        self.redirect('/tuto')
