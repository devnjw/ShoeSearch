import os, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request

def PageUrl(itemName, pageNum):
    url = "https://search.musinsa.com/search/musinsa/goods?q=" + itemName + "&list_kind=small&sortCode=pop&sub_sort=&page="+ str(pageNum) +"&display_cnt=0&saleGoods=false&includeSoldOut=false&popular=false&category1DepthCode=&category2DepthCodes=&category3DepthCodes=&selectedFilters=&category1DepthName=&category2DepthName=&brandIds=&price=&colorCodes=&contentType=&styleTypes=&includeKeywords=&excludeKeywords=&originalYn=N&tags=&saleCampaign=false&serviceType=&eventType=&type=&season=&measure=&openFilterLayout=N&selectedOrderMeasure=&d_cat_cd="
    return url

FindingItemName = "신발"

driver = webdriver.Chrome(os.getcwd() + "/chromedriver")

pageUrl = PageUrl(FindingItemName, 1)
driver.get(pageUrl)

totalPageNum = driver.find_element_by_css_selector(".totalPagingNum").text
print("Total Page of ", FindingItemName, " : ", str(totalPageNum))

cnt = 1

for i in range(int(totalPageNum)):
    pageUrl = PageUrl(FindingItemName, i+1)
    driver.get(pageUrl)
    time.sleep(2)
    item_infos = driver.find_elements_by_css_selector(".img-block")
    item_images = driver.find_elements_by_css_selector(".lazyload.lazy")

    print("Finding: ", FindingItemName, " - Page ", i+1, "/",totalPageNum, " start - ", len(item_infos), " items exist")

    for i in range(len(item_infos)):
        try:
            time.sleep(0.5)
            
            title = item_infos[i].get_attribute("title")
            price = item_infos[i].get_attribute("data-bh-content-meta3")
            item_url = item_infos[i].get_attribute("href")
            img_url = item_images[i].get_attribute("data-original")

            print("Title: ", title)
            print("Price: ", price)
            print("Image URL: ", item_url)
            print("Image URL: ", img_url)
            print()

            # Save Image
            # urllib.request.urlretrieve(img_url, "../images/musinsa/m" + str(cnt) + ".jpg")
            # cnt += 1

        except Exception as e:
            print(e)
            pass

driver.close()

