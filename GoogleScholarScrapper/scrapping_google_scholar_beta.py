import pandas as pd
from typing import List
from dataTypes.PaperData import PaperData
from utils.PaperJsonEncoder import PaperJsonEncoder
import json
import sys
import bs4
import os
import requests
import time
import pdb

class GoogleScholarScrapper():
    def clean_results(self,df_result):
        df_result.dropna(inplace=True)
        df_result.drop_duplicates(inplace=True)
        df_result.drop_duplicates(subset="link", keep=False, inplace=True)
        df_result.drop_duplicates(subset="name", keep=False, inplace=True)
        df_result = df_result[df_result["name"] != '']
        df_result = df_result[df_result["link"] != '']
        df_result = df_result[df_result["link"] != 'javascript:void(0)']
        df_result = df_result.reset_index().groupby(["name", "link"]).count().reset_index()
        df_result = df_result[df_result["index"] == 1].drop(columns={"index"})
        return df_result

    def getPapersFromUrl(self,num_pages, key_words) -> List[PaperData]:
        link_to_search = "https://scholar.google.com/scholar?start=0&hl=es&as_sdt=0,5&q={0}".format(key_words)
        print(link_to_search)
        next_page = True
        page_num = 0
        stop = num_pages
        df_elements = pd.DataFrame({"name": [], "link": []})
        while next_page:
            link_to_ordered = link_to_search.replace("start=0", "start=" + str(page_num * 10))
            resp = requests.get(link_to_ordered)
            page_soup = bs4.BeautifulSoup(resp.content, 'lxml')
            time.sleep(20)
            search_list_paper = [paper.h3.a for paper in page_soup.find(id='gs_res_ccl_mid').find_all('div') if paper.h3 is not None]
            if search_list_paper == []: #No more results
                next_page = False
                break
                
            for i in search_list_paper:
                try:
                    name = i.text
                    link = i.attrs['href']
                    temp = pd.DataFrame({"name": [name], "link": [link]})
                    df_elements = df_elements.append(temp, ignore_index=True)
                except:
                    continue
            page_num += 1
            df_results = self.clean_results(df_elements)
            if page_num >= stop:
                next_page = False
        return self.getPapersFromDF(df_results)

    def getPapersFromGoogleScholar(self,num_pages, *argv) -> List[PaperData]:
        key_words = ""
        for i in range(len(argv)):
            if i==len(argv)-1:
                key_words=key_words+argv[i]
            else:
                key_words=key_words+argv[i]+"+"
        print(key_words)
        return self.getPapersFromUrl(num_pages, key_words)

    def savePapersToJsonFile(self,paperArray: List[PaperData]) -> None:
        with open('googleScholarData.json', 'w') as outfile:
            json.dump(paperArray, outfile, cls=PaperJsonEncoder)

    def getPapersFromDF(self, df) -> List[PaperData]:
        list = []
        for i in range(df.size):
            try:
                list.append(PaperData(df.iloc[i][0], df.iloc[i][1]))
            except:
                continue
        self.savePapersToJsonFile(list)
        return list

#GoogleScholarScrapper().getPapersFromGoogleScholar(1, "covid","mask")
