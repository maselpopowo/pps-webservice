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
    
    link = soup.find('a',text="Następna")
    
    if link is not None:
        return 'http://sw.gov.pl'+link['href']
    else:
        return None

def getUnitsLinks(content):
    """
    Funkcja pobiera linki do stron jednostek podstawowych
    
    Zwraca liste linkow
    """
    soup = BeautifulSoup(content)
    
    divs = soup.find_all('div', class_='left')
    links = ['http://sw.gov.pl'+div.a['href'] for div in divs]
    
    return links
