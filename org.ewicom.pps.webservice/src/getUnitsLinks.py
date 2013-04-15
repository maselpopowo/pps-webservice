# -*- coding: utf8 -*-
from pps.webservice import utils
from pps.webservice import parser
import datetime

firstPage = 'http://www.sw.gov.pl/pl/jednostki/'
unitsLinks = []

page = utils.getContent(firstPage)

while(page is not None):
    unitsLinks.extend(parser.getUnitsLinks(page))
    nlink = parser.getUnitsNextPageLink(page)
    if nlink is not None:
        page = utils.getContent(nlink)
    else:
        page = None

utils.saveUnitsLinksToFile(unitsLinks)

utils.saveScriptInfo('Pobrano linki jednostek: ILOSC: ' + str(len(unitsLinks)) + ' DATA: ' + str(datetime.datetime.now()) + '\n')