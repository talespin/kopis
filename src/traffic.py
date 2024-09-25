import os
import json
from time import sleep
from random import randrange
from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions


def get_config():
    with open('config.json', encoding='utf-8') as fs:
        return json.load(fs)


def get_chrome_option():
    options = ChromeOptions()
    options.add_argument('headless')
    return options


def get_exit_msg():    
    print('''        ###################################################################################
        ##                                                                               ##
        ##                                                                               ##
        ##    Google Chrome 설치가 되지않았습니다. Google Chrome 설치후에 실행해주세요   ##
        ##                                                                               ##
        ##                                                                               ##
        ###################################################################################
''')


def connect_url(chrome, url, config):
    if config['request_delay_time_min'] == config['request_delay_time_max']:
        sleep(config['request_delay_time_min'])
    else:
        sleep(randrange(config['request_delay_time_min'], config['request_delay_time_max']))
    chrome.get(url)
    

def go_random_target(chrome, base_url):
    all_a = [x for x in chrome.find_elements(By.TAG_NAME, 'a') if x.is_displayed()]
    if len(all_a) <= 0: chrome.get(base_url)
    idx = randrange(1,len(all_a))
    all_a[idx].click()


def close_other_tab(chrome, main_handle):
    chwd = chrome.window_handles
    for handle in chwd:
        if handle != main_handle:
            chrome.switch_to.window(handle)
            chrome.close()
    chrome.switch_to.window(main_handle)


def main():
    try:
        chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=get_chrome_option())
        main_handle = chrome.window_handles[0]
    except:
        get_exit_msg()
        exit(0)
    while True:
        config = get_config()
        now = datetime.now().strftime('%H:%M:%S')
        if len([x for x in config['run_time'] if x[0] <= now <= x[1]]) == 0:
            sleep(10)
            continue
        try:
            use_menu_only = True if config.get('use_menus_only') == 'Y' else False
            if use_menu_only:
                menus = config['menus']
                url = menus[list(menus.keys())[randrange(0, len(menus.keys())+1)]]
                connect_url(chrome, url, config)
            else:
                if chrome.current_url.startswith(config['base_url']) == False:
                    chrome.get(config['base_url'])
                else:
                    go_random_target(chrome)
        except:
            sleep(10)
        close_other_tab(chrome, main_handle)    


if __name__=='__main__':
    main()
