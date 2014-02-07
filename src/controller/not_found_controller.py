import webapp2

class NotFoundController(webapp2.RequestHandler):
    def get(self):
        '''Responds with a whining page.'''
        self.response.write('''
<html><body>
<h1>Not found</h1>
Sorry d00d, I can't find %s
</body>
</html>''' % self.request.uri)
        