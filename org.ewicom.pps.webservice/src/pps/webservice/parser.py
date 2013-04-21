# -*- coding: utf8 -*-
'''
Modul udostepnia dane do parsowania strony sw.gov.pl

@author: Marcin Kunicki
@contact: masel.popowo@gmail.com

@version: 0.1
'''
from bs4 import BeautifulSoup

def getUnitsNextPageLink(content):
    """
    Funkcja pobiera link do nastepnej strony z jednostkami
    
    Zwraca link do nastepnej strony
    """
    soup = BeautifulSoup(content)
    
    link = soup.find('a', text="Następna")
    
    if link is not None:
        return 'http://sw.gov.pl' + link['href']
    else:
        return None

def getUnitsLinks(content):
    """
    Funkcja pobiera linki do stron jednostek podstawowych
    
    Zwraca liste linkow
    """
    soup = BeautifulSoup(content)
    
    divs = soup.find_all('div', class_='left')
    links = ['http://sw.gov.pl' + div.a['href'] for div in divs]
    
    return links

def getUnitIdAndParent(link):
    """
    Funkcja pobiera id jednostki i id rodzica
    
    Zwraca slownik z id
    """
    part = link.split('/')
    
    unit = part[-2]
    parent = part[-3]
    
    if unit == 'centralny-zarzad-sw' or parent == 'pl':
        d = {'unit_id':unit, 'parent_id':unit}
    else:
        d = {'unit_id':unit, 'parent_id':parent}
    
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

def getShortUnitName(content):
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
        s = {'unit_latitude':None, 'unit_longitude':None}
    
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
    
    d = {'unit_street':unit_street, 'unit_postcode':unit_postcode, 'unit_city':unit_city, 'unit_phone':unit_phone, 'unit_email':unit_email}
        
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
        unit_simg = 'http://sw.gov.pl/pl' + a['href']
        unit_img = 'http://sw.gov.pl/pl' + a.img['src']
    else:
        unit_simg = None
        unit_img = None
    
    d = {'unit_simg':unit_simg, 'unit_img':unit_img}
    return d

def getDefaultDescription(content):
    """
    Funkcja pobiera opis podstawowy jednostki
    
    Zwraca string
    """
    soup = BeautifulSoup(content)
    
    desc = soup.find(id='opispodstawowy')
    
    if desc is not None:
        return desc.get_text()
    else:
        return None

def getLeaders(content):
    """
    Funkcja pobiera dane o kierownictwie
    
    Zwraca liste kierownictwa
    """
    soup = BeautifulSoup(content)
    
    mdiv = soup.find('div', class_='praca-margines tab-leaders-content')
    
    divs = mdiv.find_all('div')

    keys = {1:'position', 2:'name', 3:'phone', 4:'email'}
    
    if not divs:
        print 'Brak danych dla kierwonictwa'
    else:
        i = 1
        leaders = []
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
    
    return leaders
