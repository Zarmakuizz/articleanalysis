# -*- coding: utf-8 -*-

import webapp2
from controller.search import *

class Index:
    '''Manages the basic HTML structure.'''
    
    def __init__(self):
       pass
    
    def index(self):
        ''' Displays the page's index
        :returns: HTML content as text'''
        return self.html("Your website about articles and analysis",self.index_content())
    
    def articles(self):
        ''' Let you get to the page dedicated to articles
        :returns: HTML content as text'''
        return self.html("All the world's articles",self.articles_content())
    
    def articles_search(self,search):
        ''' Let you get to the page dedicated to a search onto articles
        :returns: HTML content as text'''
        return self.html("Your searched articles",self.articles_load(search))
    
    def article(self,article):
        '''Let you display an article
        :returns: HTML content as text'''
        return self.html("Yo article",self.article_data(article));
        
    def authors(self):
        ''' Let you get to the page dedicated to authors
        :returns: HTML content as text'''
        return self.html("All the world's authors",self.authors_content())
    
    def authors_search(self,search):
        ''' Let you get to the page dedicated to a search onto authors
        :returns: HTML content as text'''
        return self.html("Your searched authors",self.authors_load(search))
    
    def author(self,author):
        '''Let you display an author
        :returns: HTML content as text'''
        return self.html("Yo Otor",self.author_data(author));
    
    def stats(self):
        ''' Let you get to the page dedicated to stats
        :returns: HTML content as text'''
        return self.html("All the world's stats",self.stats_content())
            
    def upload(self):
        ''' Let you get to the page dedicated to uploading articles
        :returns: HTML content as text'''
        return self.html("Let's upload all the world's articles",self.upload_content())
        
    def about(self):
        ''' Let you get to the page dedicated to the website's references
        :returns: HTML content as text'''
        return self.html("About us",self.about_content())
        
    def html(self,title='',content=''):
        ''' Let you get to the page dedicated to the website's references
        :returns: HTML content as text'''
        return """<!DOCTYPE html>
<html>
    %s
    %s
</html>""" % (self.head(title), self.body(content))
    
    def head(self, title="TITRE", content=''):
        """Displays the page's <head> content.
        :returns: HTML content as text"""
        return """
    <head>
        
        <title>%s - Article statistics</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="Instant access to the greatest articles and metadata about them!">
        <link rel="stylesheet" type="text/css" href="/css/pure-min.css" />
        <link rel="stylesheet" type="text/css" href="/css/side-menu.css" />
        <link rel="stylesheet" type="text/css" href="/css/bonus.css" />
        <script src="/js/tagcanvas.min.js" type="text/javascript"></script>
     </head>""" %title
    
    def body(self, content=''):
        """Displays the page's <body> content. This is a template,
        the real content is managed by other methods.
        :returns: HTML content as text"""
        return """
    <body>
        <div id='layout'>
            %s
            <div id="main">
                %s
                <div class="content">
                    %s
                </div>
            </div>
        </div>
    </body>
        """ %(self.menu(),self.header(),self.content(content))
        
    def menu(self):
        """Displays the page's left menu.
        :returns: HTML content as text"""
        return """
    <a href="#menu" id="menuLink" class="menu-link">
        <!-- Hamburger icon --><span></span>
    </a>
    <div id="menu">
        <div class="pure-menu pure-menu-open">
            <a class="pure-menu-heading" href="/">ACCUEIL</a>

            <ul>
                <li><a href="/articles/">Articles</a></li>
                <li><a href="/authors/">Authors</a></li>
                <li class="pure-menu-heading"></li>
                <li><a href="/stats/">Stats</a></li>
                <li><a href="/upload/">Upload</a></li>
                <li><a href="/about/">About</a></li>
            </ul>
        </div>
    </div>
        """
    
    def header(self,title="Article Statistics",subtitle="All your data are belong to yours!"):
        """Display the page's header.
        :returns: HTML content as text"""
        return """
                <div class="header">
                    <h1>%s</h1>
                    <h2>%s</h2>
                </div>
        """%(title,subtitle)
    
    
    def content(self,content=''):
        """content's placeholder unless content argument is set.
        :param content: The real content to display.
        :returns: HTML content as text"""
        if(content != ''): return content
        else: return "<h2>What to do here…</h2>"
    
    # The real content starts here
    
    def index_content(self):
        """Display the home page's content.
        :returns: HTML content as text"""
        words = getWordsMostFreq(30)
        # Top charted words: the most popular keywords
        topcharted = ""
        for wo in words:
            topcharted += '<li><a href="/articles/?s='+str(wo.keyWord)+'" data-weight="'+str(wo.count-10)+'">'+str(wo.keyWord)+"</a></li>\n"
        return"""<h2 class="content-subhead">Search for an article…</h2>
                    <p class="pure-g">
                        <form class='pure-form' action="/articles/" method="get">
                            <input type="text" name="s" placeholder="Enter keywords here" class='pure-u-3-5'/>
                            <button type="submit" class="pure-button pure-button-primary pure-u-1-5">Search</button>
                        </form>
                    </p>

                    <h2 class="content-subhead">What you could do here</h2>
                    <p>
                        This place lets you review articles, you could also watch trends among articles, like:
                        <ul><li>Who is a popular writer</li>
                            <li>What are the buzz words</li>
                            <li>And so on!</li>
                        </ul>
                        Just take a look…
                    </p>
                    <div class='pure-g' id="myCanvasContainer">
                        <canvas width="600" height="300" id="myCanvas">
                            <p>If you see this text, you should jump to a fresh, updated browser, for example Firefox, Google Chrome, or Internet Explorer 10.</p>
                            <ul class="weighted" id="weightTags">
                                %s
                            </ul>
                        </canvas>
                         <script type="text/javascript">
                          window.onload = function() {
                              var options = {
                                  textColour: '#565656',
                                  weight: true,
                                  weightMode: "both",
                                  weightFrom: "data-weight",
                                  weightSizeMin: 16,
                                  weightSizeMax: 64
                              };
                              try {
                                TagCanvas.Start('myCanvas', '', options);
                              } catch(e) {
                                  // something went wrong, hide the canvas container
                                  document.getElementById('myCanvasContainer').style.display = 'none';
                              }
                          };
                         </script>
                    </div>""" %(topcharted)
    
    def articles_content(self):
        """Display the article's "home" page located at [url]/articles.
        :returns: HTML content as text"""
        # Top charted words: the most popular keywords
        words = getWordsMostFreq(10)
        topcharted = ""
        for wo in words:
            topcharted += '<tr><td>'+str(wo.keyWord)+"</td><td>"+str(wo.count)+"</td></tr>\n"
        articles = getArtMostFreqCited(10)
        topCited = ""
        for art in articles:
            topCited += '<tr><td>'+str(art.nameArticle)+'</td><td>'+str(art.count)+'</td></tr>\n'
        return"""<h2 class="content-subhead">Search for an article…</h2>
                    <p class="pure-g">
                        <form class='pure-form' action="/articles/" method="get">
                            <input type="text" name="s" placeholder="Enter keywords here" class='pure-u-3-5'/>
                            <button type="submit" class="pure-button pure-button-primary pure-u-1-5">Search</button>
                        </form>
                    </p>

                    <h2 class="content-subhead">Take a look at</h2>
                    <div class='pure-g'>
                        <table class='pure-u  pure-table pure-table-horizontal pure-table-striped'>
                            <thead><tr><th>Top-charted themes</th><th>Count</th></tr></thead>
                            <tbody>
                                %s
                            </tbody>
                        </table>
                        <div class='pure-u-1-24'></div>
                        <table class='pure-u-1-2  pure-table pure-table-horizontal pure-table-striped'>
                            <thead><tr><th>Most cited articles</th><th>Count</th></tr></thead>
                            <tbody>
                                %s
                            </tbody>
                        </table>
                    </div>""" %(topcharted,topCited)
    
    def authors_content(self):
        """Display the author's "home" page located at [url]/authors.
        :returns: HTML content as text"""
        authors = listAuthor()
        topAuthors = ""
        for au in authors:
            topAuthors += '<tr><td><a href="/author/'+str(au)+'">'+str(au)+'</a></td></tr>\n'
        return"""<h2 class="content-subhead">Search for an author…</h2>
                    <p class="pure-g">
                        <form class='pure-form' action="/authors/" method="get">
                            <input type="text" name="s" placeholder="Enter author name here" class='pure-u-3-5'/>
                            <button type="submit" class="pure-button pure-button-primary pure-u-1-5">Search</button>
                        </form>
                    </p>

                    <h2 class="content-subhead">Take a look at</h2>
                    <div class='pure-g'>
                        <table class='pure-u  pure-table pure-table-horizontal pure-table-striped'>
                            <thead><tr><th>Our last authors</th></tr></thead>
                            <tbody>
                                %s
                            </tbody>
                        </table>
                        <div class='pure-u-1-24'></div>
                    </div>""" %(topAuthors)
    
    def stats_content(self):
        """Display the stats page located at [url]/stats .
        :returns: HTML content as text"""
        words = getWordsMostFreq(10)
        
        # Top charted words: the most popular keywords
        topcharted = ""
        for wo in words:
            topcharted += '<tr><td>'+str(wo.keyWord)+"</td><td>"+str(wo.count)+"</td></tr>\n"
        # TODO other top10/list of last
        authors = listAuthor()
        topAuthors = ""
        for auth in authors:
            topAuthors += '<tr><td><a href="/author/'+str(auth)+'">'+str(auth)+'</a></td></tr>\n'
        articles = getArtMostFreqCited(10)
        topCited = ""
        for art in articles:
            topCited += '<tr><td>'+str(art.nameArticle)+'</td><td>'+str(', '.join(art.authors))+'</td><td>'+str(art.count)+'</td></tr>\n'
        return"""
                    <h2 class="content-subhead">Watch the hottest, latest statistics</h2>
                    <div class='pure-g'>
                        <table class='pure-u pure-table pure-table-bordered pure-table-horizontal pure-table-striped'>
                            <thead><tr><th>Top-charted themes</th><th>Count</th></tr></thead>
                            <tbody>
                                %s
                            </tbody>
                        </table>
                        <div class='pure-u-1-24'></div>
                        <table class='pure-u  pure-table pure-table-horizontal pure-table-striped'>
                            <thead><tr><th>Our last authors</th></tr></thead>
                            <tbody>
                                %s
                            </tbody>
                        </table>
                    </div>
                    <div class'pure-g'>
                        <table class='pure-u  pure-table pure-table-horizontal pure-table-striped'>
                            <thead><tr><th>Most cited articles</th><th>Author</th><th>Count</th></tr></thead>
                            <tbody>
                                %s
                            </tbody>
                        </table>
                    </div>""" %(topcharted,topAuthors,topCited)
    
    def upload_content(self):
        """Display the upload page located at [url]/upload.
        :returns: HTML content as text."""
        # TODO manage upload.
        # sadly writing is not allowed on GAE.
        # Are we supposed to store into RAM every article?
        return"""<h2 class="content-subhead">Upload a new article…</h2>
                 <h2 style='border:4px solid red;border-radius: 4px;padding:1px;text-align:center;background-color:yellow;color:black;'>Warning, THIS PAGE DOES NOT WORK!!</h2>
                 <h3>Here you could feed some articles to that little buddy for great justice!</h3>
                    <p class="pure-g">
                        <form class='pure-form pure-form-aligned'>
                            <fieldset>
                                <div class="pure-control-group">
                                    <label for="file">Upload a file: </label>
                                    <input id="file" type="file" placeholder="Choose a file" />
                                </div>
                                <!-- <div class="pure-control-group">
                                    <label for="author">Add author's name': </label>
                                    <input id="author" type="text" placeholder="Give us the author" />
                                </div> -->
                            </fieldset>
                            <button type="submit" class="pure-button pure-button-primary">UPLOAD</button>
                        </form>
                    </p>""" 
    
    def about_content(self):
        """Display the About page located at [url]/about.
        :returns: HTML content as text."""
        return"""<h2 class="content-subhead">About this website</h2>
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam turpis nulla, posuere a tortor et, ullamcorper ultrices nunc. Nunc non dolor hendrerit, hendrerit lorem eget, laoreet tortor. Interdum et malesuada fames ac ante ipsum primis in faucibus. Aenean et tristique turpis. Proin lacus quam, tempor quis tincidunt sit amet, consequat at mauris. Nam quis eleifend felis, in fringilla ligula. In at ante dictum, tristique ipsum eu, tristique ipsum. Nullam blandit tempor ligula at iaculis. In non gravida ipsum. Aliquam sed augue quis neque consectetur tristique. Ut consectetur dui sit amet justo lacinia blandit. Suspendisse felis quam, lacinia nec tortor a, pulvinar aliquam dui. Suspendisse at dapibus sapien. Sed velit diam, tempor quis mi at, rhoncus elementum sem.</p>
                    <p>Etiam id laoreet tellus. Vestibulum eget condimentum turpis. Nunc vitae augue vel mi cursus semper. Mauris vel ligula bibendum, euismod turpis non, convallis urna. Aenean eu malesuada nisl. Nullam in mollis sem, quis consectetur nunc. Vivamus vitae lacinia metus. Sed gravida, nibh vitae congue porttitor, ipsum neque aliquam sapien, at facilisis ipsum dui eu est. Praesent egestas imperdiet sem, ut pretium risus varius in. Suspendisse non metus imperdiet, bibendum elit vel, rutrum nulla. In ullamcorper suscipit purus, non malesuada risus ultrices eu. Cras sodales, neque a scelerisque egestas, arcu purus rutrum lacus, ac suscipit ante ante sit amet lectus.</p>
                    <p>Proin bibendum, nunc sit amet bibendum ornare, nulla metus aliquet metus, nec molestie odio dolor et massa. Nulla sed mauris leo. Ut pulvinar odio libero, eu feugiat nisl aliquet vitae. Nunc leo augue, gravida at odio tincidunt, dapibus placerat augue. Morbi auctor at odio nec vestibulum. Aenean auctor magna erat, sed rhoncus lorem iaculis ut. Aliquam sit amet blandit ipsum. Cras consectetur sed sem et hendrerit. Sed congue a erat vitae lobortis.</p>""" 
    
    def articles_load(self,search=''):
        """Display an article search's results at /articles/?s=search
        :param search: the searched words as a list of strings
        :returns: HTML content as text."""
        # TODO check
        searchThis = search.split(' ')
        results = getPaperByWords(searchThis, 10)
        chunks = results.items()
        res = ""
        for i in range(0,len(chunks)):
            res += self.article_loading(chunks[i],searchThis)
        return """<h2 class="content-subhead">Search for an article…</h2>
                    <p class="pure-g">
                        <form class='pure-form' action="/articles/" method="get">
                            <input type="text" name="s" value="%s" placeholder="Enter keywords here" class='pure-u-3-5'/>
                            <button type="submit" class="pure-button pure-button-primary pure-u-1-5">Search</button>
                        </form>
                    </p>
                    <h2 class="content-subhead">Okay, here is what we found</h2>
                    %s
        """%(str(search),res)
                    
    
    def article_loading(self,article,search):
        """Generates the code for a given Article objet to display
        as the search's result. Also show the occurence of each searched word.
        This is a shortened display of said article.
        :param article: an element from the model
        :param search: the searched words as a list of strings
        :returns: HTML content as text"""
        occurences = ''
        logging.info("MERGUEZ : "+str(article))
        logging.info("CHIPOLALA : "+str(search))
        for i in range(0,len(search)):
            occurences += '<tr><td>'+str(search[i])+' </td><td>: '+str(article[1][i])+' count</td></tr>'
        
        return """
        <div class='pure-u-7-24' style='text-align:center;'>
            <a href="/article/%s">
                <div class='searched'>
                    <h4>%s</h4>
                    <img src='/img/pdf.svg' style='width:60px;height:auto;' alt='' />
                    <table class='pure-u pure-table pure-table-horizontal pure-table-striped'>
                        <tbody>
                            %s
                        </tbody>
                    </table>
                </div>
            </a>
        </div>"""%(str(article[0]),str(article[0]),occurences)
    
    def authors_load(self,search=''):
        """Display an author's search result at /authors/?s=search
        :param search: Text to search an author.
        :returns: HTML content as text"""
        authors = getAuthorsByWords(search)
        load = ''
        for a in authors:
            logging.info(a)
            load += self.author_loading(a)
        return """<h2 class="content-subhead">Search for an author…</h2>
                    <p class="pure-g">
                        <form class='pure-form' action="/authors/" method="get">
                            <input type="text" name="s" value="%s" placeholder="Enter author name here" class='pure-u-3-5'/>
                            <button type="submit" class="pure-button pure-button-primary pure-u-1-5">Search</button>
                        </form>
                    </p>
                    <h2 class="content-subhead">Okay, here is what we found</h2>
                    <div class='pure-g'>
                    %s
                    </div>
                    """%(str(search),load)
    
    def author_loading(self,author):
        """Generates the code for a given author name
        as the search result. This is a shortened view of said author.
        :param author: the author's name.
        :returns: HTML content as text."""
        return """
        <div class='pure-u-1-4' style='text-align:center;'>
            <a href="/author/%s">
                <div class='searched'>
                    <h4>%s</h4>
                    <img src='/img/author.png' alt='' />
                </div>
            </a>
        </div>
        """%(str(author.name),str(author.name))
    
    def article_data(self,name=''):
        """Displays an article located at [url]/article/text
        :param name: the article's name, which is used here as a primary key.
        :returns: HTML content as text."""
        logging.info('je cherche:'+repr(name))
        article = getArticle(name)
        words = getWordsMostFreqByDoc(name, 10)
        author = getAuthorByArticle(article)
        logging.info("SCHTROOMPFT"+str(len(words)))
        authorName = 'Unknown'
        if (author != None):
            authorName = author.name
        
        # if article ou words est nul TODO
        # return """<h2>404 : Article not found</h2>"""
        # else
        topcharted = ""
        for word in words:
            topcharted += '<tr><td>'+str(word.keyWord)+"</td><td>"+str(word.count)+"</td></tr>\n"
        citations = getArtCitedFromArt(name)
        # test for test
        
        logging.info("ONCHE ONCHE"+str(len(citations)))
        topCited = ""
        for ci in citations:
            topCited += '<tr><td>'+str(ci)+'</td></tr>'
        return """<h2>Article's name: %s</h2>
        <p>Author: %s</p>
        <p>You could <a href="/download/%s">download this article</a>.</p>
    <div class='pure-g'>
        <table class='pure-u pure-table pure-table-bordered pure-table-horizontal pure-table-striped'>
            <thead><tr><th>Themes</th><th>Count</th></tr></thead>
            <tbody>
                %s
            </tbody>
        </table>
        <div class='pure-u-1-24'></div>
        <table class='pure-u pure-table pure-table-horizontal pure-table-striped'>
            <thead><tr><th>This article references these articles:</th></tr></thead>
            <tbody>
                %s
            </tbody>
        </table>
    </div>
    """%(name,str(authorName),str(article.fileName),topcharted,topCited)
    
    def author_data(self,name=''):
        """Displays an author located at [url]/author/text
        :param name: The author's name so as we could get it from database
        :returns: HTML content as text"""
        # TODO get more of author's data?
        articles = getArticleByAuthor(name)
        topart = ""
        for art in articles:
            topart += '<tr><td><a href="/article/'+str(art)+'">'+str(art)+"</a></td></tr>\n"
        words = getWordsMostFreqByAuthor(name,10)
        
        # Top charted words: the most popular keywords
        topcharted = ""
        for word in words:
            topcharted += '<tr><td>'+str(word)+"</td><td>"+str(words[word])+"</td></tr>\n"
        return """<h2>Author's name: %s</h2>
        <div class='pure-g'>
        <table class='pure-u pure-table pure-table-bordered pure-table-horizontal pure-table-striped'>
            <thead><tr><th>Look at his articles</th></tr></thead>
            <tbody>
                %s
            </tbody>
        </table>
        <div class='pure-u-1-24'></div>
        <table class='pure-u  pure-table pure-table-horizontal pure-table-striped'>
            <thead><tr><th>This author's top words</th><th>Count</th></tr></thead>
            <tbody>
                %s
            </tbody>
        </table>
    </div>
        """%(name,topart,topcharted)
