import pandas as pd
from selenium import webdriver
import numpy as np
import time
from typing import List
from dataTypes.PaperData import PaperData
from utils.PaperJsonEncoder import PaperJsonEncoder
import json
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys

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
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    if(sys.platform == 'linux'):
        google_drive = "./chromedriver"
    else:
        google_drive = ".\\GoogleScholarScrapper\\chromedriver_win32\\chromedriver.exe"

    driver = webdriver.Chrome(google_drive, chrome_options=options)
    link_to_search = "https://scholar.google.com/scholar?start=0&hl=es&as_sdt=0,5&q={0}".format(key_words)
    print(link_to_search)
    driver.get(link_to_search)
    next_page = True
    page_num = 0
    stop = num_pages
    df_elements = pd.DataFrame({"name": [], "link": []})
    while next_page:
        link_to_ordered = link_to_search.replace("start=0", "start=" + str(page_num * 10))
        wait = WebDriverWait(driver,20)
        #time.sleep(5)
        wait.until(EC.presence_of_element_located((By.ID,'gs_res_ccl_mid')))
        search_list_paper = driver.find_elements_by_xpath('//*[@id="gs_res_ccl_mid"]//div//h3//a')
        #all_papers_page = search_list_paper.find_elements_by_tag_name("div")
        for i in search_list_paper:
            try:
                # Aquí no se están obteniendo siempre los links correctos
                #name = i.find_element_by_tag_name("h3").get_attribute("text")
                name = i.get_attribute('textContent')
                link = i.get_attribute('href')
                #link = i.find_element_by_tag_name("h3").get_attribute("href")
                #print(name)
                #print(link)
                temp = pd.DataFrame({"name": [name], "link": [link]})
                #print(temp)
                df_elements = df_elements.append(temp, ignore_index=True)
                #print(df_elements)
            except:
                continue
        page_num += 1
        df_results = clean_results(df_elements)
        #time.sleep(np.random.uniform(11, 17))
        #driver.quit()
        #driver = webdriver.Chrome(google_drive)
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
    for i in range(df.size):
        try:
            list.append(PaperData(df.iloc[i][0], df.iloc[i][1]))
        except:
            continue
    return list
    #return savePapersToJsonFile(list)


def savePapersToJsonFile(paperArray: List[PaperData]) -> None:
    with open('googleScholarData.json', 'w') as outfile:
        json.dump(paperArray, outfile, cls=PaperJsonEncoder)


#getPapersFromGoogleScholar(1, ["covid+mask+register"])
