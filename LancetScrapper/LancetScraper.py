# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 13:54:55 2020

@author: Matias
"""

from typing import List
from GenericScraper import GenericScraper
from dataTypes.PaperData import PaperData

LANCET_URL = 'https://www.thelancet.com/coronavirus'

class LancetScraper(GenericScraper):
    def getPapersFromContent(self, content) -> List[PaperData]:
        paperFromData = lambda paper: PaperData(
            paper.find('h4', attrs={"class": "title"}).text,
            "https://www.thelancet.com" + paper.find('a')['href']
        )
        return list(map(
            paperFromData,
            content.findAll('div', attrs={"class": "articleCitation"})
        ))

    def getPaperParagraphs(self, content) -> List[any]:
        return content.find_all(
            "div", {"class": "section-paragraph"}
        )   # Se obtienen todos los parrafos del paper

# LancetScraper().scrappingAndOpenLinks(LANCET_URL, 'mask', 'covid-19')
