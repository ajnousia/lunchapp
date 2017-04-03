import webapp2
import json
import model


class RestHandler(webapp2.RequestHandler):

    def dispatch(self):
        # time.sleep(1)
        super(RestHandler, self).dispatch()

    def SendJson(self, r):
        self.response.headers['content-type'] = 'text/plain'
        self.response.write(json.dumps(r))

    def SendString(self, string):
        self.response.headers['content-type'] = 'text/plain'
        self.response.write(string)


class QueryHandler(RestHandler):

    print "asdfasdfsdz"
    def get(self):
        # guests = model.AllGuests()
        # r = [AsDict(guest) for guest in guests]
        # self.SendJson(r)
        pass
