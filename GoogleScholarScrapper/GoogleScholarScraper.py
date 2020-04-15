from typing import List
from dataTypes.PaperData import PaperData
from GenericScraper import GenericScraper

class GoogleScholarScrapper(GenericScraper):
    def getPapersFromContent(self, content) -> List[PaperData]:
        paperFromData = lambda paper: PaperData(
            paper.h3.a.text,
            paper.h3.a.attrs['href']
        )

        return list(map(
            paperFromData,
            filter(
                lambda paper: paper.h3 is not None and paper.h3.a is not None,
                content.find(id='gs_res_ccl_mid').findAll('div', recursive=False)
            )
        ))

    def getPaperParagraphs(self, content) -> List[any]:
        raise Exception("Shouldn't be called.")

    def getPapersFromGoogleScholar(self, num_pages, *argv) -> List[PaperData]:
        key_words = "+".join(argv)
        link_to_search = "https://scholar.google.com/scholar?hl=es&as_sdt=0,5&q={0}&start=".format(key_words)
        return self.getPapersFromPaginatedUrl(
            url=link_to_search,
            initIdx=0,
            lastIdx=num_pages*10 - 1,
            step=10
        )

if __name__ == "__main__":
    GoogleScholarScrapper().getPapersFromGoogleScholar(1, "covid", "mask")
