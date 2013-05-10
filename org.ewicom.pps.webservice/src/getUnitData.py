#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pps.webservice import utils
from pps.webservice import parser
from pps.webservice import db_helper
from pps.webservice import ppsvar

unitId = db_helper.getOldestUnit()

if unitId is not None:
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
            
            lname = parser.getUnitListNameAndType(sname)
            unit[ppsvar.UNIT_LNAME] = lname[ppsvar.UNIT_LNAME]
            unit[ppsvar.UNITTYPE_ID] = lname[ppsvar.UNITTYPE_ID]
            
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
            utils.log('ERROR: Blad aktalizacji danych jednostki: ' + unit[ppsvar.UNIT_TEXTID])
        else:
            db_helper.insertUnitDate(unit)
            utils.log('Zaktualizowano dane jednostki: ' + unit[ppsvar.UNIT_TEXTID])
        
        try:
            leaders = parser.getLeaders(page,unit[ppsvar.UNIT_TEXTID])   
        except parser.LeadersParseError as e:
            utils.log('ERROR: ' + str(e) + unit[ppsvar.UNIT_TEXTID])
        else:
            db_helper.insertUnitLeaders(leaders, unit[ppsvar.UNIT_ID])
            utils.log('Zaktualizowano kierownictwo: ' + unit[ppsvar.UNIT_TEXTID])
        
        try:
            phones = parser.getPhones(page)
        except parser.PhonesParseError as e:
            utils.log('ERROR: ' + str(e) + unit[ppsvar.UNIT_TEXTID])
        else:
            db_helper.insertUnitPhones(phones, unit[ppsvar.UNIT_ID])
            utils.log('Zaktualizowano telefony: ' + unit[ppsvar.UNIT_TEXTID])
    else:
        utils.log('ERROR: Nie mozna pobrac strony jednostki: ' + unit[ppsvar.UNIT_TEXTID])
    
    db_helper.updateUnitLastModified(unit[ppsvar.UNIT_ID])
else:
    utils.log('ERROR: Pobrano None dla najstarszej jednostki w bazie')
