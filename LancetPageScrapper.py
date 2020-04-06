# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 13:54:55 2020

@author: Matias
"""

# Función simple que scrappea la página https://www.thelancet.com/coronavirus para revisar si en los títulos
# está la palabra entregada como parámetro y si está lo que se quiere buscar en el texto del paper, sirve como guia para empezar
# un Scrapping más complejo
# La función escribe un archivo .json con el título y el link de referencia del paper si contiene la palabra en el titulo
# Requerimientos: pip install bs4, pip install requests.

import webbrowser
from bs4 import BeautifulSoup
import requests
import json
from typing import List

# Este método simplemente abre el paper si es que contiene la palabra buscada
# Inputs: Url que contiene el título buscado, word_in_paper la palabra que se busca en paper
# Output None
from dataTypes.PaperData import PaperData
from utils.PaperJsonEncoder import PaperJsonEncoder

""" No está implementado aún el descargar automáticamente el paper a local
    descarga = content.findAll('div', attrs={"class": "article-tools__holder pull-right"})
    for i in descarga:
        link = descarga.find('a')['href']
        webbrowser.open("https://www.thelancet.com" + link)
"""
    
# Función que scrappea la página principal de Lancet en búsqueda de palabras claves en el título
# Palabra que se busca en titulo, palabra que se busca en el paper.

def lancetScrapping(word_in_title: str, word_in_paper: str) -> None:
    url = "https://www.thelancet.com/coronavirus"
    paperArray = getPapersFromUrl(url)
    savePapersToJsonFile(paperArray)
              
    papersOfInterest = filterPapersOfInterest(
        paperArray,
        word_in_title,
        word_in_paper
    )
    for paper in papersOfInterest:
        print("El título del paper es: " + paper.title)
        webbrowser.open(paper.link)

def filterPapersOfInterest(
        papers: List[PaperData],
        word_in_title: str,
        word_in_paper: str) -> List[PaperData]:

    papersTitleMatches = filter(
        lambda paper: paper.title.find(word_in_title) != -1,
        papers
    )
    return list(filter(
        lambda paper: isPaperContentOfInterest(paper.link, word_in_paper),
        papersTitleMatches
    ))

def isPaperContentOfInterest(url: str, word_in_paper: str) -> bool:
    response = requests.get(url, timeout=10)
    content = BeautifulSoup(response.content, "html.parser")
    results = content.find_all("div", {"class":"section-paragraph"}) #Se obtienen todos los parrafos del paper
    return isWordInResults(word_in_paper, results)

def isWordInResults(word: str, results: List[any]) -> bool:
    isWordInText = lambda res: res.text.find(word) != -1
    return any(map(isWordInText, results))

def getPapersFromUrl(url: str) -> List[PaperData]:
    response = requests.get(url, timeout=10)
    content = BeautifulSoup(response.content, "html.parser")
    return getPapersFromContent(content)

def getPapersFromContent(content) -> List[PaperData]:
    paperFromData = lambda paper: PaperData(
        paper.find('h4', attrs={"class": "title"}).text,
        "https://www.thelancet.com" + paper.find('a')['href']
    )
    return list(map(
        paperFromData,
        content.findAll('div', attrs={"class": "articleCitation"})
    ))

def savePapersToJsonFile(paperArray: List[PaperData]) -> None:
    with open('lancetSearchData.json', 'w') as outfile:
        json.dump(paperArray, outfile, cls=PaperJsonEncoder)

# Ejecución
lancetScrapping("mask", "COVID-19")