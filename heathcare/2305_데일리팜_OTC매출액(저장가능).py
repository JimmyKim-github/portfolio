# 데일리팜 '약국 일반약 매출액 Top 100' 크롤링

import requests
from bs4 import BeautifulSoup
import pandas as pd

# 웹 페이지에 접속하여 HTML 가져오기
base_url = "http://www.dailypharm.com/Users/DrugSaleInfo/?ID="

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
    cells = [cell.text.strip() if cell.text != "None" else "" for cell in row.find_all("td")]
    data.append(cells)

# 데이터프레임 생성
df = pd.DataFrame(data[1:], columns=data[0])

df_sorted = df.sort_index()
# sorted_df = df.sort_values(by=["제품명"], ascending=False) # by=["제품명"] 내용 입력시 해당 기준으로 정렬, True - 오름차순 , False - 내림차순

print('요청하신 ID 결과물 입니다.', '\n')
print('<<약국 일반약 매출액 Top 100>>')

# 데이터프레임 출력 설정 변경
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_columns', None)

# 정렬된 데이터프레임 출력 (공백 없이)
df_sorted.dropna(how='all', inplace=True)  # 모든 값이 없는 행 삭제
df_sorted.reset_index(drop=True, inplace=True)  # 인덱스 재설정
print(df_sorted.to_string(index=False, index_names=False), '\n')

file_save = input("파일로 저장하시겠습니까? (y/n): ")
if file_save.lower() == 'y':
    file_name = input("저장할 파일 이름을 입력하세요 (확장자 없이): ")
    file_path = f"{file_name}.csv"
    df.to_csv(file_path, index=False, encoding='utf-8-sig')
    print(f"작성하신 '{file_path}' 파일명으로 저장되었습니다.")
else:
    print("파일 저장이 취소되었습니다.")