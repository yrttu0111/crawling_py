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
NAVER_URL = "https://map.naver.com/v5/search"
SEARCH_TEXT = "가천대 헬스장"

#브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 애러 메세지 제거
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

Service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=Service, options=chrome_options)

driver.get(NAVER_URL)

time.sleep(3)

# for initalize
driver.switch_to.default_content()

with open('result.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["name", "type" ,"address", "phone", "introduce"])

# search keyword
search_box = driver.find_element(By.CSS_SELECTOR ,".input_search")
search_box.send_keys(SEARCH_TEXT + '헬스장')

time.sleep(1)

search_box.send_keys(Keys.ENTER)

time.sleep(1.5)

with open('result.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    
    while True:
        # scroll to load lazyload element
        try:
            driver.switch_to.frame("searchIframe")

            scroll_container = driver.find_element(By.ID, "_pcmap_list_scroll_container")
            for i in range(10):
                driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight)", scroll_container)
                time.sleep(0.2)

        finally:
            driver.switch_to.default_content()

        # Get Data and write
        try:
            driver.switch_to.frame("searchIframe")
            boxes = driver.find_elements(By.CLASS_NAME ,"VLTHu")

            for i in range(len(boxes)):
                try:
                    isAdd = driver.find_element(By.CSS_SELECTOR ,"#_pcmap_list_scroll_container > ul > li:nth-child(" + str(i + 1) + ") > div.qbGlu > a > span").text
                    print(isAdd)
                    if isAdd == '광고':
                        continue
                except:
                    pass
                # print(i)
                driver.find_element(By.CSS_SELECTOR ,"#_pcmap_list_scroll_container > ul > li:nth-child(" + str(i + 1) + ") > div.qbGlu > div > a.P7gyV").click()
                driver.switch_to.default_content()

                time.sleep(2)

                try:
                    driver.switch_to.frame("entryIframe")
                    time.sleep(0.5)
                    address_opener = driver.find_element(By.XPATH ,'//*[@id="app-root"]/div/div/div/div[5]/div/div[2]/div/div/div[1]/div/a/span[2]')
                    address_opener.click()
                    driver.find_element(By.CSS_SELECTOR,'body').send_keys(Keys.PAGE_DOWN)
                    time.sleep(0.6)
                    # businessHours_opener = driver.find_element(By.XPATH ,'//*[@id="app-root"]/div/div/div/div[5]/div/div[2]/div/div/div[3]/div/a')
                    # businessHours_opener.click()
                    text_css_selectors = [
                    '#app-root > div > div > div > div:nth-child(6) > div > div:nth-child(2) > div > div > div:nth-child(11) > div > a > span.zPfVt',
                    '#app-root > div > div > div > div:nth-child(6) > div > div:nth-child(2) > div > div > div:nth-child(10) > div > a > span.zPfVt',
                    '#app-root > div > div > div > div:nth-child(6) > div > div:nth-child(2) > div > div > div:nth-child(9) > div > a > span.zPfVt',
                    '#app-root > div > div > div > div:nth-child(6) > div > div:nth-child(2) > div > div > div:nth-child(8) > div > a > span.zPfVt',
                    '#app-root > div > div > div > div:nth-child(6) > div > div:nth-child(2) > div.place_section_content > div > div:nth-child(8) > div > a > span.zPfVt'
                    ]

                    for css_selector in text_css_selectors:
                        try:
                            text_opener = driver.find_element(By.CSS_SELECTOR, css_selector)
                            text_opener.click()
                            break  # 요소를 찾고 클릭했으므로 반복문 종료
                        except :
                            pass  # 해당 요소를 찾지 못한 경우 다음 CSS 선택자로 이동
                    time.sleep(0.3)
                    driver.find_element(By.CSS_SELECTOR,'body').send_keys(Keys.PAGE_UP)
                    time.sleep(0.5)
                    address_opener.click()
                    time.sleep(0.5)
                    

                    page_source = driver.page_source
                    soup = BeautifulSoup(page_source, "html.parser")
                    # place_name = driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[5]/div/div[2]/div/div/div[1]/div/a/span[1]').text
                    try:
                        place_name = soup.select("#_title > div > span")[0].string
                    except:
                        place_name = '미등록'

                    try:
                        place_type = soup.select("#_title > div > span.DJJvD")[0].string
                    except:
                        place_type = '미등록'

                    try:
                        place_address = soup.select('#app-root > div > div > div > div:nth-child(5) > div > div:nth-child(2) > div > div > div.O8qbU.tQY7D > div > a > span.LDgIH')[0].string
                    except:
                        place_address = '미등록'

                    try:
                        place_phone = soup.select("#app-root > div > div > div > div:nth-child(5) > div > div:nth-child(2) > div > div > div.O8qbU.nbXkr > div > span.xlx7Q ")[0].string
                    except:
                        place_phone = '미등록'

                    try:
                        place_introduce = text_opener.text
                    except:
                        place_introduce = '미등록'

                    

                    print([place_name,place_type, place_address, place_phone, place_introduce])
                    # writer.writerow([place_name, place_address + '(' + place_post + ')', place_phone])
                except Exception as err:
                    print(f'Unexpected {err=}, {type(err)=}')

                finally:
                    driver.switch_to.default_content()
                    driver.switch_to.frame("searchIframe")

            next_page_button_svg = driver.find_element(By.CSS_SELECTOR ,'#app-root > div > div.XUrfU > div.zRM9F > a.eUTV2 > svg')[1]    
            is_page_end = driver.execute_script("return window.getComputedStyle(arguments[0]).getPropertyValue('opacity') === '0.4'", next_page_button_svg)

            if is_page_end == True:
                break
                    
        finally:
            driver.switch_to.default_content()
        
        # goto next page
        try:
            driver.switch_to.frame("searchIframe")
            frame = driver.find_element(By.CSS_SELECTOR ,'#app-root > div > div.XUrfU > div.zRM9F > a.eUTV2')[1]
            frame.click()
        finally:
            driver.switch_to.default_content()


