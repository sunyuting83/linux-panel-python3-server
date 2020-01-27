#!/usr/bin/python
# -*- coding: UTF-8 -*-from bottle import route, run
from lib import run
import router

run(host='0.0.0.0', port=3200, debug=True)