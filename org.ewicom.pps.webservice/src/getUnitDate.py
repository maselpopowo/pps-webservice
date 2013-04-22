# -*- coding: utf8 -*-
from pps.webservice import utils
from pps.webservice import parser
from pps.webservice import dbhelper
from pps.webservice import ppsvar
import datetime

unitId = dbhelper.getOldestUnit()

if unitId is not None and unitId[ppsvar.UNIT_ID] != ppsvar.CZSW_ID:
    unit = {}
    unit[ppsvar.UNIT_ID] = unitId[ppsvar.UNIT_ID]
    page = utils.getContent(unitId[ppsvar.UNIT_LINK])
    
    name = parser.getUnitName(page)
    unit[ppsvar.UNIT_NAME] = name
    
    sname = parser.getUnitShortName(page)
    unit[ppsvar.UNIT_SNAME] = sname
    
    mapcor = parser.getMapCoordinate(page)
    unit[ppsvar.UNIT_LATITUDE] = mapcor[ppsvar.UNIT_LATITUDE]
    unit[ppsvar.UNIT_LONGITUDE] = mapcor[ppsvar.UNIT_LONGITUDE]
    
    definfo = parser.getBasicUnitInformations(page)
    unit[ppsvar.UNIT_STREET] = definfo[ppsvar.UNIT_STREET]
    unit[ppsvar.UNIT_POSTCODE] = definfo[ppsvar.UNIT_POSTCODE]
    unit[ppsvar.UNIT_CITY] = definfo[ppsvar.UNIT_CITY]
    unit[ppsvar.UNIT_PHONE] = definfo[ppsvar.UNIT_PHONE]
    unit[ppsvar.UNIT_EMAIL] = definfo[ppsvar.UNIT_EMAIL]
    
    imgs = parser.getUnitImages(page)
    unit[ppsvar.UNIT_IMG] = imgs[ppsvar.UNIT_IMG]
    unit[ppsvar.UNIT_SIMG] = imgs[ppsvar.UNIT_SIMG]
    
    defdesc = parser.getDefaultDescription(page)
    unit[ppsvar.UNIT_DESCRIPTION] = defdesc

    dbhelper.insertUnitDate(unit)
    dbhelper.updateUnitLastModified(unit[ppsvar.UNIT_ID])
    
    utils.saveScriptInfo('Zaktualizowano dane jednostki: ' + unit[ppsvar.UNIT_ID] + ' DATA: ' + str(datetime.datetime.now()) + '\n')

else:
    utils.saveScriptInfo('(Brak aktualizacji)Dane dla ' + unit[ppsvar.UNIT_ID] + ' DATA: ' + str(datetime.datetime.now()) + '\n')
    