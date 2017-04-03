from google.appengine.ext import ndb


class FetchError(ndb.Model):
    was_error = ndb.BooleanProperty()
    # TODO update_counter = ndb.IntergerProperty()
    # TODO error_dates = ndb.DateProperty(repeated=True)
    task_queue_id = ndb.IntegerProperty()


class Restaurant(ndb.Model):
    name = ndb.StringProperty()
    address = ndb.StringProperty()


class Component(ndb.Model):
    name = ndb.StringProperty()
    properties = ndb.StringProperty()
    date = ndb.DateProperty()
    parent_restaurant = ndb.KeyProperty(kind=Restaurant)


class Course(ndb.Model):
    components = ndb.LocalStructuredProperty(Component, repeated=True)
    price = ndb.FloatProperty()
    date = ndb.DateProperty()
    parent_restaurant = ndb.KeyProperty(kind=Restaurant)


class DayMenu(ndb.Model):
    date = ndb.DateProperty()
    courses = ndb.LocalStructuredProperty(Course, repeated=True)
    parent_restaurant = ndb.KeyProperty(kind=Restaurant)
