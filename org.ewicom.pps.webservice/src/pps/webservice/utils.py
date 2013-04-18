# -*- coding: utf8 -*-
'''
Modul zawiera pomocnicze funkcje dla pakietu

@author: Marcin Kunicki
@contact: masel.popowo@gmail.com

@version: 0.1
'''
import urllib2

def getContent(url):
    """
    Funkcja pobiera strone na podstawie podanego url
    
    Zwraca pobrana strone
    """
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
    else:
        page = response.read()
        return page

def saveUnitsLinksToFile(linkList):
    """
    Funkacja zapisuje do pliku liste linkow do jednostek
    
    """
    fileName = 'links.txt'
    
    try:
        f = open(fileName,'a')
    except IOError:
        print 'blad dostepu do pliku'
    else:
        f.write('\n'.join(linkList))
        f.close()

def saveScriptInfo(info):
    """
    Funkcja zapisuje inforacje z wykonania skryptu. Funkcja potrzebuje stringa
    """
    
    fileName = 'info.txt'
    
    try:
        f = open(fileName,'a')
    except IOError:
        print 'blad dostepu do pliku'
    else:
        f.write(info)
        f.close()

def getFirstUnitLink():
    """
    Funkcja pobiera pierwszy link z jednostką w pliku links.txt
    
    Zwraca link do jednostki
    """
    
    fileName = 'links.txt'
    
    try:
        f = open(fileName,'r')
        link = f.readline()
        link = link.strip()
    except IOError:
        print 'Blad dostepu do pliku: '+fileName
    else:
        f.close()
        return link

def deleteFirstUnitLink():
    """
    Funkcja usuwa pierwszy link z pliku links.txt
    
    """
    fileName = 'links.txt'
    
    try:
        f = open(fileName,'r')
        links = f.readlines()
        f.close()
        f = open(fileName,'w')
        f.write(''.join(links[1:]))
    except IOError:
        print 'Blad dostepu do pliku: '+fileName
    else:
        f.close()
