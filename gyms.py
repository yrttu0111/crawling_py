from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup


#브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 애러 메세지 제거
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

Service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=Service, options=chrome_options)


driver.get('https://map.naver.com/v5/search')
time.sleep(4)

search_box = driver.find_element(By.CSS_SELECTOR, ".input_search")
search_box.send_keys("가천대"+"헬스장")

search_box.send_keys(Keys.ENTER)
time.sleep(4)

driver.implicitly_wait(time_to_wait=60)
print('Search Loading Complete')

before_h = driver.execute_script("return window.scrollY")

#스크롤 내리기 이동 전 위치

driver.switch_to.frame('searchIframe')
itemlist = driver.find_element(By.XPATH, '//*[@id="_pcmap_list_scroll_container"]')

scroll_location = 1
scroll_height = -1

while scroll_location != scroll_height:
    
    scroll_location = driver.execute_script("return document.querySelector('#_pcmap_list_scroll_container').scrollHeight")
	
    #현재 스크롤의 가장 아래로 내림
    driver.execute_script("arguments[0].scrollTo(0, document.querySelector('#_pcmap_list_scroll_container').scrollHeight)", itemlist)

    #전체 스크롤이 늘어날 때까지 대기
    time.sleep(0.3)
    
    #늘어난 스크롤 높이
    scroll_height = driver.execute_script("return document.querySelector('#_pcmap_list_scroll_container').scrollHeight")

print('Find Loading Complete')

html = driver.page_source # 셀레니움으로 가져오기


soup = BeautifulSoup(html, 'html.parser') # BS4 로 HTML 로 파싱

re_dict = {}
#_pcmap_list_scroll_container > ul > li:nth-child(2) > div.qbGlu > div.ouxiq > a:nth-child(1) > div > div > span.YwYLL
#_pcmap_list_scroll_container > ul > li:nth-child(3) > div.qbGlu > div.ouxiq > a:nth-child(1) > div > div > span.YwYLL
num = 1
for i in soup.select('#_pcmap_list_scroll_container > ul > li'):
    if '광고' in i.text:
        continue
    name = i.select_one('div > a > div > div > span').text
    # print(i)
    try:
        ddd = driver.find_element(By.XPATH, f'//*[@id="_pcmap_list_scroll_container"]/ul/li[{num}]/div[1]/div[2]/a[1]')
    except:
        ddd = driver.find_element(By.XPATH, f'//*[@id="_pcmap_list_scroll_container"]/ul/li[{num}]/div[1]/div/a[1]/div/div')
    ddd.click()
    time.sleep(4)
    re_dict[name] = {}

    driver.switch_to.frame('entryIframe')
    print('iframe')
    html2 = driver.page_source # 셀레니움으로 가져오기
    soup2 = BeautifulSoup(html2, 'html.parser') # BS4 로 HTML 로 파싱
    gym = soup2.select('#_title > div > span.Fc1rA ')
    

    time.sleep(1)
    print(gym)
    # for j in i.select('div > a > div > span'):
    #     word = j.text
    #     print(j.text)
    #     if '별점' in word:
    #         word = word.replace('별점', '')
    #         re_dict[name]['별점'] = float(word)
    #     elif '방문자' in word or '블로그' in word:
    #         word = word.split()
    #         word[-1] = word[-1].replace(',', '')
    #         re_dict[name][word[0]] = int(word[-1])
    print (num)
    num = num + 1


driver.close()

# for i in range(1, 20):
#     time.sleep(2)
#     js_script = "document.querySelector(\"body > app > layout > div > div.container > div.router-output > " \
#                 "shrinkable-layout > search-layout > search-list > search-list-contents > perfect-scrollbar\").innerHTML"
#     raw = driver.execute_script("return " + js_script)

#     html = BeautifulSoup(raw, "html.parser")

#     print(html)

#     contents = html.select("div > div.ps-content > div > div > div .item_search")
#     for s in contents:
#         search_box_html = s.select_one(".search_box")

#         name = search_box_html.select_one(".title_box .search_title .search_title_text").text
#         print("식당명: " + name)
#         try:
#             phone = search_box_html.select_one(".search_text_box .phone").text
#         except:
#             phone = "NULL"
#         print("전화번호: " + phone)
#         address = search_box_html.select_one(By.CSS_SELECTOR, ".ng-star-inserted .address").text
#         print("주소: " + address)

#         print("--"*30)

#     try:
#         next_btn = driver.find_element("button.btn_next")
#         next_btn.click()
#     except:
#         print("데이터 수집 완료")
#         break

#     driver.close()