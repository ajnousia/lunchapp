from google.appengine.api import users
from google.appengine.ext import ndb

from data_store_classes import Account, UserPreferences
from restaurant_data_functions import get_restaurants_data

def get_user():
    user = users.get_current_user()
    parent_key = ndb.Key("Datastore", "Accounts")
    if user:
        accounts_query = Account.query(ancestor=parent_key).filter(Account.user_id == user.user_id())
        accounts = accounts_query.fetch(2)
        if len(accounts) > 1:
            print "Duplicate user. This shouldn't happen..."
        if len(accounts) > 0:
            return user
        else:
            account = Account(parent = parent_key, user_email = user.email(), user_id = user.user_id())
            account.put()
            return user
    else:
        return False

def create_dictionary_with_user_loginURL_and_logoutURL(handler):
    user = get_user()
    return_dict = {
        "user" : user,
        "login_url" : users.create_login_url(handler.request.uri),
        "logout_url" : users.create_logout_url(handler.request.uri)}
    return return_dict

def get_user_restaurant_names(user):
    restaurants = get_restaurants_data().restaurants
    user_id = user.user_id()
    if has_user_preferences(user_id):
        user_preferences = UserPreferences.query(UserPreferences.user_id == user_id).get()
        return user_preferences.restaurants
    else:
        restaurants_list = DEFAULT_RESTAURANT_NAMES
        user_preferences = UserPreferences(user_id = user_id, restaurants = restaurants_list)
        user_preferences.put()
        return restaurants_list

def has_user_preferences(user_id):
    if UserPreferences.query(UserPreferences.user_id == user_id).get() is None:
        return False
    else:
        return True
