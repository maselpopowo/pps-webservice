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

def updateUnitTable_old():
    conn = getConnection()
    cursor = conn.cursor()    
    cursor.execute('DELETE FROM unit')

    link = utils.getFirstUnitLink()
    while link:
        unitId = parser.getUnitIdAndParent(link)
    
        cursor.execute('SELECT merge_unit(%s,%s,%s)', (unitId['unit_id'], unitId['parent_id'], link))
        conn.commit()
    
        utils.deleteFirstUnitLink()
        link = utils.getFirstUnitLink()

    cursor.close()
    conn.close()
    
def updateUnitTable():
    conn = getConnection()
    if conn is not None:
        cursor = conn.cursor()    
    
        link = utils.getFirstUnitLink()
        while link:
            unitId = parser.getUnitIdAndParent(link)
        
            cursor.execute('SELECT merge_unit(%s,%s)', (unitId[ppsvar.UNIT_TEXTID], link))
            conn.commit()
        
            utils.deleteFirstUnitLink()
            link = utils.getFirstUnitLink()
    
        cursor.close()
        conn.close()

def getOldestUnit():
    conn = getConnection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('SELECT unit_id, unit_textid, unit_link FROM unit WHERE unit_lastmodified = (SELECT min(unit_lastmodified) FROM unit) LIMIT 1;')
        
        res = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if res is not None:
            return {ppsvar.UNIT_ID:res[0],ppsvar.UNIT_TEXTID:res[1],ppsvar.UNIT_LINK:res[2]}
        else:
            return None
    else:
        return None

def insertUnitDate(unit):
    conn = getConnection()
    cursor = conn.cursor()

    if unit:
        cursor.execute("""DELETE FROM details WHERE unit_id=%(unit_id)s""",unit)
        cursor.execute("""INSERT INTO details(unit_id, unit_name, unit_sname, unit_latitude, unit_longitude, unit_street, unit_postcode, unit_city, unit_phone, unit_email, unit_img, unit_simg, unit_description) VALUES (%(unit_id)s, %(unit_name)s, %(unit_sname)s, %(unit_latitude)s, %(unit_longitude)s, %(unit_street)s, %(unit_postcode)s, %(unit_city)s, %(unit_phone)s, %(unit_email)s, %(unit_img)s, %(unit_simg)s, %(unit_description)s);""",unit)
        conn.commit()
    
    cursor.close()
    conn.close()
    
def insertUnitLeaders(leaders,unitId):
    conn = getConnection()
    cursor = conn.cursor()
    
    if leaders:
        cursor.execute("""DELETE FROM leader WHERE unit_id=%s""",(unitId,))
        for l in leaders:
            l[ppsvar.UNIT_ID] = unitId
            cursor.execute("""INSERT INTO leader (unit_id,leader_position,leader_name,leader_phone,leader_email) VALUES (%(unit_id)s,%(leader_position)s,%(leader_name)s,%(leader_phone)s,%(leader_email)s)""",l)
        conn.commit()
    
    cursor.close()
    conn.close()

def insertUnitPhones(phones,unitId):
    conn = getConnection()
    cursor = conn.cursor()
    
    if phones:
        cursor.execute("""DELETE FROM phone WHERE unit_id=%s""",(unitId,))
        for p in phones:
            p[ppsvar.UNIT_ID] = unitId
            cursor.execute("""INSERT INTO phone (unit_id,phone_name,phone_number) VALUES (%(unit_id)s,%(phone_name)s,%(phone_number)s)""",p)
        conn.commit()
    
    cursor.close()
    conn.close()

def updateUnitLastModified(unitId):
    conn = getConnection()
    cursor = conn.cursor()
    
    cursor.execute("""UPDATE unit SET unit_lastmodified=now() WHERE unit_id=%s""",(unitId,))
    
    conn.commit()
    cursor.close()
    conn.close()
