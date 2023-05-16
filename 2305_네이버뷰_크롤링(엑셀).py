from datetime import datetime #시간 조회
from bs4 import BeautifulSoup
from selenium import webdriver
import time #시간 선언
import pandas as pd
from openpyxl import Workbook

now = datetime.now() #분석 하는 시간대 변수선언

print("해당 크롤링은 PC버전으로 수집 되었습니다.")

base_url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=view&query=" # 검색할 url 영역 유동적으로 수정
keyword = input("NAVER VIEW탭에 원하는 검색어를 입력하세요 : ")

search_url = base_url + keyword

driver = webdriver.Chrome()
driver.get(search_url)

time.sleep(3) #3초 딜레이

for i in range(5): #5번 반복
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #자바스크립트를 활용하여 최대 스크롤 할 수 있는 만큼 진행.
    time.sleep(1) #1초 딜레이

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

print("<<네이버 VIEW 크롤링>>")
print("조회일시 : ", now.strftime('%Y-%m-%d %H:%M:%S\n'))
print("조회하신 검색어 순위 결과 입니다.\n")

items = soup.select(".total_wrap.api_ani_send")

wb = Workbook()
ws = wb.active
ws.append(["순위", "블로그 제목", "게시글 제목", "URL"])

for rank_num, item in enumerate(items, 1):
    ad = item.select_one(".link_ad") #광고 게시글은 넘어가기
    if ad:
        print(f"{rank_num}위 : 광고 게시글 입니다.")
        continue

    blog_title = item.select_one(".sub_txt.sub_name").text
    post_title = item.select_one(".api_txt_lines.total_tit._cross_trigger")
    post_url = post_title.get("href")
    print(f"{rank_num}위 : {blog_title}, {post_title.text}, {post_url}")

    ws.append([rank_num, blog_title, post_title.text, post_url])

driver.quit()

now = datetime.now()
filename = f"{keyword} 검색결과 {now.strftime('%Y%m%d_%H%M%S')}.xlsx"
wb.save(filename)
print(f"{filename} 파일로 저장되었습니다.")