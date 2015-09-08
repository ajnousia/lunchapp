import datetime
import json
import urllib2
from HTMLParser import HTMLParser

from classes import *

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
            
            new_course = Course(price="")
            new_course.add_component(Component(name, types))    
            self.weeks_menu[self.day-1].add_course(new_course)

        if self.price_found == 1:
            self.weeks_menu[self.day-1].courses[self.food_count-1].price = data.split(' ')[0]

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