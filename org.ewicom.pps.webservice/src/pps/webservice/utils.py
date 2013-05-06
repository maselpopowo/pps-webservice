# -*- coding: utf8 -*-
'''
Modul zawiera pomocnicze funkcje dla pakietu

@author: Marcin Kunicki
@contact: masel.popowo@gmail.com

@version: 0.1
'''
import urllib2
from pps.webservice import ppsvar
import datetime

def getContent(url):
    """
    Funkcja pobiera strone na podstawie podanego url
    
    Zwraca pobrana strone
    """
    if url is not None:
        request = urllib2.Request(url)
        
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
        except ValueError as e:
            print 'Problem z adresem strony: ', e
            return None
        else:
            page = response.read()
            return page
    else:
        return None

def getDBSettings():
    """
    Funkcja zwraca dsn dla polaczenia z baza na podstawie pliku
    """
    try:
        f = open(ppsvar.DB_SETTINGS_FILE,'r')
        lines = [line.strip() for line in f]
    except IOError:
        print 'Blad dostepu do pliku: '+ppsvar.DB_SETTINGS_FILE
    else:
        f.close()
        return ' '.join(lines)

def saveUnitsLinksToFile(linkList):
    """
    Funkacja zapisuje do pliku liste linkow do jednostek
    
    """
    if linkList:
        try:
            f = open(ppsvar.LINKS_FILE,'a')
        except IOError:
            print 'blad dostepu do pliku'
        else:
            f.write('\n'.join(linkList))
            f.close()

def log(info):
    """
    Funkcja logujaca
    """
    try:
        f = open(ppsvar.LOG_FILE,'a')
    except IOError:
        print 'Blad dostepu do pliku z funkcji logujacej'
    else:
        f.write(str(datetime.datetime.now())+' '+info+'\n')
        f.close()

def getFirstUnitLink():
    """
    Funkcja pobiera pierwszy link z jednostką w pliku links.txt
    
    Zwraca link do jednostki
    """
    try:
        f = open(ppsvar.LINKS_FILE,'r')
        link = f.readline()
        link = link.strip()
    except IOError:
        print 'Blad dostepu do pliku: '+ppsvar.LINKS_FILE
    else:
        f.close()
        return link

def deleteFirstUnitLink():
    """
    Funkcja usuwa pierwszy link z pliku links.txt
    
    """
    try:
        f = open(ppsvar.LINKS_FILE,'r')
        links = f.readlines()
        f.close()
        
        f = open(ppsvar.LINKS_FILE,'w')
        f.write(''.join(links[1:]))
    except IOError:
        print 'Blad dostepu do pliku: '+ppsvar.LINKS_FILE
    else:
        f.close()
