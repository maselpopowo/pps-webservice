# -*- coding: UTF-8 -*-
'''
Created on 22-04-2013

@author: 001289mkun
'''
FIRST_PAGE = 'http://www.sw.gov.pl/pl/jednostki/'
CZSW_PAGE = 'http://www.sw.gov.pl/pl/o-sluzbie-wieziennej/centralny-zarzad-sw/'

LINKS_FILE = 'links.txt'
INFO_FILE = 'info.txt'
LOG_FILE = 'log.txt'
DB_SETTINGS_FILE = 'dbsettings.txt'

NEXT_PAGE_TEXT = u"Nast\u0119pna"
LINK_START_TEXT = 'http://sw.gov.pl'
DEF_DESC_TEXT = 'opispodstawowy'
LEADER_CLASS = 'praca-margines tab-leaders-content'
PHONES_CLASS = 'praca-margines tab-importantPh-content'
MAP_LATITUDE_ID = 'mapka_Latitude'
MAP_LONGITUDE_ID = 'mapka_Longitude'

CZSW_TEXTID = 'centralny-zarzad-sw'

UNIT_ID = 'unit_id'
UNIT_TEXTID = 'unit_textid'
UNIT_PARENT = 'parent_id'
UNIT_LINK = 'unit_link'
UNIT_LASTMODIFIED = 'unit_lastmodified'

UNIT_NAME = 'unit_name'
UNIT_SNAME = 'unit_sname'
UNIT_LNAME = 'unit_lname'
UNIT_LATITUDE = 'unit_latitude'
UNIT_LONGITUDE = 'unit_longitude'
UNIT_STREET = 'unit_street'
UNIT_POSTCODE = 'unit_postcode'
UNIT_CITY = 'unit_city'
UNIT_PHONE = 'unit_phone'
UNIT_EMAIL = 'unit_email'
UNIT_IMG = 'unit_img'
UNIT_SIMG = 'unit_simg'
UNIT_DESCRIPTION = 'unit_description'

DETAILS_ID = 'details_id'

LEADER_ID = 'leader_id'
LEADER_POSITION = 'leader_position'
LEADER_NAME = 'leader_name'
LEADER_PHONE = 'leader_phone'

PHONE_ID = 'phone_id'
PHONE_NAME = 'phone_name'
PHONE_NUMBER = 'phone_number'
LEADER_EMAIL = 'leader_email'

UNITTYPE_ID = 'unittype_id'
UNITTYPE_NAME = 'unittype_name'
UNITTYPE_SYMBOL = 'unittype_symbol'

SQL_CREATE_PARENT_TEMP = 'CREATE TEMP TABLE parent_temp (parent_textid character varying(100),unit_textid character varying(100))'
SQL_INSERT_PARENT_TEMP = 'INSERT INTO parent_temp(parent_textid,unit_textid) VALUES (%s,%s)'
SQL_MERGE_UNIT = 'SELECT merge_unit(%s,%s)'
SQL_UPDATE_UNIT_FROM_PARENT_TEMP = 'UPDATE unit SET unit_parentid = (SELECT unit_id FROM unit WHERE unit_textid=p.ptext) FROM (SELECT DISTINCT unit_textid AS utext, parent_textid AS ptext FROM parent_temp) AS p WHERE unit_textid=p.utext'
SQL_SELECT_OLDEST_UNIT = 'SELECT unit_id, unit_textid, unit_link FROM unit WHERE unit_lastmodified = (SELECT min(unit_lastmodified) FROM unit) LIMIT 1'
SQL_DELETE_DETEILS_BY_UNIT = """DELETE FROM details WHERE unit_id=%(unit_id)s"""
SQL_INSERT_DETAILS = """INSERT INTO details(unit_id, unittype_id, unit_name, unit_sname, unit_lname, unit_latitude, unit_longitude, unit_street, unit_postcode, unit_city, unit_phone, unit_email, unit_img, unit_simg, unit_description) VALUES (%(unit_id)s, %(unittype_id)s, %(unit_name)s, %(unit_sname)s, %(unit_lname)s, %(unit_latitude)s, %(unit_longitude)s, %(unit_street)s, %(unit_postcode)s, %(unit_city)s, %(unit_phone)s, %(unit_email)s, %(unit_img)s, %(unit_simg)s, %(unit_description)s);"""
SQL_DELETE_LEADER_BY_UNIT = """DELETE FROM leader WHERE unit_id=%s"""
SQL_INSERT_LEADER = """INSERT INTO leader (unit_id,leader_position,leader_name,leader_phone,leader_email) VALUES (%(unit_id)s,%(leader_position)s,%(leader_name)s,%(leader_phone)s,%(leader_email)s)"""
SQL_DELETE_PHONE_BY_UNIT = """DELETE FROM phone WHERE unit_id=%s"""
SQL_INSERT_PHONE = """INSERT INTO phone (unit_id,phone_name,phone_number) VALUES (%(unit_id)s,%(phone_name)s,%(phone_number)s)"""
SQL_UPDATE_UNIT_LASTMODIFIED = """UPDATE unit SET unit_lastmodified=now() WHERE unit_id=%s"""
SQL_SELECT_UNITTYPE = """SELECT unittype_id, unittype_name, unittype_symbol FROM unittype"""

SQL_SELECT_UNIT_LIST = """SELECT unit_id, unit_lname, parent_id, parent_lname FROM unit_list ORDER BY unit_lname ASC"""
SQL_SELECT_UNIT_PHONES = """SELECT phone_id, phone_name, phone_number FROM phone WHERE unit_id=%s"""
SQL_SELECT_UNIT_LEADERS = """SELECT leader_id, leader_position, leader_name, leader_phone, leader_email FROM leader WHERE unit_id=%s"""
SQL_SELECT_UNIT_DETAILS = """SELECT details_id, unittype_id, unit_name, unit_sname, unit_lname, unit_latitude, unit_longitude, unit_street, unit_postcode, unit_city, unit_phone, unit_email, unit_img, unit_simg, unit_description FROM details WHERE unit_id=%s"""

UNITTYPE_ID_AS = 1
UNITTYPE_ID_ZK = 2
UNITTYPE_ID_OZ = 3
UNITTYPE_ID_OISW = 4
UNITTYPE_ID_CZSW = 5
UNITTYPE_ID_OSSW = 6
UNITTYPE_ID_COSSW = 7
UNITTYPE_ID_ODKSW = 8
UNITTYPE_ID_OZM = 9
UNITTYPE_ID_BIURO = 10
UNITTYPE_ID_ZESPOL = 11

UNITTYPE_REG_INDEX_WZOR = 0
UNITTYPE_REG_INDEX_ID = 1
UNITTYPE_REG_INDEX_WYNIK = 2

UNITTYPE_REG = [[u"Areszt \u015aledczy",UNITTYPE_ID_AS,u"%s A\u015a"],
                [u"Zak\u0142ad Karny",UNITTYPE_ID_ZK,u"%s ZK"],
                [u"Okr\u0119gowy Inspektorat S\u0142u\u017cby Wi\u0119ziennej",UNITTYPE_ID_OISW,u"%s OISW"],
                [u"Centralny Zarz\u0105d SW",UNITTYPE_ID_CZSW,u"Centralny Zarz\u0105d SW"],
                [u"Centralny O\u015brodek Szkolenia S\u0142u\u017cby Wi\u0119ziennej w Kaliszu",UNITTYPE_ID_COSSW,u"Kalisz COSSW"],
                [u"O\u015brodek Szkolenia S\u0142u\u017cby Wi\u0119ziennej w Kulach",UNITTYPE_ID_OSSW,u"Kule OSSW"],
                [u"O\u015brodek Szkolenia SW w Kulach Oddzia\u0142 Zamiejscowy w Sulejowie",UNITTYPE_ID_OZM,u"Sulej\u00f3w OZ Kule OSSW"],
                [u"O\u015brodek Szkolenia S\u0142u\u017cby Wi\u0119ziennej w Popowie",UNITTYPE_ID_OSSW,u"Popowo OSSW"],
                [u"O\u015brodek Doskonalenia Kadr S\u0142u\u017cby Wi\u0119ziennej w Suchej",UNITTYPE_ID_ODKSW,u"Sucha ODKSW"],
                [u"Biuro",UNITTYPE_ID_BIURO,u"%s BIURO"],
                [u"Zesp\u00f3\u0142",UNITTYPE_ID_ZESPOL,u"%s ZESP\u00d3\u0141"],
                [u"Oddzia\u0142 Zewn\u0119trzny",UNITTYPE_ID_OZ,u"%s OZ"]]

UNIT_LIST_UNIT_ID = 'unit_id'
UNIT_LIST_UNIT_LNAME = 'unit_lname'
UNIT_LIST_PARENT_ID = 'parent_id'
UNIT_LIST_PARENT_LNAME = 'parent_lname'

JSON_CONTENT_TYPE = 'Content-type: application/json; charset=utf-8\n\n'

JSON_DETAILS_ID = 'details'
JSON_PHONES_ID = 'phones'
JSON_LEADERS_ID = 'leaders'
