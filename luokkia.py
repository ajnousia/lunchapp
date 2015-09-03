import datetime

class Restaurants(object):
    
    def __init__(self):
        self.restaurants = []
        
    def add_restaurant(self, restaurant):
        self.restaurants.append(restaurant)
        
    def number_of_restaurants(self):
        return len(self.restaurants)
        

class Restaurant(object):
    
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.menu_list = []
        
    def get_menu_list(self):
        return self.menu_list
    
    def add_menu_day(self, day_menu):
        self.menu_list.append(day_menu)
    
    def get_menu_for_date(self):
        pass
    
    def get_coordinates(self):
        pass
    

class Week_menu(object):
    
    def __init__(self):
        self.week_menu = []
        
    def add_menu_day(self, day_menu):
        self.week_menu.append(day_menu)
        
        
class Day_menu(object):
    
    def __init__(self, date_object):
        self.date = date_object
        self.courses = []
        
    def add_course(self, course):
        self.courses.append(course)
        
        
class Course(object):
    
    def __init__(self, name, price, properties = None):
        self.name = name    
        self.properties = properties # esim. "V, GL"
        self.price = price
    
    