import datetime
import json
import urllib2

from HTMLParser import HTMLParser

class PicanteHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.day = 0
        self.food_count = 0
        self.weeks_menu = []
        self.lunch_list_found = 0
        self.food_found = 0
        self.price_found = 0

    def handle_starttag(self, tag, attributes):
        if tag == 'ul' and ('class', 'lunch-list-options') in attributes:
            self.lunch_list_found += 1
            self.day += 1
            if self.day > len(self.weeks_menu):
                self.weeks_menu.append([])
                
        if self.lunch_list_found == 1:
            if tag == 'p':
                self.food_found += 1
            if tag == 'span':
                self.price_found += 1

    def handle_endtag(self, tag):
        if tag == 'ul' and self.lunch_list_found == 1 and self.food_found == 0 and self.price_found == 0:
            self.lunch_list_found -= 1
            self.food_count = 0
            
        if tag == 'p' and self.food_found == 1 and self.price_found == 0:
            self.food_found -= 1

        if tag == 'span' and self.price_found == 1:
            self.price_found -= 1
            

    def handle_data(self, data):
        if self.food_found == 1 and self.price_found == 0:
            self.food_count += 1
            modified_data = data.strip(' \t\n\r')
            types_string = modified_data[modified_data.rfind(' '):].strip()
            if len(types_string) > 6:
                types_string = ""
            food = modified_data.replace(types_string, '').strip()
            types = types_string.split(',')
            self.weeks_menu[self.day-1].append({"Courses": [{"Food": food, "Types": types}]})
            
        if self.price_found == 1:
            self.weeks_menu[self.day-1][self.food_count-1]["Price"]= data.split(' ')[0]

def parse_picante_html():
    parser = PicanteHTMLParser()
    url = 'http://www.taitotalo.com/ravintolat/lounaslistat/picante-viikon-lounaslista/'
    parser.feed(urllib2.urlopen(url).read().decode('utf-8'))
    return parser.weeks_menu
    
def get_json(url):
    request = urllib2.urlopen(url)
    return json.loads(request.read())

def parse_atomitie5_json(start_date):
    weeks_menus = []
    for i in range(0,7):
        date = start_date + datetime.timedelta(i)
        json_string = get_json('http://www.sodexo.fi/ruokalistat/output/daily_json/9/{0}/{1}/{2}/fi'.format(str(date.year), str(date.strftime('%m')), str(date.strftime('%d'))))
        new_lunch = []
        for lunch in json_string["courses"]:
            courses = []
            new_component = {}
            new_component["Food"] = lunch["title_fi"]
            try:
                new_component["Types"] = lunch["properties"].split(',')
            except KeyError:
                new_component["Types"] = []
            courses.append(new_component)
            new_lunch.append({"Courses": courses, "Price": lunch["price"]})
        weeks_menus.append(new_lunch)
    return weeks_menus

def parse_bolero_json(start_date):
    json_string = get_json('http://www.amica.fi/modules/json/json/Index?costNumber=3121&firstDay={0}&language=fi'.format(datetime.date.isoformat(start_date)))
    menus = json_string["MenusForDays"]
    weeks_menus = []
    for menu in menus:
        #date = datetime.datetime.strptime(menu["Date"],'%Y-%m-%dT%H:%M:%S')
        #menu_string += "<h1>{0}</h1>".format(date.strftime('%A %d.%m.'))
        new_lunch = []
        for lunch in menu["SetMenus"]:
            courses = []
            for component in lunch["Components"]:
                new_component = {}
                new_component["Food"] = component[0:component.find('(')-1]
                new_component["Types"] = component[component.find('(')+1:-1].strip().split(',')
                courses.append(new_component)
            new_lunch.append({"Courses": courses, "Price": lunch["Price"]})
        weeks_menus.append(new_lunch)
    return weeks_menus

def buildNominatimUrlQueryString(address):
    return 'http://nominatim.openstreetmap.org/search?' \
        'q={0}%20{1}%20{2}[restaurant]&format=json&countrycodes=fi&bounded=1&polygon=0&' \
        'limit=1'.format(address.house_number, address.street, address.city)

def geocodeAddress(address):
        json_string = get_json(buildNominatimUrlQueryString(address))
        return Location(json_string[0]["lat"], json_string[0]["lon"])
                
class Restaurant:
    def __init__(self, name, address, weeks_menus):
        self.name = name
        self.address = address
        self.weeks_menus = weeks_menus
        self.location = geocodeAddress(self.address)
    
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
        


today = datetime.date.today()
last_monday = today + datetime.timedelta(days=-today.weekday(), weeks=0)

restaurants = [Restaurant("Bolero", Address("Atomitie", "2", "00370", "Helsinki"), parse_bolero_json(last_monday)),
    Restaurant("Atomitie 5", Address("Atomitie", "5", "00370", "Helsinki"), parse_atomitie5_json(last_monday)),
    Restaurant("Picante", Address("Valimotie", "8", "00380", "Helsinki"), parse_picante_html())]

print restaurants[0].location.get_geojson()


    
    
    

