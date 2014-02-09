'''URL dispatcher.
Sets up the mapping between URIs and controller modules.
Author: (c)2009-14 Peter Sander'''
import webapp2

# sets up the URI path to encode entity and method information
from controller.crud_controller import CRUD
from controller.index_controller import INDEX

# sets up the URI path to encode entity and method information
application = webapp2.WSGIApplication([
    ('^/mapReduce', CRUD), # Create
    ('^/$',INDEX), # Index, so that Guy could try things
    ('^/css/[a-zA-Z0-9-_.]+$',INDEX), # css file
    ('^/img/[a-zA-Z0-9-_.]+$',INDEX), # images
    ('^/download/[a-zA-Z0-9-_.]+$',INDEX), # pdf
    ('^/\w+/$',INDEX), # articles, authors, stats, upload, about
    ('^/article/\w+$',INDEX), # article
    ('^/author/[^/]+$',INDEX), # author
    ],debug=True)
