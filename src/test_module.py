import datetime
import json
import urllib2
from HTMLParser import HTMLParser

def get_json(url):
    request = urllib2.urlopen(url)
    return json.loads(request.read())

def parse_atomitie5_json(start_date):
    weeks_menus = []
    for i in range(0,7):
        date = start_date + datetime.timedelta(i)
        json_string = get_json('http://www.sodexo.fi/ruokalistat/output/daily_json/9/{0}/{1}/{2}/fi'.format(str(date.year), str(date.strftime('%m')), str(date.strftime('%d'))))
        new_menu = DayMenu(date)
        for lunch in json_string["courses"]:
            new_course = Course(lunch["price"])
            try:
                types = lunch["properties"].split(',')
            except KeyError:
                types = None
            
            new_course.add_component(Component(lunch["title_fi"], types))
        new_menu.add_course(new_course)
        weeks_menus.append(new_menu)
    return weeks_menus

def parse_bolero_json(start_date):
    json_string = get_json('http://www.amica.fi/modules/json/json/Index?costNumber=3121&firstDay={0}&language=fi'.format(datetime.date.isoformat(start_date)))
    menus = json_string["MenusForDays"]
    weeks_menus = []
    for index,menu in enumerate(menus):
        new_menu = DayMenu(start_date + datetime.timedelta(index))
        for lunch in menu["SetMenus"]:
            new_course = Course(lunch["Price"])
            for component in lunch["Components"]:
                name = component[0:component.find('(')-1]
                types = component[component.find('(')+1:-1].strip().split(',')
                new_course.add_component(Component(name, types))
            new_menu.add_course(new_course)
        weeks_menus.append(new_menu)
    return weeks_menus

class Restaurants(object):
    
    def __init__(self):
        self.restaurants = []
               
    def add_restaurant(self, restaurant):
        self.restaurants.append(restaurant)
        
    def number_of_restaurants(self):
        return len(self.restaurants)
    
    def get_restaurant_by_name(self):
        pass


class Restaurant(object):
    
    def __init__(self, name, address_object):
        self.name = name
        self.address = address_object
        self.menu_list = []
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
    
    
class PicanteHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.day = 0
        self.food_count = 0
        self.weeks_menu = []
        self.date = []
        self.lunch_list_found = 0
        self.date_found = 0
        self.food_found = 0
        self.price_found = 0

    def handle_starttag(self, tag, attributes):
        if tag == 'ul' and ('class', 'lunch-list-options') in attributes:
            self.lunch_list_found += 1
            self.day += 1
            if self.day > len(self.weeks_menu):
                self.weeks_menu.append(DayMenu(self.date[self.day-1]))
            
        if tag == 'h3' and ('class', 'lunch-list-date') in attributes:
            self.date_found += 1
                
        if self.lunch_list_found == 1:
            if tag == 'p':
                self.food_found += 1
            if tag == 'span':
                self.price_found += 1

    def handle_endtag(self, tag):
        if tag == 'ul' and self.lunch_list_found == 1 and self.food_found == 0 and self.price_found == 0:
            self.lunch_list_found -= 1
            self.food_count = 0
        
        if tag == 'h3' and self.date_found == 1:
            self.date_found -= 1
            #DayMenu(self.date[self.day-1])
            
        if tag == 'p' and self.food_found == 1 and self.price_found == 0:
            self.food_found -= 1

        if tag == 'span' and self.price_found == 1:
            self.price_found -= 1
            

    def handle_data(self, data):
        if self.date_found == 1:
            date_string = data.split(' ')[0]
            self.date.append(datetime.date(datetime.date.today().year,
                                           int(date_string.split('.')[1]),
                                           int(date_string.split('.')[0]))
                             )
        
        if self.food_found == 1 and self.price_found == 0:
            self.food_count += 1
            modified_data = data.strip(' \t\n\r')
            types_string = modified_data[modified_data.rfind(' '):].strip()
            
            if len(types_string) > 6:
                types_string = ""
            
            name = modified_data.replace(types_string, '').strip()
            types = types_string.split(',')
            
            if len(types_string) == 0:
                types = None
            
            new_course = Course(price=None)
            new_course.add_component(Component(name, types))    
            self.weeks_menu[self.day-1].add_course(new_course)

        if self.price_found == 1:
            self.weeks_menu[self.day-1].courses[self.food_count-1].price = data.split(' ')[0]
            

def parse_picante_html():
    parser = PicanteHTMLParser()
    url = 'http://www.taitotalo.com/ravintolat/lounaslistat/picante-viikon-lounaslista/'
    parser.feed(urllib2.urlopen(url).read().decode('utf-8'))
    #print parser.weeks_menu[0].courses[0].components[0].name
    return parser.weeks_menu

today = datetime.date.today()
last_monday = today + datetime.timedelta(days=-today.weekday(), weeks=0)
restaurants = Restaurants()       

bolero = Restaurant("Bolero", Address("Atomitie", "2", "00370", "Helsinki"))
for menu in parse_bolero_json(last_monday):
    bolero.add_day_menu(menu)

atomitie5 = Restaurant("Atomitie 5", Address("Atomitie", "5", "00370", "Helsinki"))
for menu in parse_atomitie5_json(last_monday):
    atomitie5.add_day_menu(menu)

picante = Restaurant("Picante", Address("Valimotie", "8", "00380", "Helsinki"))
for menu in parse_picante_html():
    picante.add_day_menu(menu)

restaurants.add_restaurant(bolero)
restaurants.add_restaurant(atomitie5)
restaurants.add_restaurant(picante)
        


for restaurant in restaurants.restaurants:

    for course in restaurant.menu_list[0].courses:
        for component in course.components:
            print component.name, component.get_properties_as_string()

        print course.price
    
    for course in restaurant.menu_list[1].courses:
        for component in course.components:
            print component.name, component.get_properties_as_string()

        print course.price
    
    for course in restaurant.menu_list[2].courses:
        for component in course.components:
            print component.name, component.get_properties_as_string()

        print course.price
        
    for course in restaurant.menu_list[3].courses:
        for component in course.components:
            print component.name, component.get_properties_as_string()

        print course.price
        
    for course in restaurant.menu_list[4].courses:
        for component in course.components:
            print component.name, component.get_properties_as_string()

        print course.price
    

