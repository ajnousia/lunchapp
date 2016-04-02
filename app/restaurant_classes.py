from helper_functions import get_json

class Restaurants(object):

    def __init__(self):
        self.restaurants = []

    def add_restaurant(self, restaurant):
        self.restaurants.append(restaurant)

    def remove_restaurant(self, restaurant):
        if restaurant in self.restaurants:
            self.restaurants.remove(restaurant)

    def number_of_restaurants(self):
        return len(self.restaurants)

    def get_restaurant_by_name(self, name):
        for restaurant in self.restaurants:
            if restaurant.name == name:
                return restaurant
        raise Exception("Restaurant name not found.")

    def get_restaurant_names(self):
        names = []
        for restaurant in self.restaurants:
            names.append(restaurant.name)
        return names


class Restaurant(object):

    def __init__(self, name, address_object):
        self.name = name
        self.address = address_object
        self.menu_list = []
        if self.address != None:
            self.location = self.geocode_address()

    def get_menu_list(self):
        return self.menu_list

    def add_day_menu(self, day_menu):
        self.menu_list.append(day_menu)

    def get_menu_for_date(self, date):
        pass

    def geocode_address(self):
        json_string = get_json(self.build_nominatim_url_query_string())
        return Location(json_string[0]["lat"], json_string[0]["lon"])

    def build_nominatim_url_query_string(self):
        return 'http://nominatim.openstreetmap.org/search?' \
            'q={0}%20{1}%20{2}[restaurant]&format=json&countrycodes=fi&bounded=1&polygon=0&' \
            'limit=1'.format(self.address.house_number, self.address.street, self.address.city)


class DayMenu(object):

    def __init__(self, date_object):
        self.date = date_object
        self.courses = []

    def add_course(self, course):
        self.courses.append(course)


class Course(object):

    def __init__(self, price):
        self.components = []
        self.price = price

    def add_component(self, component):
        self.components.append(component)

    def get_course(self):
        pass


class Component(object):

    def __init__(self, name, properties = None):
        self.name = name
        self.properties = properties # esim. "V, GL"

    def get_properties_as_string(self):
        if self.properties == None:
            return ''
        else:
            return ' '.join(self.properties)


class Address:

    def __init__(self, street, house_number, postal_code, city):
        self.street = street
        self.house_number = house_number
        self.postal_code = postal_code
        self.city = city


class Location:

    def __init__(self, lat, lon):
        self.lat = float(lat)
        self.lon = float(lon)

    def get_geojson(self):
        geo_json = [ {"type": "Feature",
                      "geometry": {
                                   "type": "Point",
                                   "coordinates": [self.lon, self.lat]
                                   }
                      }
                    ]
        return geo_json
