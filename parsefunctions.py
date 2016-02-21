# -- coding: utf-8 --
import datetime
import json
import urllib2
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
from classes import *

def get_json(url):
    request = urllib2.urlopen(url)
    return json.loads(request.read())

def parse_picante_html():

    url = 'http://www.taitotalo.com/fi/ravintolat/lounaslistat/picante-viikon-lounaslista/'
    html_doc = urllib2.urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html_doc, 'html.parser')

    weeks_menus = []

    day = soup.find('h3', 'lunch-list-date')

    while day != None:
        date_string = day.string.split(' ')[0]
        new_menu = DayMenu(datetime.date(datetime.date.today().year,
                                           int(date_string.split('.')[1]),
                                           int(date_string.split('.')[0])))
        ul = day.findNext('ul', 'lunch-list-options')

        for elem in ul.contents:
            food_data = elem.contents[0]
            modified_data = food_data.strip(' \t\n\r')
            types_string = modified_data[modified_data.rfind(' '):].strip()

            if types_string.find(',') == -1 and len(types_string) > 3:
                types_string = ""
                types = None

            food_name = modified_data.replace(types_string, '').strip()
            types = types_string.split(',')

            try:
                price = elem.find('span').contents[0].split(' ')[0]
            except AttributeError:
                price = None

            new_course = Course(price)
            new_course.add_component(Component(food_name, types))
            new_menu.add_course(new_course)

        weeks_menus.append(new_menu)
        day = day.findNext('h3', 'lunch-list-date')
    return weeks_menus


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

def parse_sello_html(restaurant_name, start_date):
    week_number = start_date.isocalendar()[1]
    url = 'http://www.sello.fi/liikkeet/ravintolat-ja-kahvilat/{0}/lounaslista-viikko-{1}'.format(restaurant_name, week_number)
    html_doc = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html_doc, 'html.parser')

    weeks_menus = []
    days_list = soup.find('ul', 'lunch_list')
    day_count = 0
    while days_list != None:
        date = start_date + datetime.timedelta(day_count)
        new_menu = DayMenu(date)
        list_elem = days_list.find('li')
        while list_elem != None:
            try:
                food_data = list_elem.find('span', 'dish_title').contents[0]
                modified_data = food_data.strip(' \t\n\r').replace('\t', ' ')
                food_name = " ".join(modified_data.split())
                types = None
            except AttributeError:
                continue
            try:
                price = list_elem.find('span', 'dish_price').contents[0].split(' ')[0]
            except AttributeError:
                price = None

            if list_elem.has_attr('class') and 'last' in list_elem['class']:
                list_elem = None
            else:
                list_elem = list_elem.findNext('li')
            new_course = Course(price)
            new_course.add_component(Component(food_name, types))
            new_menu.add_course(new_course)
        weeks_menus.append(new_menu)
        days_list = days_list.findNext('ul', 'lunch_list')
        day_count += 1
        if day_count > 4:
            days_list = None
    return weeks_menus

def print_menus(restaurant):
    for menu in restaurant.menu_list:
        print menu.date
        for course in menu.courses:
            for component in course.components:
                print "name:", component.name
                print "types:", ",".join(component.properties)
            print "price:", course.price
