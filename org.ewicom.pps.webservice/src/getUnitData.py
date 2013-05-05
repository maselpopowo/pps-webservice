# -*- coding: utf8 -*-
from pps.webservice import utils
from pps.webservice import parser
from pps.webservice import dbhelper
from pps.webservice import ppsvar

for i in range(215):
    i = i + 1
    print i
    unitId = dbhelper.getOldestUnit()
    
    if unitId is not None:
        if unitId[ppsvar.UNIT_TEXTID] != ppsvar.CZSW_TEXTID:
            unit = {}
            unit[ppsvar.UNIT_ID] = unitId[ppsvar.UNIT_ID]
            unit[ppsvar.UNIT_TEXTID] = unitId[ppsvar.UNIT_TEXTID]
            
            page = utils.getContent(unitId[ppsvar.UNIT_LINK])
            if page is not None:
                try:
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
                except parser.UnitParseError as e:
                    utils.log(str(e) + unit[ppsvar.UNIT_TEXTID])
                    utils.log('Blad aktalizacji danych jednostki: ' + unit[ppsvar.UNIT_TEXTID])
                else:
                    dbhelper.insertUnitDate(unit)
                    utils.log('Zaktualizowano dane jednostki: ' + unit[ppsvar.UNIT_TEXTID])
                
                try:
                    leaders = parser.getLeaders(page)   
                except parser.LeadersParseError as e:
                    utils.log(str(e) + unit[ppsvar.UNIT_TEXTID])
                else:
                    dbhelper.insertUnitLeaders(leaders, unit[ppsvar.UNIT_ID])
                    utils.log('Zaktualizowano kierownictwo: ' + unit[ppsvar.UNIT_TEXTID])
                
                try:
                    phones = parser.getPhones(page)
                except parser.PhonesParseError as e:
                    utils.log(str(e) + unit[ppsvar.UNIT_TEXTID])
                else:
                    dbhelper.insertUnitPhones(phones, unit[ppsvar.UNIT_ID])
                    utils.log('Zaktualizowano telefony: ' + unit[ppsvar.UNIT_TEXTID])
                
                dbhelper.updateUnitLastModified(unit[ppsvar.UNIT_ID])
            else:
                utils.log('Nie mozna pobrac strony jednostki: ' + unit[ppsvar.UNIT_TEXTID])
        else:
            utils.log('Proba pobrania danych dla czsw')
            dbhelper.updateUnitLastModified(unitId[ppsvar.UNIT_ID])
    else:
        utils.log('Pobrano None dla najstarszej jednostki w bazie')
    