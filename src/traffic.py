import os
import json
import platform
from time import sleep
from random import randrange
from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions

plt = platform.system().lower()

options = ChromeOptions()
options.add_argument('headless')
chrome = webdriver.Chrome(options=options)

for m in menus:
    sleep(request_delay_time)
    chrome.get(menus[m])
all_a = [x for x in chrome.find_elements(By.TAG_NAME, 'a') if x.is_displayed()]	
idx = randrange(1,len(all_a))
all_a[idx].click()
