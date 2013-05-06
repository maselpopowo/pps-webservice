# -*- coding: utf8 -*-
from pps.webservice import utils
from pps.webservice import parser
from pps.webservice import db_helper
from pps.webservice import ppsvar

unitsLinks = []
page = utils.getContent(ppsvar.FIRST_PAGE)

while(page is not None):
    unitsLinks.extend(parser.getUnitsLinks(page))
    nlink = parser.getUnitsNextPageLink(page)
    if nlink is not None:
        page = utils.getContent(nlink)
    else:
        page = None

utils.saveUnitsLinksToFile(unitsLinks)
utils.log('Pobrano linki jednostek: ILOSC: ' + str(len(unitsLinks)) )

db_helper.updateUnitTable()
