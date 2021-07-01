from flask import render_template, jsonify
from flask_restful import Resource, abort

from app import db
from app.models import Item

import os, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request

def PageUrl(itemName, pageNum):
    url = "https://search.musinsa.com/search/musinsa/goods?q=" + itemName + "&list_kind=small&sortCode=pop&sub_sort=&page="+ str(pageNum) +"&display_cnt=0&saleGoods=false&includeSoldOut=false&popular=false&category1DepthCode=&category2DepthCodes=&category3DepthCodes=&selectedFilters=&category1DepthName=&category2DepthName=&brandIds=&price=&colorCodes=&contentType=&styleTypes=&includeKeywords=&excludeKeywords=&originalYn=N&tags=&saleCampaign=false&serviceType=&eventType=&type=&season=&measure=&openFilterLayout=N&selectedOrderMeasure=&d_cat_cd="
    return url

class Crawl(Resource):
    def get(self):
        FindingItemName = "신발"

        driver = webdriver.Chrome(os.getcwd() + "/chromedriver")

        pageUrl = PageUrl(FindingItemName, 1)
        driver.get(pageUrl)

        totalPageNum = driver.find_element_by_css_selector(".totalPagingNum").text
        items = driver.find_elements_by_css_selector(".lazyload.lazy")
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
                    # time.sleep(0.05)
                    
                    title = item_infos[i].get_attribute("title")
                    brand = item_infos[i].get_attribute("data-bh-content-meta4")
                    price = item_infos[i].get_attribute("data-bh-content-meta3")
                    item_url = item_infos[i].get_attribute("href")
                    img_url = item_images[i].get_attribute("data-original")
                    shop = "musinsa"

                    # print("Title: ", title)
                    # print("Brand: ", brand)
                    # print("Price: ", price)
                    # print("Image URL: ", item_url)
                    # print("Image URL: ", img_url)
                    # print()

                    new_user = Item(
                        title = title,
                        brand = brand,
                        price = price,
                        item_url = item_url,
                        image_url = img_url,
                        shop = shop
                    )

                    db.session.add(new_user)
                    db.session.commit()

                    # Save Image
                    urllib.request.urlretrieve(img_url, "images/musinsa/m" + str(cnt) + ".jpg")
                    cnt += 1

                except Exception as e:
                    print(e)
                    pass

        driver.close()