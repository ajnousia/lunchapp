#!/usr/bin/env python
# -- coding: utf-8 --

import material_backend.rest_classes as rest_classes
import webapp2

# Kun depolyaat appengineen:
# 1. Vaihda debug=False

app = webapp2.WSGIApplication([
    ('/rest/query', rest_classes.QueryHandler),
    ],
    debug=True)
