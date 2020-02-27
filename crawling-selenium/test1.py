# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
# import pandas as pd 
# #import csv
# #from pandas import DataFrame
# from bs4 import BeautifulSoup




# browser = webdriver.Chrome('./chromedriver')
# #browser.get("http://python.org")
# browser.get("https://www.youtube.com/")

# time.sleep(2)

# # test = browser.find_element_by_css_selector('#product-46349183 > a > div > img')
# body = browser.find_element_by_tag_name("body")
# num_of_pagedowns=50

# while num_of_pagedowns:
#     body.send_keys(Keys.PAGE_DOWN)
#     time.sleep(0.3)
#     num_of_pagedowns-=1
#     try:
#         browser.find_element_by_xpath("""//*[@id="feed-main-what_to_watch"]/button""").click()
#     except:
#         None

# html = browser.page_source
# soup = BeautifulSoup(html,'lxml')
# titles = soup.find_all('h3')

# for title in titles:
#     print(title.get_text())


# #pypi = None)
# #for m in test:
# #    if m.text == "PyPI":
# #        pypi = m
# # print(test.text)


# #dataframe = pd.DataFrame(test)
# #dataframe.to_csv("test.csv",mode='w',header=False)


 
# #pypi.click()  # 클릭
 
# time.sleep(5) # 5초 대기
# browser.quit() # 브라우저 종료


# import requests
# from bs4 import BeautifulSoup
# def extract_links():

# # li > div > div.product-info-item.product-info-item-name > a
#     html = requests.get('https://www.zara.com/kr/ko/woman-knitwear-l1152.html?v1=1445718').text
#     soup = BeautifulSoup(html, 'html.parser')
#     link = soup.select(
#         'li > div > div.product-info-item.product-info-item-name > a'
#     )
#     links = []
#     for element in link:
#         links.append("".join(element['href'] + '?' + element['data-extraquery']))
#     return links

# print(extract_links())


# import time

# import pandas as pd
# from selenium import webdriver

# options = webdriver.ChromeOptions()
# options.add_argument('window-size=1920x1080')
# options.add_argument("disable-gpu")
# driver = webdriver.Chrome('./chromedriver', options=options)
# driver.implicitly_wait(3)
# url = "https://www.ktmmobile.com/product/phone/officialNoticeSupportList.do"
# driver.get(url)

# data = []
# mCols = ['구분', '모델명', '요금제', '출고가', '공시지원금', '판매가']
# df = pd.DataFrame(columns=mCols)



# # 일단 배열 을 설정 함 .

# def getMobileData(n):
#     driver.implicitly_wait(10)
#     et = driver.find_element_by_xpath('//*[@id="tablePage"]/button[{}]'.format(n + 2))
#     driver.execute_script("arguments[0].click();", et)
#     time.sleep(3)
#     a = driver.find_element_by_id("listTb")
#     b = a.find_elements_by_css_selector("tr")
#     for i in b:
#         j = i.find_elements_by_css_selector("td")
#         for k in j:
#             print(k.text)
#             data.append(k.text)



# if __name__ == "__main__":
#     # 첫번째 페이지 
#     firstpage = 1
#     # 마지막 페이지 설정 500페이지까지 존재
#     endpage = 6
#     mCols = ['구분', '모델명', '요금제', '출고가', '공시지원금', '판매가']
#     df = pd.DataFrame(columns=mCols)

#     for page in range(firstpage, endpage):
#         print("{}페이지 수집 시작".format(page))
#         page = page % 10
#         getMobileData(page)
#         if page % 10 == 0:  # 만약에 페이지가 10 페이지가 됬을 경우
#             nextPageMove = driver.find_element_by_xpath('//*[@id="tablePage"]/button[13]')
#             driver.execute_script("arguments[0].click();", nextPageMove)
#             time.sleep(3)

#     for i in data:
#         df = df.append(pd.Series(i, index=df.columns), ignore_index=True)

#     df.to_csv('./kt_finally_test.csv', encoding='ms949')
# driver.foward()  
#     driver.back()     


# 출처: https://sacko.tistory.com/15 [데이터 분석하는 문과생, 싸코]
# import time
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver import Chrome
# import pandas as pd
# def getMobileData():
#     driver = Chrome("./chromedriver")
#     mCols = ["단말기명 ", "공시지원금 ", "판매가 ", "공시일자"]
#     df = pd.DataFrame(columns=mCols)
#     driver.implicitly_wait(3)
#     url = "http://www.smartchoice.or.kr/smc/smartlife/dantongTelList.do"
#     driver.get(url)
#     driver.implicitly_wait(10)
#     drop1 = driver.find_element_by_css_selector("#dan_Company")
#     drop2 = driver.find_element_by_css_selector("#planLGUService")
#     select1 = Select(drop1)
#     select1.select_by_index(3)  # 첫번재 option 클릭 !
#     time.sleep(.5)
#     select2 = Select(drop2)
#     select2.select_by_index(2)
#     time.sleep(.5)
#     drop3 = driver.find_element_by_css_selector("#dan_Plan_Code")
#     select3 = drop3.find_elements_by_tag_name("option")
#     feeSize = len(select3) - 1
#     print("메뉴의 개수는 {} 입니다".format(feeSize))
#     for k in range(feeSize):
#         driver.find_element_by_css_selector("#dan_Plan_Code option:nth-of-type({})".format(k + 2)).click()
#         time.sleep(0.5)
#         driver.find_element_by_css_selector("#stopResult button").click()
#         time.sleep(2)
#         page_move = driver.find_elements_by_css_selector("div.paging > span > *")
#         pages_num = len(page_move)
#         print(pages_num)  # 16 이 나옴
#         if pages_num != 0:
#             for page in range(pages_num):  # 0 부터 16 까지
#                 print("page", page)
#                 phone_list = driver.find_elements_by_css_selector(
#                     "#planTelTable > tr.dan.dan.page{} > td:nth-child(8) > a".format(page + 1))
#                 time.sleep(1)
#                 for pl in phone_list:
#                     pl.click()  # a 태그를 클릭해서 자바스크립트를 보여주는 버튼 click
#                     time.sleep(2)
#                     print("=" * 50)
#                     title = driver.find_element_by_css_selector("p.titP")
#                     time.sleep(2)
#                     table_list = driver.find_elements_by_css_selector(
#                         "#productUpdateListPopBody tr")  # 여기서 자바스크립트 전체 내용을 가져옴
#                     for table in table_list:
#                         time.sleep(1)
#                         shipment = table.find_element_by_css_selector("td:nth-of-type(1)").text
#                         support_money = table.find_element_by_css_selector("td:nth-of-type(2)").text
#                         standard_disclosure_date = table.find_element_by_css_selector("td:nth-of-type(3)").text
#                         print(title.text + " : ", shipment, support_money, standard_disclosure_date)
#                         info = [title.text, shipment, support_money, standard_disclosure_date]
#                         df.loc[len(df)] = info
#                     time.sleep(1)
#                     driver.execute_script("getProductUpdateListClose('web')")  # 자바 스크립트 닫는 click 부분
#                 try:
#                     if (page + 1) % 5 != 0:
#                         page_move[page + 1].click()
#                         time.sleep(2)
#                     else:
#                         driver.find_element_by_css_selector("div.paging > button.btn_pag_next").click()
#                         time.sleep(2)
#                 except:
#                     print("수집완료")
#         else:  # page 가 1 페이지 밖에 없을 경우
#             phone_list = driver.find_elements_by_css_selector(
#                 "#planTelTable > tr.dan.dan.page{} > td:nth-child(8) > a".format(1))
#             time.sleep(1)
#             for pl in phone_list:
#                 pl.click()  # a 태그를 클릭해서 자바스크립트를 보여주는 버튼 click
#                 time.sleep(2)
#                 print("=" * 50)
#                 title = driver.find_element_by_css_selector("p.titP")
#                 time.sleep(2)
#                 table_list = driver.find_elements_by_css_selector(
#                     "#productUpdateListPopBody tr")  # 여기서 자바스크립트 전체 내용을 가져옴
#                 for table in table_list:
#                     time.sleep(1)
#                     shipment = table.find_element_by_css_selector("td:nth-of-type(1)").text
#                     support_money = table.find_element_by_css_selector("td:nth-of-type(2)").text
#                     standard_disclosure_date = table.find_element_by_css_selector("td:nth-of-type(3)").text
#                     print(title.text + " : ", shipment, support_money, standard_disclosure_date)
#                     info = [title.text, shipment, support_money, standard_disclosure_date]
#                     df.loc[len(df)] = info
#                 time.sleep(1)
#                 driver.execute_script("getProductUpdateListClose('web')")  # 자바 스크립트 닫는 click 부분
#     df.to_csv("./lg/lg_LTE.csv", encoding='ms949')
# if __name__ == "__main__":
#     getMobileData()


# import time
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver import Chrome
# import pandas as pd
# def getMobileData():
#     driver = Chrome("./chromedriver")
#     mCols = ["단말기명 ", "공시지원금 ", "판매가 ", "공시일자"]
#     df = pd.DataFrame(columns=mCols)
#     driver.implicitly_wait(3)
#     url = "http://www.smartchoice.or.kr/smc/smartlife/dantongTelList.do"
#     driver.get(url)
#     driver.implicitly_wait(10)
#     drop1 = driver.find_element_by_css_selector("#dan_Company")
#     drop2 = driver.find_element_by_css_selector("#planLGUService")
#     select1 = Select(drop1)
#     select1.select_by_index(3)  # 첫번재 option 클릭 !
#     time.sleep(.5)
#     select2 = Select(drop2)
#     select2.select_by_index(2)
#     time.sleep(.5)
#     drop3 = driver.find_element_by_css_selector("#dan_Plan_Code")
#     select3 = drop3.find_elements_by_tag_name("option")
#     feeSize = len(select3) - 1
#     print("메뉴의 개수는 {} 입니다".format(feeSize))
#     for k in range(feeSize):
#         driver.find_element_by_css_selector("#dan_Plan_Code option:nth-of-type({})".format(k + 2)).click()
#         time.sleep(0.5)
#         driver.find_element_by_css_selector("#stopResult button").click()
#         time.sleep(2)
#         page_move = driver.find_elements_by_css_selector("div.paging > span > *")
#         pages_num = len(page_move)
#         print(pages_num)  # 16 이 나옴
#         if pages_num != 0:
#             for page in range(pages_num):  # 0 부터 16 까지
#                 print("page", page)
#                 phone_list = driver.find_elements_by_css_selector(
#                     "#planTelTable > tr.dan.dan.page{} > td:nth-child(8) > a".format(page + 1))
#                 time.sleep(1)
#                 for pl in phone_list:
#                     pl.click()  # a 태그를 클릭해서 자바스크립트를 보여주는 버튼 click
#                     time.sleep(2)
#                     print("=" * 50)
#                     title = driver.find_element_by_css_selector("p.titP")
#                     time.sleep(2)
#                     table_list = driver.find_elements_by_css_selector(
#                         "#productUpdateListPopBody tr")  # 여기서 자바스크립트 전체 내용을 가져옴
#                     for table in table_list:
#                         time.sleep(1)
#                         shipment = table.find_element_by_css_selector("td:nth-of-type(1)").text
#                         support_money = table.find_element_by_css_selector("td:nth-of-type(2)").text
#                         standard_disclosure_date = table.find_element_by_css_selector("td:nth-of-type(3)").text
#                         print(title.text + " : ", shipment, support_money, standard_disclosure_date)
#                         info = [title.text, shipment, support_money, standard_disclosure_date]
#                         df.loc[len(df)] = info
#                     time.sleep(1)
#                     driver.execute_script("getProductUpdateListClose('web')")  # 자바 스크립트 닫는 click 부분
#                 try:
#                     if (page + 1) % 5 != 0:
#                         page_move[page + 1].click()
#                         time.sleep(2)
#                     else:
#                         driver.find_element_by_css_selector("div.paging > button.btn_pag_next").click()
#                         time.sleep(2)
#                 except:
#                     print("수집완료")
#         else:  # page 가 1 페이지 밖에 없을 경우
#             phone_list = driver.find_elements_by_css_selector(
#                 "#planTelTable > tr.dan.dan.page{} > td:nth-child(8) > a".format(1))
#             time.sleep(1)
#             for pl in phone_list:
#                 pl.click()  # a 태그를 클릭해서 자바스크립트를 보여주는 버튼 click
#                 time.sleep(2)
#                 print("=" * 50)
#                 title = driver.find_element_by_css_selector("p.titP")
#                 time.sleep(2)
#                 table_list = driver.find_elements_by_css_selector(
#                     "#productUpdateListPopBody tr")  # 여기서 자바스크립트 전체 내용을 가져옴
#                 for table in table_list:
#                     time.sleep(1)
#                     shipment = table.find_element_by_css_selector("td:nth-of-type(1)").text
#                     support_money = table.find_element_by_css_selector("td:nth-of-type(2)").text
#                     standard_disclosure_date = table.find_element_by_css_selector("td:nth-of-type(3)").text
#                     print(title.text + " : ", shipment, support_money, standard_disclosure_date)
#                     info = [title.text, shipment, support_money, standard_disclosure_date]
#                     df.loc[len(df)] = info
#                 time.sleep(1)
#                 driver.execute_script("getProductUpdateListClose('web')")  # 자바 스크립트 닫는 click 부분
#     df.to_csv("./lg/lg_LTE.csv", encoding='ms949')
# if __name__ == "__main__":
#     getMobileData()



#     from selenium import webdriver
# import time
# import pandas as pd 
# #import csv
# #from pandas import DataFrame
# from bs4 import BeautifulSoup




# browser = webdriver.Chrome('./chromedriver')
# #browser.get("http://python.org")
# browser.get("https://www.zara.com/kr/ko/woman-shoes-l1251.html?v1=1445725")
# #menus = browser.find_elements_by_css_selector('#top ul.menu li')
# #test = browser.find_element_by_css_selector('#products > div._groups-wrap > ul')
# test = browser.find_element_by_css_selector('#product-46349183 > a > div > img')
# #pypi = None
# #for m in test:
# #    if m.text == "PyPI":
# #        pypi = m
# print(test.text)


# #dataframe = pd.DataFrame(test)
# #dataframe.to_csv("test.csv",mode='w',header=False)


 
# #pypi.click()  # 클릭
 
# time.sleep(5) # 5초 대기
# browser.quit() # 브라우저 종료

def extrat_indeed_jobs(last_page):
    jobs = []
    for page in range(last_page):
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    for result in results:
        title = result.find("div", {"class": "title"}).find("a")["title"]
        company = result.find("span", {"class": "company"})
        company_anchor = company.find("a")
        if company_anchor is not None:
            company = str(company_anchor.string)
        else:
            company = str(company.string)
        company = company.strip()
        location = result.find("div", {"class": "recJobLoc"})["data-rc-loc"]
        jobs.append({"title":title, "company":company, "location":location})
    return jobs

import requests
from bs4 import BeautifulSoup
def extract_links():
    html = requests.get('https://www.zara.com/kr/ko/woman-knitwear-l1152.html?v1=1445718').text
    soup = BeautifulSoup(html, 'html.parser')
    link = soup.select(
        'li > div > div.product-info-item.product-info-item-name > a'
    )
    links = []
    for element in link:
        links.append("".join(element['href'] + '?' + element['data-extraquery']))
    return links