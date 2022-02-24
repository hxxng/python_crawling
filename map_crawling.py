from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path='./chromedriver', options=options)

driver.get("https://map.naver.com/v5/search")

time.sleep(3)
search_box = driver.find_element_by_css_selector("div.input_box>input.input_search")
search_box.send_keys("마라탕")

time.sleep(2)
search_box.send_keys(Keys.ENTER)

# 크롤링
for p in range(20):
    time.sleep(2)

    driver.switch_to_frame("searchIframe")    
    raw = driver.page_source
    
    html = BeautifulSoup(raw, "html.parser")

    contents = html.select("body > div#app-root > div._28gZt > div._2lx2y > div._1Az1K > ul > li")
    for s in contents:
        name = s.select_one("span.OXiLu").text
        stars = s.select_one("div._3hn9q > a > div._17H46 > span._2FqTn._1mRAM > em")
        if stars != None:
            star  = stars.text
            print("식당명: " + name + " ★ " + star)
        else:
            print("식당명: " + name)
        
        # try:
        #     phone = search_box_html.select_one(".search_text_box .phone").text
        # except:
        #     phone = "NULL"
        # print("전화번호: " + phone)
        # address = search_box_html.select_one(".ng-star-inserted .address").text
        # print("주소: " + address)

        print("--"*30)
        
    try:
        next_btn = html.select("body > div#app-root > div._28gZt > div._2lx2y > div._2ky45 > a._2bgjK")
        for b in next_btn:
            text = b.select_one("span.place_blind").get_text()
            if text == "다음페이지":
                print(b)
                b.click()
    except:
        print("데이터 수집 완료")
        break

driver.close()

