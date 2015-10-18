import lunchapp
from google.appengine.ext import ndb

# def get_data():
#     data = memcache.get('key')
#     if data is not None:
#         return data
#     else:
#         data = self.query_for_data()
#         memcache.add('key', data, 60)
#         return data
#
# def get_restaurants(self, datastore):
#     restaurants = memcache.get('{}:restaurants'.format(datastore))
#     if restaurants is None:
#         restaurants = self.render_restaurants(datastore)
#         if not memcache.add('{}:greetings'.format(datastore),
#                             restaurants):
#             logging.error('Memcache set failed.')
#     return restaurants
#
# def render_restaurants(self, datastore):
#     restaurants = ndb.gql('SELECT * '
#                         'FROM RestaurantObj '
#                         'WHERE ANCESTOR IS :1 ',
#                         restaurant_data_key(datastore))
#     output = cStringIO.StringIO()
#     for restaurant in restaurants:
#         if greeting.author:
#             output.write('<b>{}</b> wrote:'.format(greeting.author))
#         else:
#             output.write('An anonymous person wrote:')
#         output.write('<blockquote>{}</blockquote>'.format(
#             cgi.escape(greeting.content)))
#     return output.getvalue()

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

class UserPrefs(ndb.Model):
    user = ndb.UserProperty()
    restaurants = ndb.StructuredProperty(RestaurantEntity, repeated=True)
