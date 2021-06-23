import os, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request

driver = webdriver.Chrome(os.getcwd() + "/chromedriver")
driver.get("https://www.google.co.kr/imghp?hl=ko&tab=ri&authuser=0&ogbl")
elem = driver.find_element_by_name("q")
elem.send_keys("신발")
elem.send_keys(Keys.RETURN)

SCROLL_PAUSE_TIME = 1

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        try:
            driver.find_element_by_css_selector(".mye4qd").click()
        except:
            break
    last_height = new_height

cnt = 1
images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
for image in images:
    try:
        image.click()
        time.sleep(2)
        imgUrl = driver.find_element_by_xpath('/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/div[15]/a[1]/div[1]/img').get_attribute("src")
        urllib.request.urlretrieve(imgUrl, "google/" + str(cnt) + ".jpg")
        cnt += 1
    except Exception as e:
        print(e)
        pass

driver.close()
