import requests
import time
import re
from datetime import datetime
from bs4 import BeautifulSoup

print("※ 해당 코드는 PC버전 네이버 뉴스 기준으로 검색됩니다.")

news_search = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query="
news_keyword = input("원하는 뉴스 키워드를 검색하세요: ")
url = news_search + news_keyword

response = requests.get(url)

print('\n', "<<검색하신 헤드라인 결과입니다.>>")
print("조회일시:", datetime.now().strftime('%Y-%m-%d %H:%M:%S\n'))

html = response.text
soup = BeautifulSoup(html, 'html.parser')
links = soup.select(".news_tit")

for link in links:
    title = link.text
    url = link.attrs['href']

    # 언론사 가져오기
    press_element = link.find_next(class_="info press")
    press = press_element.text.strip() if press_element else "언론사 정보 없음"

    # 기사 제목, URL, 언론사 출력하기
    print("제목:", title)
    print("URL:", url)
    print("언론사:", press)
    print("---------------------")
