from typing import List
from GenericScraper import GenericScraper
from dataTypes.PaperData import PaperData

ARXIV_URL = 'https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=COVID-19&terms-0-field=title&terms-1-operator=OR&terms-1-term=SARS-CoV-2&terms-1-field=abstract&terms-3-operator=OR&terms-3-term=COVID-19&terms-3-field=abstract&terms-4-operator=OR&terms-4-term=SARS-CoV-2&terms-4-field=title&terms-5-operator=OR&terms-5-term=coronavirus&terms-5-field=title&terms-6-operator=OR&terms-6-term=coronavirus&terms-6-field=abstract&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=200&order=-announced_date_first&source=home-covid-19'

class ArxivScraper(GenericScraper):
    def getPapersFromContent(self, content) -> List[PaperData]:
        paperFromData = lambda paper: PaperData(
            paper.find('p', attrs={"class": "title is-5 mathjax"}).text,
            paper.find('a')['href']
        )
        return list(map(
            paperFromData,
            content.findAll('li', attrs={"class": "arxiv-result"})
        ))

    def getPaperParagraphs(self, content) -> List[any]:
        return content.find_all(
            "p",
            {"class": "abstract mathjax"}
        )   # Se obtienen todos los parrafos del paper





