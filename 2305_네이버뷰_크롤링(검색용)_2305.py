#230514 네이버 View 크롤링
#필요 패키지 설치1 : pip install beautifulSoup4 // 스크래핑을 위한 패키지. 자바스크립트로 작성된건 가지고 오기 힘듬.
#필요 패키지 설치2 : pip install requests
#필요 패키지 설치3 : pip install lxmll // 구문을 분석하기 위한 파서
#필요 패키지 설치4 : pip install selenium // beautifulSoup 업그레이드 버전. 
#참고강의 : https://youtu.be/XVaC4prLsrY


# ============== 셀레니움을 통한 웹 크롤링(스크롤 기능 있음) ================
from datetime import datetime #시간 조회
from bs4 import BeautifulSoup
from selenium import webdriver
import time #시간 선언

now = datetime.now() #분석 하는 시간대 변수선언

base_url ="https://search.naver.com/search.naver?sm=tab_hty.top&where=view&query=" # ※검색할 url 영역 유동적으로 수정
keyword = input("검색어를 입력하세요 : ")

search_url = base_url + keyword

driver = webdriver.Chrome()
driver.get(search_url)

time.sleep(3) #3초 딜레이

for i in range(5): #5번 반복
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #자바스크립트를 활용하여 최대 스크롤 할 수 있는 만큼 진행.
    time.sleep(1) #1초 딜레이

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# items = soup.select(".api_txt_lines.total_tit")  # ※해당 클래스에 가지고 오려고 하는 '타이틀' 부분 체크해서 수정 + 빈칸은 . 으로 해야 한다.

print("<<네이버 VIEW 크롤링>>")
print("조회일시 : ", now.strftime('%Y-%m-%d %H:%M:%S\n'))
print("검색하신 순위 결과 입니다.\n")

# for e, item in enumerate(items, 1):
#     print(f"{e}위 : {item.text}")

items = soup.select(".total_wrap.api_ani_send") # ※해당 클래스에 가지고 오려고 하는 타이틀 부분 체크해서 수정 + 빈칸은 . 으로 해야 한다.

for rank_num, item in enumerate(items, 1): #출력결과
    print(f"{rank_num}위")
    ad = item.select_one(".link_ad") #광고 게시글은 넘어가기
    if ad:
        print("광고 게시글 입니다.")
        continue

    blog_title = item.select_one(".sub_txt.sub_name").text
    print(f"{blog_title}") #블로그 제목

    post_title = item.select_one(".api_txt_lines.total_tit._cross_trigger")
    print(f"{post_title.text}") #게시글 제목
    print(f"{post_title.get('href')}") #url

    print()

driver.quit() #드라이버 닫음


# ====================기본 웹 크롤링(스크롤 기능 없음)===========================
# from bs4 import BeautifulSoup
# import requests

# base_url ="https://search.naver.com/search.naver?sm=tab_hty.top&where=view&query=" # ※검색할 url 영역 유동적으로 수정
# keyword = input("검색어를 입력하세요 : ")
# search_url = base_url + keyword

# r = requests.get(search_url)
# r.text
# soup = BeautifulSoup(r.text, "html.parser")

# items = soup.select(".total_wrap.api_ani_send") # ※해당 클래스에 가지고 오려고 하는 타이틀 부분 체크해서 수정 + 빈칸은 . 으로 해야 한다.

# for rank_num, item in enumerate(items, 1): #출력결과
#     print(f"<<{rank_num}>>")
#     ad = item.select_one(".link_ad") #광고 게시글은 넘어가기
#     if ad:
#         print("광고 게시글 입니다.")
#         continue

#     blog_title = item.select_one(".sub_txt.sub_name").text
#     print(f"{blog_title}") #블로그 제목

#     post_title = item.select_one(".api_txt_lines.total_tit._cross_trigger")
#     print(f"{post_title.text}") #게시글 제목
#     print(f"{post_title.get('href')}") #url

#     print()