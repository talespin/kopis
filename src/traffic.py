import os
import sys
import json
import logging
from time import sleep
from random import randrange
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions


def get_config():
    with open('config.json', encoding='utf-8') as fs:
        return json.load(fs)


def get_chrome_option():
    options = ChromeOptions()
    #options.add_argument('headless')
    return options


def get_exit_msg():    
    msg = '''        ###################################################################################
        ##                                                                               ##
        ##                                                                               ##
        ##    Google Chrome 설치가 되지않았습니다. Google Chrome 설치후에 실행해주세요   ##
        ##                                                                               ##
        ##                                                                               ##
        ###################################################################################
'''
    if os.environ.get('OS','').find('indow') >= 0:
        msg = msg.encode('utf-8').decode('cp949')
    print(msg)

def connect_url(chrome, url, config):
    logging.debug('connect_url:' + url)
    if config['request_delay_time_min'] == config['request_delay_time_max']:
        sleep(config['request_delay_time_min'])
    else:
        sleep(randrange(config['request_delay_time_min'], config['request_delay_time_max']))
    chrome.get(url)

def run_script(chrome, script, config):
    logging.debug('connect_url:' + url)
    if config['request_delay_time_min'] == config['request_delay_time_max']:
        sleep(config['request_delay_time_min'])
    else:
        sleep(randrange(config['request_delay_time_min'], config['request_delay_time_max']))
    menus = config['menus']
    script = menus[list(menus.keys())[randrange(0, len(menus.keys())+1)]]
    chrome.execute_script(script)
    

def go_random_target(chrome, base_url):
    chrome.execute_script("scroll(0, 0);")
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
        chrome.set_window_size(1800,950)
        main_handle = chrome.window_handles[0]
    except:
        get_exit_msg()
        exit(0)
    cnt = 0
    while True:
        config = get_config()
        now = datetime.now().strftime('%H:%M:%S')
        if len([x for x in config['run_time'] if x[0] <= now <= x[1]]) == 0:
            sleep(10)
            continue
        try:
            cnt += 1
            if cnt >= 100:
                cnt = 0
                chrome.get(config['base_url'])
            use_menu_only = True if config.get('use_menus_only') == 'Y' else False
            if use_menu_only:
                run_script(chrome, script, config)
            else:
                if chrome.current_url.startswith(config['base_url']) == False:
                    chrome.get(config['base_url'])
                else:
                    go_random_target(chrome, config['base_url'])
        except Exception as e:
            logging.debug(str(e))
            sleep(10)
        close_other_tab(chrome, main_handle)


if __name__=='__main__':
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    main()
