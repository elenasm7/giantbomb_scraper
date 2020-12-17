import time
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
# import cv2
import numpy as np 
import pandas as pd
import re
import urllib
import pickle
# import query
import re


import random

def get_data_from_page(rows,games_dict):
    game_d = {}
    for row in rows:
        for lab in ['Name','First release date','Platfrom',
                    'Developer','Publisher','Genre','Theme',
                    'Franchise','Aliasses']:
            if lab in row.text:
                if lab == 'First release date':
                    game_d[lab] = row.find('td').find('span').text
                elif lab == 'Genre' or lab == 'Platfrom':
                    if len(row.find('td').findAll('a')) > 1:
                        game_d[lab] = [i.text for i in rows[10].find('td').findAll('a')]
                    else:
                        game_d[lab] = row.find('td').find('a').text
                else:
                    try:
                        game_d[lab] = row.find('td').find('a').text
                    except:
                        game_d[lab] = None
    return game_d

def get_game_details(title,driver,games_dict):
    time.sleep(random.randint(0,2))
    search_results = driver.find_elements_by_class_name('media')
    search_results[0].click()
    time.sleep(random.randint(0,2))
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    rows = soup.findAll('tr')
    games_dict[title] = get_data_from_page(rows,games_dict)
    return 'done'

def save_pickle(file_name,obj):
    with open(file_name, 'wb') as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return file_name + ' is saved'

def open_pickle(file_name):
    with open(file_name, 'rb') as handle:
        obj = pickle.load(handle)
    return obj
    

# DB_CONNECTION = query.get_db_connection('../../../.supreme_db_creds.pkl','Sandbox_Elena_Morais',dbhost='centaur')

# all_tables = {}

# for region in ['USA','EU']:
#     for yr in range(2013,2021):
#         title = f'{region}_VGT_{yr}_Table_update'
#         all_tables[title] = query.return_table(DB_CONNECTION,'Sandbox_Elena_Morais',title)

# tabs = []
# for tab in all_tables.keys():
#     tabs.append(all_tables[tab][['title','publisher','franchise_update']])
    
# full_table = pd.concat(tabs)

# titles = list(set(full_table.title.to_list()))
# 

titles = open_pickle('set_of_titles.pkl')

games_dict = {}

driver = webdriver.Chrome(executable_path='/Users/elena.morais/Documents/chromedriver_2') 
driver.get('https://www.giantbomb.com')

time.sleep(60)

for title in titles:
    print(title)

    # time.sleep(random.randint())
    time.sleep(random.randint(2,5))
    driver.find_element_by_xpath('//div[@data-toggle="search"]').click()
    time.sleep(random.randint(0,2))
    driver.find_element_by_xpath('//input[@class="js-site-search-query"]').send_keys(title)
    time.sleep(random.randint(0,2))
    driver.find_element_by_xpath('//input[@class="js-site-search-query"]').send_keys(u'\ue007')

    get_game_details(title,driver,games_dict)