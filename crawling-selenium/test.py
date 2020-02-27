# from selenium import webdriver
# import time
# import pandas as pd 
# #import csv
# #from pandas import DataFrame
# from bs4 import BeautifulSoup



# browser = webdriver.Chrome('./chromedriver')
# browser.get("https://www.zara.com/kr/ko/woman-shoes-l1251.html?v1=1445725")
# test = browser.page_source
# soup = BeautifulSoup(test, 'html.parser')
# link = soup.select(
#         'li > div > div.product-info-item.product-info-item-name > a'
#     )

# links = []
    
# for element in link:
#         links.append("".join(element['href'] + '?' + element['data-extraquery']))

# time.sleep(1) # 5초 대기

# # print(links)
# def getPages(page):
#     browser.get(links[page])
#     time.sleep(1)
#     test = browser.page_source
#     soup = BeautifulSoup(test, 'lxml')
#     description = soup.select('#description > p')
#     product_name = soup.select('#product > div.product-info-container._product-info-container > div > div.info-section > header > h1')
#     product_price = soup.select('#product > div.product-info-container._product-info-container > div > div.info-section > div.price._product-price > span')
#     product_imgs =  soup.select('#main-images > div > a')
#     product_sizes =  soup.select('#product > div.product-info-container._product-info-container > div > div.info-section > form > fieldset > div > div.size-list > label > span > div')
#     product_compositions = soup.select('#popup-composition > ul.list-composition > li > p.zonasPrenda')
#     product_color = soup.select('#product > div.product-info-container._product-info-container > div > div.info-section > div:nth-child(3) > p > span._colorName')

#     product_size_list=[]

#     for element in product_sizes:
#         product_size_list.append(element.text)

#     product_img_list=[]
#     for element in product_imgs:
#         product_img_list.append(element['href'])


#     time.sleep(1)
#     browser.find_element_by_css_selector('#product > div.product-info-container._product-info-container > div > div.info-section > div:nth-child(6) > ul > li:nth-child(1) > a').click()

#     html=browser.page_source
#     soup=BeautifulSoup(html,'lxml')

#     product_popups_topic=soup.select('div > ul > li > p.title-section')
#     product_popups_content=soup.select('div > ul > li > p.zonasPrenda')

#     popups_list=[]
#     for element in range(len(product_popups_topic)):
#         popups_list.append({product_popups_topic[element].text:product_popups_content[element].text})

#     time.sleep(1)
#     product_popups_cares=soup.select('#popup-composition > ul.list-cares > li > span')
#     time.sleep(1)

#     cares_list=[]

#     for element in range(len(product_popups_cares)):
#         cares_list.append(product_popups_cares[element].text)


#     product_summery={
#         "description":description[0].text,
#         "product_name":product_name[0].text,
#         "product_price":product_price[0].text,
#         "product_img":product_img_list,
#         "product_size":product_size_list,
#         "product_color":product_color[0].text,
#         "popup_list":popups_list,
#         "cares_list":cares_list
#     }
#     print(product_summery)

#        time.sleep(1)
#     browser.find_element_by_css_selector('#catalog-area > div.popup._popup > div._popup-wrapper > div.popup-header > div').click()    
#     time.sleep(1)
    


# for element in range(len(links)):
#     getPages(element)






# browser.quit() # 브라우저 종료

from selenium import webdriver
import time
import pandas as pd
import csv
from collections import OrderedDict
from bs4 import BeautifulSoup
browser = webdriver.Chrome('./chromedriver')
browser.get('https://www.zara.com/kr/ko/woman-shoes-l1251.html?v1=1445725')
# browser.get('https://www.zara.com/kr/ko/woman-knitwear-l1152.html?v1=1445718')
# browser.get('https://www.zara.com/kr/ko/woman-bags-l1024.html?v1=1445798')
test = browser.page_source
soup = BeautifulSoup(test, 'html.parser')
link = soup.select(
        'li > div > div.product-info-item.product-info-item-name > a'
    )
links = []
for element in link:
        links.append("".join(element['href'] + '?' + element['data-extraquery']))
# links = list(OrderedDict.fromkeys(links))
time.sleep(1) # 5초 대기
product_summery = []
def getPages(page):
    browser.get(links[page])
    # browser.get('https://www.zara.com/kr/ko/%EC%BD%98%ED%8A%B8%EB%9D%BC%EC%8A%A4%ED%8C%85-%EB%A6%AC%EB%B8%8C%EB%93%9C-%EC%8A%A4%EC%9B%A8%ED%84%B0-p04369004.html?v1=46093909&v2=1445718')
    time.sleep(2)
    test = browser.page_source
    soup = BeautifulSoup(test, 'lxml')
    description = soup.select('#description > p')
    product_name = soup.select('#product > div.product-info-container._product-info-container > div > div.info-section > header > h1')
    product_price = soup.select('#product > div.product-info-container._product-info-container > div > div.info-section > div.price._product-price > span')
    product_imgs =  soup.select('#main-images > div > a')
    product_sizes =  soup.select('#product > div.product-info-container._product-info-container > div > div.info-section > form > fieldset > div > div.size-list > label > span > div')
    product_color = soup.select('#product > div.product-info-container._product-info-container > div > div.info-section > div:nth-child(3) > p > span._colorName')
    product_size_list=[]

    for element in product_sizes:
        product_size_list.append(element.text)

    product_img_list=[]

    for element in product_imgs:
        product_img_list.append(element['href'])

    time.sleep(2)

    try:
        browser.find_element_by_css_selector('#product > div.product-info-container._product-info-container > div > div.info-section > div:nth-child(6) > ul > li:nth-child(1) > a').click()

    except Exception as identifier:
        browser.find_element_by_css_selector('#product > div.product-info-container._product-info-container > div > div.info-section > div:nth-child(5) > ul > li:nth-child(1) > a').click()
    
    time.sleep(2)
    
    html=browser.page_source
    soup=BeautifulSoup(html,'lxml')
    product_popups_topic=soup.select('div > ul > li > p.title-section')
    product_popups_content=soup.select('div > ul > li > p.zonasPrenda')

    popups_list=[]
    try:
        for element in range(len(product_popups_topic)):
            popups_list.append({product_popups_topic[element].text:product_popups_content[element].text})
    except Exception as identifier:
        for element in range(len(product_popups_topic)):
            if(element==1):
                popups_list.append({'caution':product_popups_topic[element].text})
            else:
                popups_list.append({product_popups_topic[element].text:product_popups_content[element].text})
    
            #product > div.product-info-container._product-info-container > div > div.info-section > div:nth-child(6) > ul > li:nth-child(1) > a
    
    
    product_popups_cares=soup.select('#popup-composition > ul.list-cares > li > span')
    cares_list=[]

    for element in range(len(product_popups_cares)):
        cares_list.append(product_popups_cares[element].text)
    name = product_name[0].text.split(' ')
    name.pop()
    name.pop()

    name = ' '.join(name)
    product_detail = [description[0].text, name, product_price[0].text, product_img_list, product_size_list, product_color[0].text, popups_list, cares_list]
    product_summery.append(product_detail)
    data = pd.DataFrame(product_summery)

    data.columns = ['description', 'name', 'price', 'img', 'size', 'color', 'composition', 'care']
    data.to_csv('zara_shoes.csv', encoding='utf-8')

    print(product_summery)
    time.sleep(2)

# product_summery = []

for element in range(len(links)):
    try:
        getPages(element)
    except Exception as identifier:
        getPages(element)
# link=['https://www.zara.com/kr/ko/puff-sleeve-knit-top-p02162001.html?v1=34796228&v2=1445718']
# getPages(0)
browser.quit() # 브라우저 종료

#popup-composition > ul.list-composition > li:nth-child(1) > p.title-section
#popup-composition > ul.list-composition > li:nth-child(1) > p.zonasPrenda

#popup-composition > ul.list-composition > li:nth-child(2) > p

#popup-composition > h2:nth-child(3)
#popup-composition > ul.list-cares > li:nth-child(1) > i
#popup-composition > ul.list-cares > li:nth-child(4)
#popup-composition > ul.list-cares

# <img class="product-media _img _imgImpressions" alt="마이크로 스터드 레더 바이커 앵클부츠" src="https://static.zara.net/stdstatic/1.144.0-b.7/images/transparent-background.png">