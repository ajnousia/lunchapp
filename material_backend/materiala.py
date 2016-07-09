import webapp2
import json
import model


def AsDict(guest):
    return {'id': guest.key.id(), 'first': guest.first, 'last': guest.last}


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

    def get(self):
        # guests = model.AllGuests()
        # r = [AsDict(guest) for guest in guests]
        # self.SendJson(r)
        pass
