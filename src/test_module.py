import urllib2

from HTMLParser import HTMLParser

class PicanteHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.day = 0
        self.weeks_menu = []
        self.days_menu = {"Courses": [], "Price": []}
        self.component = {"Food": '', "Types": []}
        self.lunch_list_found = False
        self.food_found = False
        self.price_found = False

    def handle_starttag(self, tag, attributes):
        if tag == 'ul' and ('class', 'lunch-list-options') in attributes:
            self.lunch_list_found = True
            self.day += 1
        if self.lunch_list_found:
            if tag == 'p':
                self.food_found = True
            if tag == 'span':
                self.price_found = True

    def handle_endtag(self, tag):
        if tag == 'ul' and self.lunch_list_found:
            self.lunch_list_found = False
        if tag == 'p' and self.food_found:
            self.food_found = False
        if tag == 'span' and self.price_found:
            self.price_found = False

    def handle_data(self, data):
        if self.food_found and self.price_found == False:
            modified_data = data.rstrip(' \t\n\r')
            print modified_data
            types_string = modified_data[modified_data.rfind(' '):]
            print types_string
            food = modified_data.replace(types_string, '').strip()
            print food
            
            self.component["Food"] = food
            self.component["Types"] = types_string.split(',')
            
        if self.price_found:
            self.days_menu["Courses"].append(self.component)
            self.days_menu["Price"] = data.split(' ')[0]
        if self.day > len(self.weeks_menu):
            self.weeks_menu.append(self.days_menu)
            self.days_menu["Courses"] = []


def parse_picante_html():
    parser = PicanteHTMLParser()
    url = 'http://www.taitotalo.com/ravintolat/lounaslistat/picante-viikon-lounaslista/'
    parser.feed(urllib2.urlopen(url).read().decode('utf-8'))
    print parser.weeks_menu




parse_picante_html()
