from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import csv
from webdriver_manager.chrome import ChromeDriverManager



DRIVER_URL = "./chromedriver/chromedriver"
URL = "https://www.woondoc.com/search/coach"
SEARCH_TEXT = "강남구 역삼동"

#브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 애러 메세지 제거
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

Service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=Service, options=chrome_options)

driver.get(URL)

time.sleep(10)

# for initalize
driver.switch_to.default_content()

with open(SEARCH_TEXT+ ' 운동닥터 ' +'result.csv', 'w', newline='' ) as file:
    writer = csv.writer(file)
    writer.writerow(["name", "introduce", "price", "gym_address"])

# search keyword
search_box = driver.find_element(By.CSS_SELECTOR ,"#search_keyword")
search_box.send_keys(SEARCH_TEXT)

time.sleep(1.5)

search_box.send_keys(Keys.ENTER)

time.sleep(2)


search_list = driver.find_elements(By.CSS_SELECTOR ,"#__next > div > div > div.searchTabWrap > div.searchBarWrap > div:nth-child(4) > div > ul > li.SearchList__SearchBarList-sc-z0gr3-1.hpLQfz.list-group-item.focus")
search_list[0].click()

time.sleep(5)


with open(SEARCH_TEXT+ ' 운동닥터 ' +'result.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    
    while True:
        time.sleep(0.5)
        # Get Data and write
        try:
            
            boxes = driver.find_elements(By.CSS_SELECTOR ,"#__next > div > div > div.searchTabWrap > div.searchForm > div > div > div")
            boxesLen = len(boxes)
            if boxesLen == 0:
                time.sleep(1.5)
                boxes = driver.find_elements(By.CSS_SELECTOR ,"#__next > div > div > div.searchTabWrap > div.searchForm > div > div > div")
                boxesLen = len(boxes)
            
            print(boxesLen)

            for i in range(boxesLen):
                try:
                    time.sleep(0.5)
                    boxes[i].click()
                    time.sleep(1.5)
                    driver.switch_to.window(driver.window_handles[1])
                    print('change window 1')
                    time.sleep(0.5)

                    try:
                        name = driver.find_element(By.CSS_SELECTOR ,"#__next > div > div:nth-child(2) > div > section > div.grayBackground > div > div > div.col-md-5 > div > div.upside > div > div:nth-child(1) > div:nth-child(2) > div.coachName").text.split(' ')[0].encode('cp949', 'ignore').decode('cp949')
                    except:
                        name = "이름 없음"

                    try:
                        introduce = driver.find_element(By.CSS_SELECTOR ,"#__next > div > div:nth-child(2) > div > section > div.grayBackground > div > div > div.col-md-7 > div > div:nth-child(1) > div.contentWrap.centerTime > div.introduce.noDrag").text.encode('cp949', 'ignore').decode('cp949')
                    except:
                        introduce = "소개 없음"
                    
                    try:
                        price = driver.find_element(By.CSS_SELECTOR, "#__next > div > div:nth-child(2) > div > section > div.grayBackground > div > div > div.col-md-5 > div > div.downside > div > div.flexBox.grayBox > label:nth-child(3)").text.replace('원', '').replace(',', '').encode('cp949', 'ignore').decode('cp949')
                    except:
                        price = "가격 없음"

                    time.sleep(0.5)
                    driver.find_element(By.CSS_SELECTOR ,"#__next > div > div:nth-child(2) > div > section > div.detail_menu__Menu-sc-oi2f2m-0.hEYhlP > div.tabWrap > div > div:nth-child(2)").click()
                    time.sleep(0.5)
                    try:
                        gym_address = driver.find_element(By.CSS_SELECTOR ,"#__next > div > div:nth-child(2) > div > section > div.grayBackground > div > div > div.col-md-7 > div > div > div > div:nth-child(1) > div.contentWrap > div:nth-child(2) > div").text.replace(" 주소 복사", "").encode('cp949', 'ignore').decode('cp949')
                    except:
                        gym_address = "헬스장 없음"

                    print([name, introduce, price, gym_address])
                    writer.writerow([name, introduce, price,gym_address])

                except Exception as err:
                    print(f'Unexpected {err=}, {type(err)=}')

                finally:
                    driver.switch_to.default_content()
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    print('change window 0')

            end = True
            print('end')
            break
        finally:
            driver.switch_to.default_content()
            