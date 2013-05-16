#!/usr/bin/env python

from pps.webservice import json_parser
from pps.webservice import ppsvar
import cgi

form = cgi.FieldStorage()
unitId = form.getvalue('unitId')

print ppsvar.JSON_CONTENT_TYPE
print json_parser.getUnitInfo(unitId)
