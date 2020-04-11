from typing import List
from GenericScraper import GenericScraper
from dataTypes.PaperData import PaperData

MBIO_URL = 'https://mbio.asm.org/latest'

class MbioScraper(GenericScraper):
    def getPapersFromContent(self, content) -> List[PaperData]:
        paperFromData = lambda paper: PaperData(
            paper.find('a', attrs={"class": "highwire-cite-linked-title"}).text,
            "https://mbio.asm.org" + paper.find('a')['href']
        )
        return list(map(
            paperFromData,
            content.findAll('div', attrs={"class": "highwire-cite-col highlight-right-col"})
        ))

    def getPaperParagraphs(self, content) -> List[any]:
        return list(content.find('div', {'class': 'abstract'}))

# MbioScraper().scrappingAndOpenLinks(MBIO_URL, 'virus', 'covid-19')
