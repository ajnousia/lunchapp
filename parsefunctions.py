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
        new_lunch = []
        for lunch in json_string["courses"]:
            courses = []
            new_component = {}
            new_component["Food"] = lunch["title_fi"]
            new_component["Types"] = lunch["properties"].split(',')
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

