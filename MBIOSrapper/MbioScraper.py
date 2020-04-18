from typing import List
from GenericScraper import GenericScraper
from dataTypes.PaperData import PaperData
from dateutil import parser

MBIO_URL_NO_PAGE = 'https://mbio.asm.org/latest'
MBIO_URL = 'https://mbio.asm.org/latest?page='

class MbioScraper(GenericScraper):
    def getPapersFromContent(self, content) -> List[PaperData]:
        paperFromData = lambda paper: PaperData(
            paper.find('a', attrs={"class": "highwire-cite-linked-title"}).text,
            "https://mbio.asm.org" + paper.find('a')['href'],
            parser.parse(paper.find('div', attrs={"class": "highwire-cite-metadata"}).text)
        )
        return list(
            map(
                paperFromData,
                filter(
                    lambda auxContent: 'research' in
                    auxContent.find('div', {'class': 'highwire-cite-overline'}).text.lower(),
                    content.findAll('div', attrs={"class": "highwire-cite-col highlight-right-col"})
                )
            )
        )

    def getPaperParagraphs(self, content) -> List[any]:
        return list(content.find(
            'div', {'class': 'abstract'}
        ))

if __name__ == "__main__":
    for i in MbioScraper().getPapersFromUrl('https://mbio.asm.org/latest'):
        print(i.title)
        print(i.dateTime)
