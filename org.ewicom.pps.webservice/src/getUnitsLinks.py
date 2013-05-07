#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pps.webservice import utils
from pps.webservice import parser
from pps.webservice import db_helper

unitsLinks = []
unitsLinks.extend(parser.getUnitsLinks())
unitsLinks.extend(parser.getDepartmentsLinks())

utils.saveUnitsLinksToFile(unitsLinks)
utils.log('Pobrano linki jednostek: ILOSC: ' + str(len(unitsLinks)) )

db_helper.updateUnitTable()
