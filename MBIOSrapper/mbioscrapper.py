import webbrowser
from bs4 import BeautifulSoup
import requests
import json
from typing import List
from dataTypes.PaperData import PaperData
from utils.PaperJsonEncoder import PaperJsonEncoder



# Función simple que scrappea los últimos artículos de la página "https://mbio.asm.org" para revisar si en los títulos
# está la palabra entregada como parámetro y si está lo que se quiere buscar en el texto del paper, sirve como guia para empezar
# un Scrapping más complejo
# La función escribe un archivo .json con el título y el link de referencia del paper si contiene la palabra en el titulo

def mbioScrappingAndOpenLinks(word_in_title: str, word_in_paper: str) -> None:
    paperArray = getPapersFromMbio()
    savePapersToJsonFile(paperArray)
    papersOfInterest = filterPapersOfInterest(
        paperArray,
        word_in_title,
        word_in_paper
    )
    openPapersInBrowser(papersOfInterest)


def getPapersFromMbio() -> List[PaperData]:
    url = "https://mbio.asm.org/latest"
    return getPapersFromUrl(url)


def getMbioPapersOfInterest(word_in_title: str, word_in_paper: str) -> List[PaperData]:
    paperArray = getPapersFromMbio()
    return filterPapersOfInterest(
        paperArray,
        word_in_title,
        word_in_paper
    )


def openPapersInBrowser(papers: List[PaperData]) -> None:
    for paper in papers:
        print("El título del paper es: " + paper.title)
        webbrowser.open(paper.link)


def filterPapersOfInterest(
        papers: List[PaperData],
        word_in_title: str,
        word_in_paper: str) -> List[PaperData]:
    papersTitleMatches = filter(
        lambda paper: paper.title.lower().find(word_in_title) != -1,
        papers
    )
    return list(filter(
        lambda paper: isPaperContentOfInterest(paper.link, word_in_paper),
        papersTitleMatches
    ))


def isPaperContentOfInterest(url: str, word_in_paper: str) -> bool:
    response = requests.get(url, timeout=10)
    content = BeautifulSoup(response.content, "html.parser")
    results = list(content.find('div', {'class': 'abstract'}))
    return isWordInResults(word_in_paper, results)


def isWordInResults(word: str, results: List[any]) -> bool:
    isWordInText = lambda res: res.text.lower().find(word) != -1
    return any(map(isWordInText, results))


def getPapersFromUrl(url: str) -> List[PaperData]:
    response = requests.get(url, timeout=10)
    content = BeautifulSoup(response.content, "html.parser")
    return getPapersFromContent(content)

# Cambiar esta función
def getPapersFromContent(content) -> List[PaperData]:

    paperFromData = lambda paper: PaperData(
        paper.find('a', attrs={"class": "highwire-cite-linked-title"}).text,
        "https://mbio.asm.org" + paper.find('a')['href']
    )

    return list(map(
        paperFromData,
        content.findAll('div', attrs={"class": "highwire-cite-col highlight-right-col"})
    ))


def savePapersToJsonFile(paperArray: List[PaperData]) -> None:
    with open('mbioSearchData.json', 'w') as outfile:
        json.dump(paperArray, outfile, cls=PaperJsonEncoder)

def getMbioPapersOfInterestInTitle(word: str):
    result = getPapersFromMbio()
    list = []
    for res in result:
        if res.title.find(word)!=-1:
            list.append(res)
    savePapersToJsonFile(list)

mbioScrappingAndOpenLinks('virus', 'covid-19')
