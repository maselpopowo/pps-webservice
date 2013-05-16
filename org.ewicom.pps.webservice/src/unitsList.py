#!/usr/bin/env python

from pps.webservice import json_parser
from pps.webservice import ppsvar

print ppsvar.JSON_CONTENT_TYPE
print json_parser.getUnitList()

