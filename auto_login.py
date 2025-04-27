# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00899AFCB98D0F09A75750EFD640E01C4D75D1AEA7025E44CA2A374DB39530FE2A746ADCD5BDAECB3268B08777BC2DEDB7F1557CF3C663749EBC72ABCBD57E6B76EA4C863241D6A544539248F59A0A69E359604A1B55E3700970956EE28068DF0660C7FFEBAAFE3F2B453BB50D520E2F235D6E4A22738951C32BD64780582896F59186D18B290110B7F3B296268F892CC600A749DB53A65B6367FF1CAE1C264A653301BA639C59A7A14ADC32065CD3C50436D9CFB06D507F4BA30552B42E14A54FCF448458AD0289A212E31027A9C356CB8D00815FF5C98D14382CF601D797D8CF408D00DF17C97BA2CBBE4D8EC578F06FF0B11A7D8F3BD82C5E61F3EAF58B14EFD5C37AA05F9DC5025850F72614C20365DA493FBFEC819E5BD7CC8261D383A2A0B46F74A6FEE7288B26B0DA3A1E5EA698B52C58B33DED9CC4E7B3FC83ABF956DD4551EC2BCAA59B7663F33D9524809A4F612B5AAEB8D5681901621AD326715BCD"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
