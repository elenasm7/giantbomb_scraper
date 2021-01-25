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
import query
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
                        game_d[lab] = ','.join([i.text for i in row.find('td').findAll('a')])
                    elif row.find('td').find('a') == None:
                        game_d[lab] = None
                    else:
                        game_d[lab] = row.find('td').find('a').text    
                elif lab == 'Publisher':
                    if len(row.find('td').findAll('a')) > 1:
                        game_d['Publisher_extra'] = ','.join([i.text for i in row.find('td').findAll('a')])
                        game_d[lab] = row.find('td').find('a').text
                    elif row.find('td').find('a') == None:
                        game_d[lab] = None
                    else:
                        game_d[lab] = row.find('td').find('a').text
                else:
                    try:
                        game_d[lab] = row.find('td').find('a').text
                    except:
                        game_d[lab] = None
    return game_d

def get_game_details(title,driver,games_dict):
    t = title.split('(')[0]
    time.sleep(random.randint(2,5))
#     driver.find_element_by_partial_link_text(t).click()
    search_results = driver.find_elements_by_class_name('media')
    search_results[0].click()
    time.sleep(random.randint(0,2))
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    rows = soup.findAll('tr')
    games_dict[title] = get_data_from_page(rows,games_dict)
    return 'done'

def get_game_details_2(title,driver,games_dict):
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


#data to be taken care of:
hand_done_titles = open_pickle('hand_done_titles.pkl')

pages = {'Borderlands 2 (PS Vita)':'https://www.giantbomb.com/borderlands-2/3030-36055/',
 'Sonic Boom':'https://www.giantbomb.com/sonic-boom/3030-949/',
 'Pokemon X Version':'https://www.giantbomb.com/pokemon-xy/3030-41088/',
 "Madagascar 3: Europe's Most Wanted":'https://www.giantbomb.com/madagascar-3-the-video-game/3030-37449/',
 'Final Fantasy XV Windows Edition':'https://www.giantbomb.com/final-fantasy-xv/3030-21006/',
 'Dungeons & Dragons: Neverwinter':'https://www.giantbomb.com/neverwinter/3030-32417/',
 'Minecraft: Wii U Edition':'https://www.giantbomb.com/minecraft/3030-30475/',
 'DriveClub Bikes':'https://www.giantbomb.com/driveclub/3030-41693/',
 'Minecraft: PlayStation 3 Edition':'https://www.giantbomb.com/minecraft/3030-30475/',
 'Heavy Fire: The Chosen Few':'https://www.giantbomb.com/heavy-fire-afghanistan/3030-37010/',
 'Myst 3DS':'https://www.giantbomb.com/myst/3030-3970/',
 "Deadlight: Director's Cut":'https://www.giantbomb.com/deadlight/3030-37262/',
 'Sly Cooper Collection':"https://www.giantbomb.com/the-sly-collection/3030-31788/",
 'Minecraft: PS Vita Edition':"https://www.giantbomb.com/minecraft/3030-30475/",
 'Resident Evil: Revelations (console version)':"https://www.giantbomb.com/resident-evil-revelations/3030-31737/",
 'Dead Nation (PS Vita)':"https://www.giantbomb.com/dead-nation/3030-27866/",
 'Disgaea 1 Complete':"https://www.giantbomb.com/disgaea-hour-of-darkness/3030-18540/",
 'Code Name: S.T.E.A.M.':"https://www.giantbomb.com/code-name-s-t-e-a-m/3030-46597/",
 'Resident Evil Zero':"https://www.giantbomb.com/resident-evil-0/3030-10247/"}


if __name__ == "__main__":


    db_connection = query.get_db_connection('../../../.supreme_db_creds.pkl',
                                            'Sandbox_Elena_Morais',
                                            dbhost='centaur')
    
    db_table_name = 'Giantbomb_vgt_title_publisher_updates_new'

    titles = open_pickle('set_of_titles.pkl')
    skip_titles = list(pages.keys())
    st_2 = list(hand_done_titles.keys())
    skip_titles.extend(st_2)
    scraped_titles = list(open_pickle('giant_bomb_updated_game_info_new.pkl').keys())
    db_titles = pd.read_sql(db_table_name,con=db_connection)['index'].to_list()
    skip_titles.extend(scraped_titles)
    skip_titles.extend(db_titles)
    t = [t for t in titles if t not in skip_titles]
    
    
#     games_dict = {}
    games_dict = open_pickle('giant_bomb_updated_game_info_new.pkl')

    if len(t) != 0:
        driver = webdriver.Chrome(executable_path='/Users/elena.morais/Documents/chromedriver_2') 
        driver.get('https://www.giantbomb.com')
        print('stopped after getting to page')

        time.sleep(15)
        print('stopped after getting to sleep')

    c = len(db_titles)
    lower = len(db_titles)

    for title in t:
        print(title)

        time.sleep(random.randint(2,5))
        driver.find_elements_by_xpath('//div[@class="js-masthead-toggle masthead-toggle masthead-toggle-search"]')[1].click()
        time.sleep(random.randint(0,2))
        try:
            driver.find_element_by_xpath('//input[@class="js-site-search-query"]').send_keys(title)
        except:
            time.sleep(5)
            driver.find_element_by_xpath('//input[@class="js-site-search-query"]').send_keys(title)
        try:
            driver.find_elements_by_xpath("//option[@value='game']")[0].click()
        except:
            print("nothing popped up in the list")
        time.sleep(random.randint(0,2))
    #     driver.find_element_by_xpath('//select[@class="dropdown--selector"]').click()
    #     driver.find_element_by_xpath('//option[@value="game"]').click()
        time.sleep(random.randint(0,2))
        driver.find_element_by_xpath('//input[@class="js-site-search-query"]').send_keys(u'\ue007')
    #     river-search__select
        get_game_details(title,driver,games_dict)
        c += 1 
        
        if c % 50 == 0:
            save_pickle('giant_bomb_updated_game_info_new.pkl',games_dict)

        if c % 500 == 0:
            save_df = pd.DataFrame(games_dict).T.reset_index().iloc[lower:c,:]
            lower = c
            save_df.to_sql(db_table_name,con=db_connection,
                           schema='Sandbox_Elena_Morais',if_exists='append')
            save_pickle('giant_bomb_updated_game_info_new.pkl',games_dict)
            
        else:
            pass
    

        
    
    save_pickle('giant_bomb_updated_game_info_new.pkl',games_dict)
#     games_dict.update(hand_done_titles)
    save_df = pd.DataFrame(games_dict).T.reset_index().iloc[lower:,:]
    
#     print(save_df.tail())
    
#     def is_li(val):
#         if type(val) == type([]):
#             return ','.join(val)
#         else:
#             return val
    
#     for col in save_df.columns:
#         save_df[col] = save_df[col].apply(lambda val: is_li(val))
        
#     save_df.to_sql(db_table_name,con=db_connection,schema='Sandbox_Elena_Morais',if_exists='append')
    
    bottom = save_df.shape[0]
    
    driver = webdriver.Chrome(executable_path='/Users/elena.morais/Documents/chromedriver_2')
    for title in pages.keys():
        print(title)
        driver.get(pages[title])

        time.sleep(random.randint(2,5))
        get_game_details_2(title,driver,games_dict)

    save_pickle('giant_bomb_updated_game_info_new.pkl',games_dict)
    save_df = pd.DataFrame(games_dict).T.reset_index().iloc[bottom:,:]
    save_df.to_sql(db_table_name,con=db_connection,schema='Sandbox_Elena_Morais',if_exists='append')
    
    
    
    
    
    
        
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