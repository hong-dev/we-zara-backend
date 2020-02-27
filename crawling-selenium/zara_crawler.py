import time
import pandas as pd
import csv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from collections import OrderedDict
from bs4 import BeautifulSoup

def getPages():

    time.sleep(2)
    test = browser.page_source
    soup = BeautifulSoup(test, 'lxml')
    description = soup.select('#description > p')
    product_name = soup.select(
        '#product > div.product-info-container._product-info-container> div > div.info-section > header > h1'
    )
    product_price = soup.select(
        '#product > div.product-info-container._product-info-container > div > div.info-section > div.price._product-price > span'
    )
    product_imgs =  soup.select('#main-images > div > a')
    product_sizes =  soup.select(
        '#product > div.product-info-container._product-info-container > div > div.info-section > form > fieldset > div > div.size-list > label > span > div'
    )
    product_color = soup.select(
        '#product > div.product-info-container._product-info-container > div > div.info-section > div:nth-child(3) > p > span._colorName'
        )

    product_size_list=[]

    for element in product_sizes:
        product_size_list.append(element.text)

    product_img_list=[]

    for element in product_imgs:
        product_img_list.append(element['href'])

    time.sleep(2)

    try:
        browser.find_element_by_css_selector(
            '#product > div.product-info-container._product-info-container > div > div.info-section > div:nth-child(6) > ul > li:nth-child(1) > a'
            ).click()

    except Exception as identifier:
        browser.find_element_by_css_selector(
            '#product > div.product-info-container._product-info-container > div > div.info-section > div:nth-child(5) > ul > li:nth-child(1) > a'
            ).click()

    time.sleep(2)
    html=browser.page_source
    soup=BeautifulSoup(html,'lxml')
    product_popups_topic=soup.select('div > ul > li > p.title-section')
    product_popups_content=soup.select('div > ul > li > p.zonasPrenda')
    popups_list=[]

    try:
        for element in range(len(product_popups_topic)):
            popups_list.append(
                {product_popups_topic[element].text:product_popups_content[element].text}
                )
    except Exception as identifier:
        for element in range(len(product_popups_topic)):
            if(element==1):
                popups_list.append(
                    {'caution':product_popups_topic[element].text}
                    )
            else:
                popups_list.append(
                    {product_popups_topic[element].text:product_popups_content[element].text}
                    )


    product_popups_cares=soup.select('#popup-composition > ul.list-cares > li > span')
    cares_list=[]

    for element in range(len(product_popups_cares)):
        cares_list.append(product_popups_cares[element].text)
        ß
    name = product_name[0].text.split(' ')
    name.pop()
    name.pop()
    name = ' '.join(name)
    product_detail = [
        description[0].text,
        name, product_price[0].text,
        product_img_list,
        product_size_list,
        product_color[0].text,
        popups_list,
        cares_list
        ]

    time.sleep(2)
    return product_detail

browser = webdriver.Chrome('./chromedriver')
browser.get('https://www.zara.com/kr/ko/woman-knitwear-l1152.html?v1=1445718')
body = browser.find_element_by_tag_name('body')
time.sleep(2)
test = browser.page_source
soup = BeautifulSoup(test, 'lxml')

id_list=[]
li_list= soup.select("#products > div._groups-wrap > ul > li")
product_summery = []

for element in li_list:
    id_list.append("".join(element['id']))

product_pre_name=""
product_pre_color=""

for element in id_list:
    if(id_list.index(element)>42):
        try:
            if 'product' in element:
                time.sleep(2)
                browser.find_element_by_css_selector(
                    '#'+element+" > div > div.product-info-item.product-info-item-name > a"
                    ).click()

                product_detail = getPages()

                try:
                    browser.find_element_by_css_selector(
                        '#catalog-area > div.popup._popup > div._popup-wrapper > div.popup-header > div'
                        ).click()
                    time.sleep(.5)
                    browser.back()
                    time.sleep(1)

                except Exception as idf:
                    try:
                        browser.find_element_by_css_selector(
                            '#catalog-area > div.popup._popup > div._popup-wrapper > div.popup-header > div'
                            ).click()
                    except Exception as identifier:
                        browser.back()
                        time.sleep(1)

                test = browser.page_source
                soup = BeautifulSoup(test,'lxml')
                img = soup.select('#'+element+"> a > div >img")
                imgurl=[]

                for element in img:
                    imgurl.append("".join(element['src']))

                product_detail.append(imgurl[0])
                if(not(product_pre_color == product_detail[5] and product_pre_name  == product_detail[1])):
                    product_summery.append(product_detail)
                    product_pre_name=product_detail[1]
                    product_pre_color=product_detail[5]
                    print(product_pre_color+" "+product_pre_name)
                    data = pd.DataFrame(product_summery)
                    data.columns = ['description', 'name', 'price', 'img', 'size', 'color', 'composition', 'care','primary_thumbnail']
                    data.to_csv('zara_knit.csv', encoding='utf-8')

        except Exception as identifier:
                print(identifier)
                time.sleep(1)

time.sleep(5)
browser.quit()



