from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import pandas as pd

browser=webdriver.Chrome()
browser.maximize_window() # 창 최대화

url="https://naver.com"
browser.get(url) # url 이동

dream="프로그래머"
fileName="dream_link.txt"

elem_Query=browser.find_element_by_id("query")
elem_Query.clear()
elem_Query.send_keys(dream)
browser.find_element_by_id("search_btn").click()

html_source=browser.page_source
soup=BeautifulSoup(html_source, 'lxml')
elem_Data = soup.find_all("div", attrs={"class":"total_wrap api_ani_send"})
df = []
for t in elem_Data:
    if(t.find("a", attrs={"class":"api_txt_lines total_tit _cross_trigger"})):
        title=t.find("a", attrs={"class":"api_txt_lines total_tit _cross_trigger"}).get_text()
        content_url=t.find("a", attrs={"class":"api_txt_lines total_tit _cross_trigger"})["href"]
        df.append([title,content_url])
        print("title : ",title,"\ncontent_url : ",content_url)


#--------데이터 저장--------

# 데이터 프레임 만들기
newDf=pd.DataFrame(columns=["title","url_link"])
# 자료 집어넣기
for i in range(len(df)):
    newDf.loc[i] = df[i]
# 저장하기
# 현재 작업폴더 안의 data 폴더에 저장
df_dir = "./data/" # 저장할 디렉토리
newDf.to_csv(df_dir+"dream_search_df.csv", index=False, encoding="utf-8-sig")
## 컬럼 정보 저장
# 컬럼 설명 테이블
col_names=["title","url_link"]
col_exp=["컨텐츠 제목", "연결 링크"]
new_exp=pd.DataFrame({"col_names":col_names,"col_explanation":col_exp})
# 현재 작업폴더 안의 data 폴더에 저장
df_dir = "./data/" # 저장할 디렉토리
new_exp.to_csv(df_dir+"dream_col_exp.csv",index=False,encoding='utf-8-sig')


browser.quit()
