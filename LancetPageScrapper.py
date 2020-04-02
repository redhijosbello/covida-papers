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

# Este método simplemente abre el paper si es que contiene la palabra buscada
# Inputs: Url que contiene el título buscado, word_in_paper la palabra que se busca en paper
# Output None

def analyzePaperContent(url,word_in_paper):
    open_page = False
    response = requests.get(url,timeout=10)
    content = BeautifulSoup(response.content, "html.parser")
    result = content.find_all("div", {"class":"section-paragraph"}) #Se obtienen todos los parrafos del paper
    for res in result:
        if res.text.find(word_in_paper) != -1:                      #Si tiene la palabra entonces se abre el paper
            open_page = True 
            break
    if open_page == True:
        webbrowser.open(url)
    """ No está implementado aún el descargar automáticamente el paper a local
    descarga = content.findAll('div', attrs={"class": "article-tools__holder pull-right"})
    for i in descarga:
        link = descarga.find('a')['href']
        webbrowser.open("https://www.thelancet.com" + link)
    """  
    
# Función que scrappea la página principal de Lancet en búsqueda de palabras claves en el título
# Palabra que se busca en titulo, palabra que se busca en el paper.
        
def lancetScrapping(word_in_title, word_in_paper):
    url = "https://www.thelancet.com/coronavirus"
    response = requests.get(url,timeout=10)
    content = BeautifulSoup(response.content, "html.parser")
    paperArray = []
    for paper in content.findAll('div', attrs={"class": "articleCitation"}):
        paperObject = {
            "title": paper.find('h4', attrs={"class": "title"}).text,
            "link": "https://www.thelancet.com" + paper.find('a')['href'] 
        }
        paperArray.append(paperObject)
    
    with open('lancetSearchData.json', 'w') as outfile:
        json.dump(paperArray, outfile)
              
    with open('lancetSearchData.json') as json_data:
        jsonData = json.load(json_data)

    for i in jsonData:
        if i['title'].find(word_in_title)!=-1:
            print("El título del paper es: " + i['title'])
            analyzePaperContent(i['link'], word_in_paper)  

# Ejecución
lancetScrapping("mask", "COVID-19")