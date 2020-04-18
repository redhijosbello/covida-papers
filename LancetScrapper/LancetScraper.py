# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 13:54:55 2020

@author: Matias
"""

from typing import List
from GenericScraper import GenericScraper
from dataTypes.PaperData import PaperData
from dateutil import parser
LANCET_URL = 'https://www.thelancet.com/coronavirus'

class LancetScraper(GenericScraper):
    def getPapersFromContent(self, content) -> List[PaperData]:
        paperFromData = lambda paper: PaperData(
            paper.find('h4', attrs={"class": "title"}).text,
            "https://www.thelancet.com" + paper.find('a')['href'],
            parser.parse(paper.find('div', attrs={"class": "published-online"}).text.strip()[11:]) if paper.find('div', attrs={"class": "published-online"}) is not None else "None dateTime finded"
        )
        return list(map(
            paperFromData,
            content.findAll('div', attrs={"class": "articleCitation"})
        ))

    def getPaperParagraphs(self, content) -> List[any]:
        return content.find_all(
            "div", {"class": "section-paragraph"}
        )   # Se obtienen todos los parrafos del paper

if __name__ == "__main__":
    for i in LancetScraper().getPapersFromUrl("https://www.thelancet.com/coronavirus"):
        if i.dateTime is not None:
            print(i.dateTime)
