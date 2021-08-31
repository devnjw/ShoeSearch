from flask_restful import Resource

from app import db
from app.models import Item, Brand

import os, time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import urllib.request

def PageUrl(itemName, pageNum):
    url = "https://search.musinsa.com/search/musinsa/goods?q=" + itemName + "&list_kind=small&sortCode=pop&sub_sort=&page="+ str(pageNum) +"&display_cnt=0&saleGoods=false&includeSoldOut=false&popular=false&category1DepthCode=&category2DepthCodes=&category3DepthCodes=&selectedFilters=&category1DepthName=&category2DepthName=&brandIds=&price=&colorCodes=&contentType=&styleTypes=&includeKeywords=&excludeKeywords=&originalYn=N&tags=&saleCampaign=false&serviceType=&eventType=&type=&season=&measure=&openFilterLayout=N&selectedOrderMeasure=&d_cat_cd="
    return url

def PageUrlWithCategory(categoryNum, pageNum):
    itemNum = "005" # 신발
    url = "https://search.musinsa.com/category/"+ itemNum + categoryNum +"?d_cat_cd="+ itemNum + categoryNum +"&brand=&rate=&page_kind=search&list_kind=small&sort=pop&sub_sort=&page="+ str(pageNum) +"&display_cnt=90&sale_goods=&ex_soldout=&color=&price1=&price2=&exclusive_yn=&shoeSizeOption=&tags=&campaign_id=&timesale_yn=&q=&includeKeywords="
    return url

class MusinsaItemCrawler(Resource):
    def get(self):
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

            for j in range(len(item_infos)):
                try:
                    title = item_infos[j].get_attribute("title")
                    brand = item_infos[j].get_attribute("data-bh-content-meta4")
                    price = item_infos[j].get_attribute("data-bh-content-meta3")
                    item_url = item_infos[j].get_attribute("href")
                    img_url = item_images[j].get_attribute("data-original")
                    shop = "musinsa"

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


class MusinsaBrandCrawler(Resource):
    def get(self):
        driver = webdriver.Chrome(os.getcwd() + "/chromedriver")
        driver.get("https://store.musinsa.com/app/contents/brandshop")

        time.sleep(2)

        brand_list = driver.find_elements_by_tag_name("dl")
        

        for brand in brand_list:
            eng_name = brand.text.split(' SALE')[0]
            #subs = brand.text.splitlines()[1] #.split(' (')[0]

            if len(brand.text.splitlines()) == 2:
                eng_name = brand.text.splitlines()[0]
                subs = brand.text.splitlines()[1]

                if eng_name.find(' SALE') > -1:
                    eng_name = eng_name[0:eng_name.find(' SALE')]
                if eng_name.find(' 단독') > -1:
                    eng_name = eng_name[0:eng_name.find(' 단독')]
                if subs.find(' (') > -1:
                    subs = subs[0:subs.find(' (')]

                # print(eng_name, eng_name.lower(), subs)

                try:
                    new_brand = Brand(
                        eng_name = eng_name.lower(),
                        subs = subs
                    )

                    db.session.add(new_brand)
                    db.session.commit()

                except Exception as e:
                    print(e)
                    pass

        driver.close()


class MusinsaItemWithCategoryCrawler(Resource):
    def get(self):
        CategoryList = [["014", "구두"], ["015", "로퍼"], ["012", "힐"], ["017", "플랫슈즈"], ["019", "블로퍼"], ["004", "샌들"], ["018", "슬리퍼"], ["011", "부츠"]]

        # driver = webdriver.Chrome(os.getcwd() + "/chromedriver")
        driver = webdriver.Chrome(ChromeDriverManager().install())

        for c in CategoryList:
            pageUrl = PageUrlWithCategory(c[0], 1)
            driver.get(pageUrl)

            totalPageNum = driver.find_element_by_css_selector(".totalPagingNum").text
            print("Total Page of category ", c[1], " : ", str(totalPageNum))

            cnt = 1
            for i in range(int(totalPageNum)):
                pageUrl = PageUrlWithCategory(c[0], i+1)
                driver.get(pageUrl)
                time.sleep(2)
                item_infos = driver.find_elements_by_css_selector(".img-block")
                item_images = driver.find_elements_by_css_selector(".lazyload.lazy")

                print("Finding: ", c[1], " - Page ", i+1, "/",totalPageNum, " start - ", len(item_infos), " items exist")

                FILEPATH = "images/musinsa/" + c[1] + "/"
                os.makedirs(FILEPATH, exist_ok=True)

                for j in range(len(item_infos)):
                    try:
                        img_url = item_images[j].get_attribute("data-original")

                        # Save Image
                        urllib.request.urlretrieve(img_url, FILEPATH + str(cnt) + ".jpg")
                        cnt += 1

                    except Exception as e:
                        print(e)
                        pass

        driver.close()