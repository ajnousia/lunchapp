import lunchapp
from google.appengine.ext import ndb

class PickledRestaurants(ndb.Model):
    pickled_restaurants = ndb.PickleProperty()
    week_number = ndb.IntegerProperty()


class Account(ndb.Model):
    user_email = ndb.StringProperty()
    user_id = ndb.StringProperty()


class Storage(ndb.Model):
    pickled_data = ndb.PickleProperty()


class RestaurantEntity(ndb.Model):
    name = ndb.StringProperty()


class UserPreferences(ndb.Model):
    user_id = ndb.StringProperty()
    restaurants = ndb.StringProperty(repeated=True)

class UserPrefs(ndb.Model):
    user = ndb.UserProperty()
    restaurants = ndb.StructuredProperty(RestaurantEntity, repeated=True)
