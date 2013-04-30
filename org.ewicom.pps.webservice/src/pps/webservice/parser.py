# -*- coding: utf8 -*-
'''
Modul udostepnia dane do parsowania strony sw.gov.pl

@author: Marcin Kunicki
@contact: masel.popowo@gmail.com

@version: 0.1
'''
from bs4 import BeautifulSoup
from pps.webservice import ppsvar

def getUnitsNextPageLink(content):
    """
    Funkcja pobiera link do nastepnej strony z jednostkami
    
    Zwraca link do nastepnej strony
    """
    soup = BeautifulSoup(content)
    
    link = soup.find('a', text=ppsvar.NEXT_PAGE_TEXT)
    
    if link is not None:
        return ppsvar.LINK_START_TEXT + link['href']
    else:
        return None

def getUnitsLinks(content):
    """
    Funkcja pobiera linki do stron jednostek podstawowych
    
    Zwraca liste linkow
    """
    soup = BeautifulSoup(content)
    
    divs = soup.find_all('div', class_='left')
    links = [ppsvar.LINK_START_TEXT + div.a['href'] for div in divs]
    
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
    
    unit_name = soup.find('div', class_='jednostka').h3.string
    
    if unit_name is None:
        raise NameError('No UnitName')
    else:
        return unit_name.strip()

def getUnitShortName(content):
    """
    Funkcja pobiera skrucona nazwe jednostki
    
    Zwrana skrucona nazwe jednostki
    """
    soup = BeautifulSoup(content)
    
    unit_sname_ns = soup.title.string
    unit_sname = unit_sname_ns.split('/')
    
    return unit_sname[-1].strip()

def getMapCoordinate(content):
    """
    Funkcja pobiera koordynaty na mapie
    
    Zwraca slownik lub None
    """
    soup = BeautifulSoup(content)
    
    unit_latitude = soup.find(id='mapka_Latitude')
    unit_longitude = soup.find(id='mapka_Longitude')
    
    if unit_latitude is not None or unit_longitude is not None:
        s = {'unit_latitude':unit_latitude['value'], 'unit_longitude':unit_longitude['value']}
    else:
        s = {'unit_latitude':'', 'unit_longitude':''}
    
    return s

def getBasicUnitInformations(content):
    """
    Funkcja pobiera dane podstawowe o jednostce - adres, tel, email
    
    Zwraca slownik
    """
    soup = BeautifulSoup(content)
    
    div = soup.find('div', class_='jednostka')
    p = div.find_all('p')
    
    unit_street = (p[0].string).strip()
    
    unit_tc = (p[1].string).strip()
    unit_postcode = unit_tc[0:6]
    unit_city = unit_tc[7:]
    
    unit_phone_p = p[2].string
    unit_phone = unit_phone_p[10:].strip()
    
    unit_email_p = p[3].string
    unit_email = unit_email_p[8:].strip()
    
    d = {ppsvar.UNIT_STREET:unit_street, ppsvar.UNIT_POSTCODE:unit_postcode, ppsvar.UNIT_CITY:unit_city, ppsvar.UNIT_PHONE:unit_phone, ppsvar.UNIT_EMAIL:unit_email}
        
    return d

def getUnitImages(content):
    """
    Funkcja pobiera linki do zdjec jednostki
    
    Zwaraca slownik z 2 linkami
    """
    soup = BeautifulSoup(content)
    
    div = soup.find('div', class_='pad')
    
    a = div.find('a')
    
    if a is not None:
        unit_simg = ppsvar.LINK_START_TEXT + a['href']
        unit_img = ppsvar.LINK_START_TEXT + a.img['src']
    else:
        unit_simg = ''
        unit_img = ''
    
    d = {ppsvar.UNIT_SIMG:unit_simg, ppsvar.UNIT_IMG:unit_img}
    return d

def getDefaultDescription(content):
    """
    Funkcja pobiera opis podstawowy jednostki
    
    Zwraca string
    """
    soup = BeautifulSoup(content)
    
    desc = soup.find(id=ppsvar.DEF_DESC_TEXT)
    
    if desc is not None:
        return desc.get_text()
    else:
        return ''

def getLeaders(content):
    """
    Funkcja pobiera dane o kierownictwie
    
    Zwraca liste kierownictwa
    """
    soup = BeautifulSoup(content)
    
    mdiv = soup.find('div', class_=ppsvar.LEADER_CLASS)
    
    divs = mdiv.find_all('div')

    keys = {1:ppsvar.LEADER_POSITION, 2:ppsvar.LEADER_NAME, 3:ppsvar.LEADER_PHONE, 4:ppsvar.LEADER_EMAIL}
    
    leaders = []
    if len(divs) == 1:
        return leaders
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
                leaders.append(l)
            else:
                l[keys[i]] = d.get_text().strip()
                i = i + 1
    
    for l in leaders:
        l[keys[3]] = (l[keys[3]])[10:]
        if len(l) == 4:
            l[keys[4]] = (l[keys[4]])[8:]
        else:
            l[keys[4]] = ''
    
    return leaders

def getPhones(content):
    """
    Funkcja pobiera dane o waznych telefonach
    
    Zwraca tablise slownikow
    """
    soup = BeautifulSoup(content)
    phones = []
    
    mdiv = soup.find('div', class_=ppsvar.PHONES_CLASS)
    
    #None dla bledu linku, strona inna niz jednostki
    if mdiv is not None:
        #None dla braku telefonow w jednostce
        if mdiv.div is not None:
            divs = mdiv.div.find_all('div')
            #sa telefony w jednostce  
            if divs:
                for d in divs:
                    pname = d.b.extract()
                    pname = (pname.get_text().strip())[:-1]
                    
                    pnumber = d.get_text().strip()
                    
                    phone = {ppsvar.PHONE_NAME:pname,ppsvar.PHONE_NUMBER:pnumber}
                    phones.append(phone)
    
    return phones
