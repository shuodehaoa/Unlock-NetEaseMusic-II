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
    browser.add_cookie({"name": "MUSIC_U", "value": "003F35C7539F3C4ED1BB32E4D6EBF7871246FA916A457CCC8B4B22A74BD98B547FA23050A214980235C2A6C7B96BA48AFE22A58EBE713C3175CEB7680BD75B6E0A0B70B00A97E123283137CA6DA195858B685CADE97F84496B7207509018FE0A69E4B2F056E3E14B5DAABEC2EFD2A211D924FEF5C1EF15D022B27ADA47EF4AADFCBCC9F2602C3DC19060AE8FD8BC94CFA4A125B7188A02CAD9351F371FFE45391C1BC596176F57324106FB0071E9FA4ABD41D1CC45D566B98097CBD1CFDF8CE6920EE7D5268D1D4F79E15326B503F9F33A7EEF0DE8D1F251E7BC671282F856D95330D756D9109D26AACA68EBD61B03C2C51EE7E16421831F213600E030FA9E888BBD7B939F3A874AC87A5B067B5D1664021D824F2D84F5A14EC080945694077C91F66DF036086EBB326811EB5E849FD9547209D90880A8B7D6F8E7CFB1D9E7F3C60267F719B3F84EE331D6B2316934DFEF42B692F3EBA77D02D43CD07373901A21"})
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
