#!/usr/bin/env python
# -- coding: utf-8 --
import webapp2
from app.lunchapp import *
# Kun depolyaat appengineen:
# 1. Vaihda debug=False


app = webapp2.WSGIApplication([
    ('/', MainPage),
    (r'/settings', SettingsPage),
    (r'/about', AboutPage),
    (r'/worker', FetchData)
    ],
    debug=False)
