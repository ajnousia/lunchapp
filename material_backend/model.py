from google.appengine.ext import ndb


class Guest(ndb.Model):
    first = ndb.StringProperty()
    last = ndb.StringProperty()


def AllGuests():
    return Guest.query()


def UpdateGuest(id, first, last):
    guest = Guest(id=id, first=first, last=last)
    guest.put()
    return guest


def InsertGuest(first, last):
    guest = Guest(first=first, last=last)
    guest.put()
    return guest


def DeleteGuest(id):
    key = ndb.Key(Guest, id)
    key.delete()


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



# class Component(object):
#
#     def __init__(self, name, properties_list = None):
#         self.name = name
#         self.properties = properties_list # esim. "V, GL"
#
#     def get_properties_as_string(self):
#         if self.properties == None:
#             return ''
#         else:
#             return ' '.join(self.properties)
