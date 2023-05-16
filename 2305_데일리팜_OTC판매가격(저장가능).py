# 데일리팜 '지역별 다빈도 일반약 판매가격 정보' 크롤링

import requests
from bs4 import BeautifulSoup
import pandas as pd

# 웹 페이지에 접속하여 HTML 가져오기
base_url = "http://www.dailypharm.com/Users/DrugPriceInfo/?ID="

# 사용자로부터 입력 받은 사이트 주소
site_id = input("사이트 뒤에 ID '숫자'만 입력하세요: ")

# 완성된 URL
url = base_url + site_id

# 조합된 URL 요청 진행
response = requests.get(url)
html_content = response.content

# BeautifulSoup을 사용하여 HTML 파싱
soup = BeautifulSoup(html_content, "html.parser")

# 표 내용 추출
table = soup.find("table")
data = []
header_row = table.find("tr")
headers = [header.text for header in header_row.find_all("th")]
data.append(headers)

rows = table.find_all("tr")[1:]
for row in rows:
    cells = [cell.text if cell.text != "None" else "" for cell in row.find_all("td")]
    data.append(cells)

# 데이터프레임 생성
df = pd.DataFrame(data[1:], columns=data[0])

df_sorted = df.sort_index()
# sorted_df = df.sort_values(by=["제품명"], ascending=False) # by=["제품명"] 내용 입력시 해당 기준으로 정렬, True - 오름차순 , False - 내림차순

print('요청하신 ID 결과물 입니다.', '\n')
print('<<지역별 다빈도 일반약 판매가격 정보>>')
# 정렬된 데이터프레임 출력
print(df_sorted,'\n')

file_name = input("저장할 파일 이름을 입력하세요 (확장자 없이): ")
file_path = f"{file_name}.csv"
df.to_csv(file_path, index=False, encoding='utf-8-sig')

print(f"작성하신 '{file_path}' 파일명으로 저장되었습니다.")
