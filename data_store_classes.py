import lunchapp
from google.appengine.ext import ndb

class PickledRestaurants(ndb.Model):
    pickled_restaurants = ndb.PickleProperty()
    week_number = ndb.IntegerProperty()
    date = ndb.DateProperty(auto_now_add=True)


class Account(ndb.Model):
    user_email = ndb.StringProperty()
    user_id = ndb.StringProperty()


class UserPreferences(ndb.Model):
    user_id = ndb.StringProperty()
    restaurants = ndb.StringProperty(repeated=True)


class FetchError(ndb.Model):
    was_error = ndb.BooleanProperty()
    # TODO update_counter = ndb.IntergerProperty()
    # TODO error_dates = ndb.DateProperty(repeated=True)
