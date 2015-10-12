import lunchapp
from google.appengine.ext import ndb

class RestaurantEntity(ndb.Model):
    name = ndb.StringProperty()

class UserEntity(ndb.Model):
    user = ndb.UserProperty()
    restaurants = ndb.StructuredProperty(RestaurantEntity, repeated=True)

# class CourseEntity(ndb.Model):
#   price = ndb.FloatProperty()
#   components = ndb.StructuredProperty(ComponentEntity, repeated=True)
#
# class DayMenuEntity(ndb.Model):
#   date = ndb.DateProperty()
#   courses = ndb.StructuredProperty(CourseEntity, repeated=True)
#
# class RestaurantEntity(ndb.Model):
#   name = ndb.StringProperty()
#   address = ndb.StringProperty()
#   menu_list = ndb.StructuredProperty(DayMenuEntity, repeated=True)
