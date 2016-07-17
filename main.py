#!/usr/bin/env python
# -- coding: utf-8 --

from old_lunchapp.lunchapp import *
from material_backend.material_app import *




# Kun depolyaat appengineen:
# 1. Vaihda debug=Fals


app = webapp2.WSGIApplication([
    ('/', MainPage),
    (r'/settings', SettingsPage),
    (r'/about', AboutPage),
    (r'/worker', FetchData),
    ('/rest/query', QueryHandler),
    ],
    debug=False)
