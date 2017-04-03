import webapp2
import json
import model


class RestHandler(webapp2.RequestHandler):

    def dispatch(self):
        super(RestHandler, self).dispatch()

    def SendJson(self, r):
        self.response.headers['content-type'] = 'text/plain'
        self.response.write(json.dumps(r))

    def SendString(self, string):
        self.response.headers['content-type'] = 'text/plain'
        self.response.write(string)


class QueryHandler(RestHandler):

    def get(self):
        pass
