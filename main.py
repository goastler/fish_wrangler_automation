import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
import time
import sys
from webdriver_manager.chrome import ChromeDriverManager

driver = None

def setup():
    global driver
    options = Options()
    options.headless = False
    options.add_argument("--window-size=900,900")

    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=options)
    driver.implicitly_wait(10)
    driver.get("https://fish-wrangler.com/fishwrangler/auth")

    el = driver.find_element(By.ID, 'main_email')
    el.send_keys('myemailaddress')
    sleep(1)
    el = driver.find_element(By.CSS_SELECTOR,
                             '#add_app > div.hsuccess.welcome > table:nth-child(1) > tbody > tr > td.play_fw_com_td > form > table > tbody > tr:nth-child(2) > td:nth-child(2) > input')
    el.send_keys('mypassword')
    sleep(1)
    el = driver.find_element(By.CSS_SELECTOR,
                             '#add_app > div.hsuccess.welcome > table:nth-child(1) > tbody > tr > td.play_fw_com_td > form > table > tbody > tr:nth-child(2) > td.pl.nbsp > input.inputbutton')
    el.click()

def fish():
    try:
        els = driver.find_elements(By.ID, "fishNowLink")
        if len(els) > 0 and els[0].text == "NOW!":
            print('fishing now')
            el = els[0]
            el.click()
            return True
        # els = driver.find_elements(By.CSS_SELECTOR, "#fishNowLink > sup")
        # if len(els) > 0 and els[0].text != "" and int(els[0].text) > 0 and int(els[0].text) < 16:
        #     print('skipping to fish now')
        #     els = driver.find_elements(By.ID, "fishNowLink")
        #     el = els[0]
        #     el.click()
        #     return True
        els = driver.find_elements(By.CSS_SELECTOR, '#timer_div > span > a')
        if len(els) > 0 and els[0].text == "NOW!":
            print('fishing now')
            el = els[0]
            el.click()
            return True
        els = driver.find_elements(By.CSS_SELECTOR, '#timer_div')
        if len(els) > 0:
            el = els[0].find_element(By.CSS_SELECTOR, 'span')
            t = el.text
            print('fishing', t)
            t = t.replace('hours', 'hour')
            t = t.replace('mins', 'min')
            t = t.replace('secs', 'sec')
            parts = t.split(' ')
            secs = 0
            for i in range(len(parts) - 1):
                if parts[i + 1].lower() == 'hour':
                    secs += int(parts[i]) * 60 * 60
                    i = i + 1
                elif parts[i + 1].lower() == 'min':
                    secs += int(parts[i]) * 60
                    i = i + 1
                elif parts[i + 1].lower() == 'sec':
                    secs += int(parts[i])
                    i = i + 1
                else:
                    pass
            sleep(secs + 1)
            return True
        return False
    except:
        print('fishing error')

setup()
t1 = time.monotonic_ns()
while True:
    t2 = time.monotonic_ns()
    if t2 - t1 > 8.64e+13:
        driver.quit()
        setup()
        t1 = time.monotonic_ns()
    print(datetime.now())
    if not fish():
        driver.get("https://fish-wrangler.com/fishwrangler/my")
    sleep(10)


# driver.quit()
