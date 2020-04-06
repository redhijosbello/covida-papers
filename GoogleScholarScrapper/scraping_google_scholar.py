#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
import numpy as np
import time


# In[3]:


google_scholar = "https://scholar.google.com/scholar?start=0&hl=es&as_sdt=0,5&q={0}"

google_drive = r"D:\proyectos\scraper_proyecto\chromedriver_win32\chromedriver.exe"

xpath_search ='//*[@id="gs_hdr_tsi"]'

xpath_list_paper = '//*[@id="gs_res_ccl_mid"]'

order_date = '//*[@id="gs_bdy_sb_in"]/ul[1]/li[2]/a'

key_words = ["covid+mask+register"]


# In[ ]:



def clean_results(df_result):
    """
    Cleaning dataframe with title and link for paper
    """
    
    df_result.dropna(inplace=True)
    df_result.drop_duplicates(inplace=True)
    df_result.drop_duplicates(subset="link", keep=False,inplace=True)
    df_result.drop_duplicates(subset="name",keep=False, inplace=True)

    df_result = df_result[df_result["name"] != '']
    df_result = df_result[df_result["link"] != '']
    df_result = df_result[df_result["link"] != 'javascript:void(0)']
    df_result = df_result.reset_index().groupby(["name","link","num_page"]).count().reset_index()
    df_result = df_result[df_result["index"]==1].drop(columns={"index"})
    return df_result


driver = webdriver.Chrome(google_drive) 
## Initializae google scholar webpage
link_to_search = google_scholar.format(key_words[0])
driver.get(link_to_search)
next_page = True
page_num = 1
stop = 50
df_elements = pd.DataFrame({"name":[],"link":[],"num_page":[]})
# the next loop tried to obtain onformation from all the index pages sadly it doesn't have information to stop
# I added an stoper at 50 pages
while next_page:

    link_to_ordered = link_to_search.replace("start=0","start="+str(page_num*10))
    
    time.sleep(10) 
    search_list_paper = driver.find_element_by_xpath(xpath_list_paper) 
    all_papers_page = search_list_paper.find_elements_by_tag_name("div")
    elements_in = 0
    for i in all_papers_page: 
        try:
            elements_in += 1
            name = i.find_element_by_tag_name("a").get_attribute("text")
            link = i.find_element_by_tag_name("a").get_attribute("href")
            temp = pd.DataFrame({"name":[name],"link":[link], "num_page":[page_num]})
            df_elements = df_elements.append(temp, ignore_index=True)
        except:
            continue
    print("elements in this page: ", elements_in)
    page_num += 1        
    df_results = clean_results(df_elements)
    time.sleep(np.random.uniform(11,17)) 

    driver.quit()
    driver = webdriver.Chrome(google_drive) 
    driver.get(link_to_ordered)
    try:
        driver.get(link_to_ordered)
        next_page = True
    except:
        next_page = False
    # stoping process   
    if page_num == stop:
        next_page = False
        
df_results.to_csv("articles_related_with_covid_mask.csv")


driver.quit()

