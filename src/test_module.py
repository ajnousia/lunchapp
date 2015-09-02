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
    print parser.weeks_menu


parse_picante_html()
