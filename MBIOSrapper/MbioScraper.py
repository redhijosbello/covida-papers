from typing import List
from GenericScraper import GenericScraper
from dataTypes.PaperData import PaperData

MBIO_URL = 'https://mbio.asm.org/latest?page='

class MbioScraper(GenericScraper):
    def getPapersFromContent(self, content) -> List[PaperData]:
        paperFromData = lambda paper: PaperData(
            paper.find('a', attrs={"class": "highwire-cite-linked-title"}).text,
            "https://mbio.asm.org" + paper.find('a')['href']
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
        return list(content.find('div', {'class': 'abstract'}))

# MbioScraper().scrappingAndOpenLinks(MBIO_URL, 'virus', 'covid-19')
# MbioScraper().getPapersOfInterestPaginatedSource(
#         MBIO_URL,
#         startIdx=1,
#         endIdx=5,
#         word_in_title='covid',
#         word_in_paper='covid')
