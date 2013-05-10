# -*- coding: utf-8 -*-
'''
Created on 16-04-2013

@author: 001289mkun
'''
import utils
import parser
import psycopg2
import ppsvar

def getConnection():
    try:
        dsn = utils.getDBSettings()
        conn = psycopg2.connect(dsn)
    except psycopg2.Error as e:
        utils.log('Problem z polaczeniem z baza danych: ' + repr(e))
    else:
        return conn
    
def updateUnitTable():
    conn = getConnection()
    if conn is not None:
        cursor = conn.cursor()    
    
        link = utils.getFirstUnitLink()
        cursor.execute(ppsvar.SQL_CREATE_PARENT_TEMP)
        while link:
            unitId = parser.getUnitIdAndParent(link)
        
            cursor.execute(ppsvar.SQL_MERGE_UNIT, (unitId[ppsvar.UNIT_TEXTID], link))
            cursor.execute(ppsvar.SQL_INSERT_PARENT_TEMP, (unitId[ppsvar.UNIT_PARENT], unitId[ppsvar.UNIT_TEXTID]))
            conn.commit()
        
            utils.deleteFirstUnitLink()
            link = utils.getFirstUnitLink()
    
        cursor.execute(ppsvar.SQL_UPDATE_UNIT_FROM_PARENT_TEMP)
        conn.commit()
        cursor.close()
        conn.close()

def getOldestUnit():
    conn = getConnection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute(ppsvar.SQL_SELECT_OLDEST_UNIT)
        
        res = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if res is not None:
            return {ppsvar.UNIT_ID:res[0], ppsvar.UNIT_TEXTID:res[1], ppsvar.UNIT_LINK:res[2]}
        else:
            return None
    else:
        return None

def insertUnitDate(unit):
    conn = getConnection()
    cursor = conn.cursor()

    if unit:
        cursor.execute(ppsvar.SQL_DELETE_DETEILS_BY_UNIT, unit)
        cursor.execute(ppsvar.SQL_INSERT_DETAILS, unit)
        conn.commit()
    
    cursor.close()
    conn.close()
    
def insertUnitLeaders(leaders, unitId):
    conn = getConnection()
    cursor = conn.cursor()
    
    if leaders:
        cursor.execute(ppsvar.SQL_DELETE_LEADER_BY_UNIT, (unitId,))
        for l in leaders:
            l[ppsvar.UNIT_ID] = unitId
            cursor.execute(ppsvar.SQL_INSERT_LEADER, l)
        conn.commit()
    
    cursor.close()
    conn.close()

def insertUnitPhones(phones, unitId):
    conn = getConnection()
    cursor = conn.cursor()
    
    if phones:
        cursor.execute(ppsvar.SQL_DELETE_PHONE_BY_UNIT, (unitId,))
        for p in phones:
            p[ppsvar.UNIT_ID] = unitId
            cursor.execute(ppsvar.SQL_INSERT_PHONE, p)
        conn.commit()
    
    cursor.close()
    conn.close()

def updateUnitLastModified(unitId):
    conn = getConnection()
    cursor = conn.cursor()
    
    cursor.execute(ppsvar.SQL_UPDATE_UNIT_LASTMODIFIED, (unitId,))
    
    conn.commit()
    cursor.close()
    conn.close()

def getUnitTypeList():
    conn = getConnection()
    if conn is not None:
        cursor = conn.cursor()
        
        types = []
        cursor.execute(ppsvar.SQL_SELECT_UNITTYPE)
        res = cursor.fetchall()
        
        if res:
            for r in res:
                types.append({ppsvar.UNITTYPE_ID:r[0],ppsvar.UNITTYPE_NAME:r[1],ppsvar.UNITTYPE_SYMBOL:r[2]})
    
    cursor.close()
    conn.close()
    
    return types
