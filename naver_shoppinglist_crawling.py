from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv

#크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

#브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

#불필요한 에러 메시지 없애기
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

#브라우저 생성
browser = webdriver.Chrome('/Users/ham/Documents/chromedriver_mac64/chromedriver')

#웹사이트 열기
browser.get('https://www.naver.com/')
browser.implicitly_wait(10) #10초 기다림

#쇼핑 메뉴 클릭
browser.find_element(By.CSS_SELECTOR, "#NM_FAVORITE > div.group_nav > ul.list_nav.type_fix > li:nth-child(5) > a").click()
time.sleep(2) #2초 기다림

#검색창 클릭
search = browser.find_element(By.CSS_SELECTOR, "#__next > div > div.pcHeader_header__tXOY4 > div > div > div._gnb_header_area_150KE > div > div._gnbLogo_gnb_logo_3eIAf > div > div._gnbSearch_gnb_search_3O1L2 > form > div._gnbSearch_inner_2Zksb > div > input")
search.click()

#검색어 입력
search.send_keys('크록스 내피')
search.send_keys(Keys.ENTER)

#등록순으로 선택
browser.find_element(By.CSS_SELECTOR, "#content > div.style_content__xWg5l > div.seller_filter_area > div > div.subFilter_sort_box__FpfWA > a:nth-child(9)").click()

#파일 생성
f = open(r"/Users/ham/Desktop/J/naver_shopping_crawling.csv", 'w', encoding='CP949', newline='')
csvwriter = csv.writer(f)

while True:
    #스크롤 전 높이
    before_h = browser.execute_script("return window.scrollY")

    #무한 스크롤
    while True:
        browser.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END)

        #스크롤 사이 페이지 로딩 시간
        time.sleep(1)

        #스크롤 후 높이
        after_h = browser.execute_script("return window.scrollY")

        if after_h == before_h:
            break
        before_h = after_h

    #상품 정보 div
    items = browser.find_elements(By.CSS_SELECTOR, ".basicList_info_area__TWvzp")

    for item in items:
        name = item.find_element(By.CSS_SELECTOR, ".basicList_title__VfX3c").text
        try:
            price = item.find_element(By.CSS_SELECTOR, ".price_num__S2p_v").text
        except:
            price = "판매중단"
        categories = item.find_elements(By.CSS_SELECTOR, ".basicList_depth__SbZWF .basicList_category__cXUaZ")
        cate1 = categories[0].text if len(categories) >= 1 else ""
        cate2 = categories[1].text if len(categories) >= 2 else ""
        cate3 = categories[2].text if len(categories) >= 3 else ""
        cate4 = categories[3].text if len(categories) >= 4 else ""
        # link = item.find_element(By.CSS_SELECTOR, ".basicList_title__VfX3c > a").get_attribute('href')
        print(name, price, cate1, cate2, cate3, cate4)

        #데이터 쓰기
        csvwriter.writerow([name, price, cate1, cate2, cate3, cate4])

    # 다음 버튼 클릭
    try:
        next_button = browser.find_element(By.CSS_SELECTOR, ".pagination_next__pZuC6")
        if "disabled" not in next_button.get_attribute("class"):
            next_button.click()
        else:
            break
    except:
        break

#파일 닫기
f.close()