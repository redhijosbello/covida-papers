import abc
import json
import webbrowser
from typing import List

import requests
from bs4 import BeautifulSoup

from dataTypes.PaperData import PaperData
from utils.PaperJsonEncoder import PaperJsonEncoder

# Clase simple que scrappea los últimos artículos de una página, por ej. "https://mbio.asm.org" para revisar si en
# los títulos está la palabra entregada como parámetro y si está lo que se quiere buscar en el texto del paper,
# sirve como guia para empezar un Scrapping más complejo La función escribe un archivo .json con el título y el link
# de referencia del paper si contiene la palabra en el titulo
from utils.utils import flatmap


class GenericScraper(metaclass=abc.ABCMeta):
	def scrappingAndOpenLinks(
			self,
			url: str,
			word_in_title: str,
			word_in_paper: str) -> None:
		paperArray = self.getPapersFromUrl(url)
		self.savePapersToJsonFile(paperArray)
		papersOfInterest = self.filterPapersOfInterest(
			paperArray,
			word_in_title,
			word_in_paper
		)
		self.openPapersInBrowser(papersOfInterest)

	def getPapersOfInterest(
			self,
			url: str,
			word_in_title: str,
			word_in_paper: str) -> List[PaperData]:
		paperArray = self.getPapersFromUrl(url)
		return self.filterPapersOfInterest(
			paperArray,
			word_in_title,
			word_in_paper
		)

	def filterPapersOfInterest(
			self,
			papers: List[PaperData],
			word_in_title: str,
			word_in_paper: str) -> List[PaperData]:

		papersTitleMatches = filter(
			lambda paper: paper.title.lower().find(word_in_title.lower().strip()) != -1,
			papers
		)
		return list(filter(
			lambda paper: self.isPaperContentOfInterest(paper.link, word_in_paper),
			papersTitleMatches
		))

	def getPapersOfInterestPaginatedSource(
			self,
			url: str,
			startIdx: int,
			endIdx: int,
			word_in_title: str,
			word_in_paper: str,
			step: int = 1) -> List[PaperData]:
		paperArray = self.getPapersFromPaginatedUrl(url, startIdx, endIdx, step=step)
		return self.filterPapersOfInterest(
			paperArray,
			word_in_title,
			word_in_paper
		)

	def isPaperContentOfInterest(self, url: str, word_in_paper: str) -> bool:
		response = requests.get(url, timeout=10)
		content = BeautifulSoup(response.content, "html.parser")
		results = self.getPaperParagraphs(content)  # Se obtienen todos los parrafos del paper
		return self.isWordInResults(word_in_paper, results)

	def getPapersFromUrl(self, url: str) -> List[PaperData]:
		response = requests.get(url, timeout=10)
		content = BeautifulSoup(response.content, "html.parser")
		return self.getPapersFromContent(content)

	def getPapersFromPaginatedUrl(self, url: str, initIdx: int, lastIdx: int, step: int=1) -> List[PaperData]:
		urlArray = map(
			lambda idx: url + str(idx),
			range(initIdx, lastIdx + 1, step)
		)
		return list(flatmap(
			lambda aUrl: self.getPapersFromUrl(aUrl),
			urlArray
		))

	@classmethod
	def savePapersToJsonFile(cls, paperArray: List[PaperData]) -> None:
		with open('lancetSearchData.json', 'w') as outfile:
			json.dump(paperArray, outfile, cls=PaperJsonEncoder)

	@classmethod
	def isWordInResults(cls, word: str, results: List[any]) -> bool:
		isWordInText = lambda res: res.text.lower().find(word.lower().strip()) != -1
		return any(map(isWordInText, results))

	@classmethod
	def openPapersInBrowser(cls, papers: List[PaperData]) -> None:
		for paper in papers:
			print("El título del paper es: " + paper.title)
			webbrowser.open(paper.link)

	@abc.abstractmethod
	def getPapersFromContent(self, content) -> List[PaperData]:
		pass

	@abc.abstractmethod
	def getPaperParagraphs(self, content):
		pass
