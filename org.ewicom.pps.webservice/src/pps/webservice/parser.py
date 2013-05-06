# -*- coding: utf8 -*-
'''
Modul udostepnia dane do parsowania strony sw.gov.pl

@author: Marcin Kunicki
@contact: masel.popowo@gmail.com

@version: 0.1
'''
from bs4 import BeautifulSoup
from pps.webservice import ppsvar, utils

class UnitsLinksParseError(Exception):
    """
    Wyjatek rzucany dla bledu parsowania linkow jednostek
    """
    def __init__(self,msg):
        self.msg = msg
    def __str__(self):
        return self.__class__.__name__+': '+repr(self.msg)

class UnitParseError(Exception):
    """
    Wyjatek rzucany dla bledu parsowania danych dla jednostki
    """
    def __init__(self,msg):
        self.msg = msg
    def __str__(self):
        return self.__class__.__name__+': '+repr(self.msg)

class LeadersParseError(Exception):
    """
    Wyjatek rzucany dla bledu parsowania danych o kierownictwie
    """
    def __init__(self,msg):
        self.msg = msg
    def __str__(self):
        return self.__class__.__name__+': '+repr(self.msg)

class PhonesParseError(Exception):
    """
    Wyjatek rzycany dla bledu parsowania danych o telefonach
    """
    def __init__(self,msg):
        self.msg = msg
    def __str__(self):
        return self.__class__.__name__+': '+repr(self.msg)
                
def getUnitsNextPageLink(content):
    """
    Funkcja pobiera link do nastepnej strony z jednostkami
    
    Zwraca link do nastepnej strony
    """
    soup = BeautifulSoup(content)
    
    try:
        link = soup.find('a', text=ppsvar.NEXT_PAGE_TEXT)
    except AttributeError as e:
        raise UnitsLinksParseError(e)
    else:   
        if link is not None:
            return ppsvar.LINK_START_TEXT + link['href']
        else:
            return None

def getUnitsOnPageLinks(content):
    """
    Funkcja pobiera linki do stron jednostek podstawowych z pojedynczej strony zbiorczej
    
    Zwraca liste linkow
    """
    soup = BeautifulSoup(content)
    links = []
    
    try:
        divs = soup.find_all('div', class_='left')
        if divs:
            links = [ppsvar.LINK_START_TEXT + div.a['href'] for div in divs]
    except AttributeError as e:
        raise UnitsLinksParseError(e)
    else:
        return links

def getUnitsLinks():
    """
    Funkcja pobiera linki jednostek podsawowych
    
    Zwraca liste linkow
    """
    page = utils.getContent(ppsvar.FIRST_PAGE)
    links = []

    while(page is not None):
        links.extend(getUnitsOnPageLinks(page))
        nlink = getUnitsNextPageLink(page)
        if nlink is not None:
            page = utils.getContent(nlink)
        else:
            page = None
    
    return links

def getDepartmentsLinks():
    """
    Funkcja zwraca linki do biur i zespolow podleglych czsw
    
    Zwraca liste linkow
    """
    content = utils.getContent(ppsvar.CZSW_PAGE)
    soup = BeautifulSoup(content)
    links = []
    
    try:
        ul = soup.find('ul',class_='poziom3')
        lis = ul.find_all('li')
        if lis:
            links = [ppsvar.LINK_START_TEXT + li.a['href'] for li in lis]
    except AttributeError as e:
        raise UnitsLinksParseError(e)
    else:
        return links

def getUnitIdAndParent(link):
    """
    Funkcja pobiera id jednostki i id rodzica
    
    Zwraca slownik z id
    """
    part = link.split('/')
    
    unit = part[-2]
    parent = part[-3]
    
    if unit == ppsvar.CZSW_TEXTID or parent == 'pl':
        d = {ppsvar.UNIT_TEXTID:unit, ppsvar.UNIT_PARENT:unit}
    else:
        d = {ppsvar.UNIT_TEXTID:unit, ppsvar.UNIT_PARENT:parent}
    
    return d

def getUnitName(content):
    """
    Funkcja pobiera pena nazw jednostki
    
    Zwraca nazwe jednostki - string
    """
    soup = BeautifulSoup(content)
    try:
        divs = soup.find_all('div', class_='jednostka')
        for d in divs:
            if d.find('h3'):
                unit_name = d.h3.string
                unit_name = unit_name.strip()
    except AttributeError as e:
        raise UnitParseError(e)
    else:
        return unit_name

def getUnitShortName(content):
    """
    Funkcja pobiera skrucona nazwe jednostki
    
    Zwrana skrucona nazwe jednostki
    """
    soup = BeautifulSoup(content)
    
    try:
        unit_sname_ns = soup.title.string
        unit_sname = unit_sname_ns.split('/')
        unit_sname = unit_sname[-1].strip()
    except AttributeError as e:
        raise UnitParseError(e)
    else:
        return unit_sname

def getMapCoordinate(content):
    """
    Funkcja pobiera koordynaty na mapie
    
    Zwraca slownik lub None
    """
    soup = BeautifulSoup(content)
    
    unit_latitude = soup.find(id=ppsvar.MAP_LATITUDE_ID)
    unit_longitude = soup.find(id=ppsvar.MAP_LONGITUDE_ID)
    
    if unit_latitude is not None or unit_longitude is not None:
        s = {ppsvar.UNIT_LATITUDE:unit_latitude['value'], 
             ppsvar.UNIT_LONGITUDE:unit_longitude['value']}
    else:
        s = {ppsvar.UNIT_LATITUDE:'', 
             ppsvar.UNIT_LONGITUDE:''}
    
    return s

def getBasicUnitInformations(content):
    """
    Funkcja pobiera dane podstawowe o jednostce - adres, tel, email
    
    Zwraca slownik
    """
    soup = BeautifulSoup(content)
    
    try:
        div = soup.find_all('div', class_='jednostka')
        for d in div:
            if d.h3:
                p = d.find_all('p')
                
                unit_street = (p[0].string).strip()
                
                unit_tc = (p[1].string).strip()
                unit_postcode = unit_tc[0:6]
                unit_city = unit_tc[7:]
                
                unit_phone_p = p[2].string
                unit_phone = unit_phone_p[10:].strip()
                
                unit_email_p = p[3].string
                unit_email = unit_email_p[8:].strip()
    except AttributeError as e:
        raise UnitParseError(e)
    else:
        d = {ppsvar.UNIT_STREET:unit_street, 
             ppsvar.UNIT_POSTCODE:unit_postcode, 
             ppsvar.UNIT_CITY:unit_city, 
             ppsvar.UNIT_PHONE:unit_phone, 
             ppsvar.UNIT_EMAIL:unit_email}
        
    return d

def getUnitImages(content):
    """
    Funkcja pobiera linki do zdjec jednostki
    
    Zwaraca slownik z 2 linkami
    """
    soup = BeautifulSoup(content)
    
    try:
        div = soup.find('div', class_='pad') 
        if div is not None:
            a = div.find('a')
        else:
            a = None
    except AttributeError as e:
        raise UnitParseError(e)
    else:
        if a is not None:
            unit_simg = ppsvar.LINK_START_TEXT + a['href']
            unit_img = ppsvar.LINK_START_TEXT + a.img['src']
            d = {ppsvar.UNIT_SIMG:unit_simg, ppsvar.UNIT_IMG:unit_img}
        else:
            d = {ppsvar.UNIT_SIMG:'', ppsvar.UNIT_IMG:''}
    
    return d

def getDefaultDescription(content):
    """
    Funkcja pobiera opis podstawowy jednostki
    
    Zwraca string
    """
    soup = BeautifulSoup(content)
    
    desc = soup.find(id=ppsvar.DEF_DESC_TEXT)
    
    if desc is not None:
        d = desc.get_text()
    else:
        d = ''
        
    return d

def getUnitLeaders(content):
    """
    Funkcja pobiera dane o kierownictwie
    
    Zwraca liste kierownictwa
    """
    soup = BeautifulSoup(content)
    keys = {1:ppsvar.LEADER_POSITION, 
            2:ppsvar.LEADER_NAME, 
            3:ppsvar.LEADER_PHONE, 
            4:ppsvar.LEADER_EMAIL}
    leaders = []
    
    try:
        mdiv = soup.find('div', class_=ppsvar.LEADER_CLASS)
        divs = mdiv.find_all('div')
    except AttributeError as e:
        raise LeadersParseError(e)
    else:
        if len(divs) == 1:
            raise LeadersParseError('Brak danych o kierownictwie')
        else:
            i = 1
            l = {}
            for d in divs:
                if d.get('class') == ['first-l']:
                    if l:
                        leaders.append(l)
                    i = 1
                    l = {}
                if d.get('class') == ['jedn-linia']:
                    continue
                else:
                    l[keys[i]] = d.get_text().strip()
                    i = i + 1
            leaders.append(l)
        
        for l in leaders:
            l[keys[3]] = (l[keys[3]])[10:]
            if len(l) == 4:
                l[keys[4]] = (l[keys[4]])[8:]
            else:
                l[keys[4]] = ''
    
    return leaders

def getCzswLeaders(content):
    """
    Funkcja pobiera dane o kierownictwie czsw
    
    Zwraca liste kierownictwa
    """
    soup = BeautifulSoup(content)
    keys = {1:ppsvar.LEADER_POSITION, 
            2:ppsvar.LEADER_NAME, 
            3:ppsvar.LEADER_PHONE, 
            4:ppsvar.LEADER_EMAIL}
    leaders = []
    
    try:
        mdiv = soup.find('div', class_=ppsvar.LEADER_CLASS)
        divs = mdiv.find_all('div', class_='leader-zd')
    except AttributeError as e:
        raise LeadersParseError(e)
    else:
        for div in divs:
            l = {}
            i = 1
            for d in div.find_all('div'):
                    l[keys[i]] = d.get_text().strip()
                    i = i + 1
            leaders.append(l)
    
        for l in leaders:
            l[keys[3]] = (l[keys[3]])[10:]
            if len(l) == 4:
                l[keys[4]] = (l[keys[4]])[8:]
            else:
                l[keys[4]] = ''
    
    return leaders

def getLeaders(content,unitTextId):
    if unitTextId == ppsvar.CZSW_TEXTID:
        return getCzswLeaders(content)
    else:
        return getUnitLeaders(content)

def getPhones(content):
    """
    Funkcja pobiera dane o waznych telefonach
    
    Zwraca tablise slownikow
    """
    soup = BeautifulSoup(content)
    phones = []
    
    try:
        mdiv = soup.find('div', class_=ppsvar.PHONES_CLASS)
        divs = mdiv.div.find_all('div')
    except AttributeError as e:
        raise PhonesParseError(e)
    else:
        for d in divs:
            pname = d.b.extract()
            pname = (pname.get_text().strip())[:-1]
            
            pnumber = d.get_text().strip()
            
            phone = {ppsvar.PHONE_NAME:pname,
                     ppsvar.PHONE_NUMBER:pnumber}
            phones.append(phone)
    
    return phones
