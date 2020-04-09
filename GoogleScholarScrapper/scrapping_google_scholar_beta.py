import pandas as pd
from selenium import webdriver
import numpy as np
import time
from typing import List
from dataTypes.PaperData import PaperData
from utils.PaperJsonEncoder import PaperJsonEncoder
import json

def clean_results(df_result):
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


def getPapersFromGoogleScholar(num_pages, key_words) -> List[PaperData]:
    return getPapersFromUrl(num_pages, key_words)


def getPapersFromUrl(num_pages, key_words) -> List[PaperData]:
    google_drive = ".\\chromedriver_win32\\chromedriver.exe"
    driver = webdriver.Chrome(google_drive)
    link_to_search = "https://scholar.google.com/scholar?start=0&hl=es&as_sdt=0,5&q={0}".format(key_words[0])
    driver.get(link_to_search)
    next_page = True
    page_num = 1
    stop = num_pages
    df_elements = pd.DataFrame({"name": [], "link": []})
    while next_page:
        link_to_ordered = link_to_search.replace("start=0", "start=" + str(page_num * 10))
        time.sleep(10)
        search_list_paper = driver.find_element_by_xpath('//*[@id="gs_res_ccl_mid"]')
        all_papers_page = search_list_paper.find_elements_by_tag_name("div")
        for i in all_papers_page:
            try:
                # Aquí no se están obteniendo siempre los links correctos

                name = i.find_element_by_tag_name("a").get_attribute("text")
                link = i.find_element_by_tag_name("a").get_attribute("href")
                temp = pd.DataFrame({"name": [name], "link": [link]})
                df_elements = df_elements.append(temp, ignore_index=True)
            except:
                continue
        page_num += 1
        df_results = clean_results(df_elements)
        time.sleep(np.random.uniform(11, 17))
        driver.quit()
        driver = webdriver.Chrome(google_drive)
        driver.get(link_to_ordered)
        try:
            driver.get(link_to_ordered)
            next_page = True
        except:
            next_page = False
        if page_num >= stop:
            next_page = False
    return getPapersFromDF(df_results)


def getPapersFromDF(df) -> List[PaperData]:
    list = []
    for i in range(df.shape[0]):
        list.append(PaperData(df.iloc[i][0], df.iloc[i][1]))
    return savePapersToJsonFile(list)


def savePapersToJsonFile(paperArray: List[PaperData]) -> None:
    with open('googleScholarData.json', 'w') as outfile:
        json.dump(paperArray, outfile, cls=PaperJsonEncoder)


getPapersFromGoogleScholar(1, ["covid+mask+register"])