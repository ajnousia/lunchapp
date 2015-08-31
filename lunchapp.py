#!/usr/bin/env python
# -- coding: utf-8 --
import webapp2
import jinja2
import datetime

from parsefunctions import *
from HTMLParser import HTMLParser




HTML_HEADER = """<!DOCTYPE html>
<html>
<link rel="stylesheet" href="/bootstrap/css/bootstrap.css">
<link rel="stylesheet" href="/bootstrap/css/bootstrap-responsive.css">
<link rel="stylesheet" href="/stylesheets/style.css">
<script src="js/jquery.js"></script>
<script src="js/bootstrap.min.js"></script>
  <body>
    <div class="navbar navbar-default navbar-static-top">
    <div class="container">
      <div class="navbar-header">
        <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
        </button>
        <a class="navbar-brand" href="#">Bootstrap</a>
      </div>
      <div class="collapse navbar-collapse">
        <ul class="nav navbar-nav navbar-right">
          <li class="active"><a href="#">Home</a></li>
          <li><a href="#about">About</a></li>
          <li><a href="#contact">Contact</a></li>
        </ul>
      </div><!--/.nav-collapse -->
    </div>
  </div>"""

HTML_FOOTER = "</body></html>"

class Restaurant:
    def __init__(self, name, address, weeks_menus):
        self.name = name
        self.address = address
        self.weeks_menus = weeks_menus





class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        self.response.write(HTML_HEADER)
        today = datetime.date.today()
        last_monday = today + datetime.timedelta(days=-today.weekday(), weeks=0)

        restaurants = [Restaurant("Bolero", "Atomitie 2 c 00370 Helsinki", parse_bolero_json(last_monday)),
               Restaurant("Atomitie 5", "Atomitie 5 00370 Helsinki", parse_atomitie5_json(last_monday))]

        self.response.write("""<div class="container"><div class="row">""")

        for restaurant in restaurants:
            self.response.write("""<div class="col-md-4">
                                        <div class="panel panel-default">
                                            <div class="panel-heading">""")
            self.response.write("<h3>" + restaurant.name + "</h3></div>") #panel-heading
            self.response.write("""<div class="panel-body">""")
            for course in restaurant.weeks_menus[today.weekday()]:
                for component in course["Courses"]:
                    self.response.write(component["Food"] + " <i>" +' '.join(component["Types"]) + "</i><br>")
                self.response.write(course["Price"]+ "<br><br>")
            self.response.write("</div>") #panel-body
            self.response.write("</div>") #panel
            self.response.write("</div>") #col
        self.response.write("</div></div>") #menu-container, row

        self.response.write(HTML_FOOTER)


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
