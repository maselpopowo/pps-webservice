
'''
Created on 14-05-2013

@author: 001289mkun
'''
from pps.webservice import db_helper
from pps.webservice import ppsvar
import json

def getUnitList():
    """
    Funkcja zwraca json dla listy jednostek w bazie
    """
    units = db_helper.getUnitList()
    json_string = json.dumps(units)
    return json_string

def getUnitInfo(unitId):
    """
    Funkcja zwraca json dla pojedynczej jednostki - details, phones i leaders
    """
    details = db_helper.getUnitDetails(unitId)
    phones = db_helper.getUnitPhones(unitId)
    leaders = db_helper.getUnitLeaders(unitId)
    
    unitData = []
    unitData.append({ppsvar.JSON_DETAILS_ID:details})
    unitData.append({ppsvar.JSON_PHONES_ID:phones})
    unitData.append({ppsvar.JSON_LEADERS_ID:leaders})
    
    json_string = json.dumps(unitData)
    return json_string

