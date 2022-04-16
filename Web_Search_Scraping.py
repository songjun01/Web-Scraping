from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime

now = datetime.now()
current_time=int(now.strftime("%H"))

search_word=input("검색어를 입력하세요 : ")
browser=webdriver.Chrome()
browser.maximize_window() # 창 최대화

url="https://search.naver.com/search.naver?where=nexearch&sm=tab_jum&query="+search_word
browser.get(url) # url 이동
df = []

#-------------Scraping NAVER, YOUTUBE-------------
def webScraping_Naver_Youtube(page_url,find_all_tag,find_all_attrs_class,find_all_attrs,find_tag,find_attrs_class,find_attrs):
    browser.get(page_url)
    if(page_url=="https://search.naver.com/search.naver?where=view&sm=tab_jum&query="+search_word or page_url=="https://www.youtube.com/results?search_query="+search_word):
        count_num=0
        while(count_num<5):
            browser.execute_script("window.scrollTo(0,document.documentElement.scrollHeight)")
            time.sleep(0.5)
            count_num=count_num+1
    elif(page_url=="https://search.shopping.naver.com/search/all?where=all&frm=NVSCTAB&query="+search_word):
        count_num=0
        while(count_num<3):
            browser.execute_script("window.scrollTo(0,document.documentElement.scrollHeight)")
            time.sleep(0.5)
            count_num=count_num+1
    html_source=browser.page_source
    soup=BeautifulSoup(html_source, 'lxml')
    elem_Data_View = soup.find_all(find_all_tag, attrs={find_all_attrs_class:find_all_attrs})
    for t in elem_Data_View:
        if(t.find(find_tag, attrs={find_attrs_class:find_attrs})):
            title=t.find(find_tag, attrs={find_attrs_class:find_attrs}).get_text()
            content_url=t.find(find_tag, attrs={find_attrs_class:find_attrs})["href"]
            if(page_url=="https://www.youtube.com/results?search_query="+search_word):
                content_url="https://www.youtube.com"+t.find(find_tag, attrs={find_attrs_class:find_attrs})["href"]
            df.append([title,content_url])

#-------------Scraping GOOGLE, DAUM-------------
def webScraping_Google_Daum(page_url,find_all_tag,find_all_attrs_class,find_all_attrs,find_tag):
    browser.get(page_url)
    html_source=browser.page_source
    soup=BeautifulSoup(html_source, 'lxml')
    elem_Data_View = soup.find_all(find_all_tag, attrs={find_all_attrs_class:find_all_attrs})
    for t in elem_Data_View:
        if(t.find(find_tag)):
            title=t.find(find_tag).get_text()
            content_url=t.find(find_tag)["href"]
            df.append([title,content_url])

#-------------NextPage GOOGLE, DAUM-------------
def while_Google_Daum(page_url,find_all_tag,find_all_attrs_class,find_all_attrs,find_tag,para_num,para_str,maxNum,plusNum):
    fusion_page_num=para_num
    fusion_page_str=para_str
    while(fusion_page_num<maxNum):
        webScraping_Google_Daum(page_url+fusion_page_str,find_all_tag,find_all_attrs_class,find_all_attrs,find_tag)
        fusion_page_num=fusion_page_num+plusNum
        fusion_page_str=str(fusion_page_num)


#아침,점심,저녁 모두 다른 사이트로 검색
if(current_time>=0 and current_time<=9):            #다음
    while_Google_Daum("https://search.daum.net/search?w=fusion&DA=PGD&enc=utf8&q="+search_word+"&p=","div","class","wrap_cont","a",1,"1",6,1)
    while_Google_Daum("https://search.daum.net/search?w=brunch&DA=PGD&enc=utf8&q="+search_word+"&page=","strong","class","tit_cont","a",1,"1",6,1)
    while_Google_Daum("https://search.daum.net/search?w=news&DA=PGD&enc=utf8&cluster=y&cluster_page=1&q="+search_word+"&p=","div","class","wrap_cont","a",1,"1",6,1)
elif(current_time>=10 and current_time<=16):        #네이버
    webScraping_Naver_Youtube("https://search.naver.com/search.naver?where=view&sm=tab_jum&query="+search_word,"div","class","total_wrap api_ani_send","a","class","api_txt_lines total_tit _cross_trigger")
    webScraping_Naver_Youtube("https://search.naver.com/search.naver?where=news&sm=tab_jum&query="+search_word,"div","class","news_wrap api_ani_send","a","class","news_tit")
    webScraping_Naver_Youtube("https://search.naver.com/search.naver?where=news&sm=tab_jum&query="+search_word+"&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=82&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=11","div","class","news_wrap api_ani_send","a","class","news_tit")
    webScraping_Naver_Youtube("https://search.naver.com/search.naver?where=news&sm=tab_jum&query="+search_word+"&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=82&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=21","div","class","news_wrap api_ani_send","a","class","news_tit")
    webScraping_Naver_Youtube("https://search.naver.com/search.naver?where=news&sm=tab_jum&query="+search_word+"&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=82&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=31","div","class","news_wrap api_ani_send","a","class","news_tit")
    webScraping_Naver_Youtube("https://search.naver.com/search.naver?where=news&sm=tab_jum&query="+search_word+"&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=82&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=41","div","class","news_wrap api_ani_send","a","class","news_tit")
    webScraping_Naver_Youtube("https://search.naver.com/search.naver?where=video&sm=tab_jum&query={}&nso=so%3Ar%2Cp%3Aall%2Ca%3Aall".format(search_word),"div","class","info_area","a","class","info_title")
    webScraping_Naver_Youtube("https://search.shopping.naver.com/search/all?where=all&frm=NVSCTAB&query="+search_word,"div","class","basicList_title__3P9Q7","a","class","basicList_link__1MaTN")
    webScraping_Naver_Youtube("https://book.naver.com/search/search.nhn?query="+search_word,"dl","style","width:654px","a","target","_blank")
elif(current_time>=17 and current_time<=23):        #구글,유튜브
    while_Google_Daum("https://www.google.com/search?q="+search_word+"&start=","div","class","yuRUbf","a",0,"10",50,10)
    webScraping_Naver_Youtube("https://www.youtube.com/results?search_query="+search_word,"div","id","title-wrapper","a","id","video-title")


#-------------데이터 저장-------------

# 데이터 프레임 만들기
newDf=pd.DataFrame(columns=["title","url_link"])
# 자료 집어넣기
for i in range(len(df)):
    newDf.loc[i] = df[i]
# 저장하기
# 현재 작업폴더 안의 data 폴더에 저장
df_dir = "./data/" # 저장할 디렉토리
newDf.to_csv(df_dir+search_word+"_search_df.csv", index=False, encoding="utf-8-sig")
## 컬럼 정보 저장
# 컬럼 설명 테이블
col_names=["title","url_link"]
col_exp=["컨텐츠 제목", "연결 링크"]
new_exp=pd.DataFrame({"col_names":col_names,"col_explanation":col_exp})
# 현재 작업폴더 안의 data 폴더에 저장
df_dir = "./data/" # 저장할 디렉토리
new_exp.to_csv(df_dir+search_word+"_col_exp.csv",index=False,encoding='utf-8-sig')


browser.quit()



#-------------naver_view-------------
#webScraping_Naver("https://search.naver.com/search.naver?where=view&sm=tab_jum&query="+search_word,"div","class","total_wrap api_ani_send","a","class","api_txt_lines total_tit _cross_trigger")
#-------------naver_news-------------
#webScraping_Naver("https://search.naver.com/search.naver?where=news&sm=tab_jum&query="+search_word,"div","class","news_wrap api_ani_send","a","class","news_tit")
#-------------naver_books-------------
#webScraping_Naver("https://book.naver.com/search/search.nhn?query="+search_word,"dl","style","width:654px","a","target","_blank")
#-------------naver_shopping-------------
#webScraping_Naver("https://search.shopping.naver.com/search/all?where=all&frm=NVSCTAB&query="+search_word,"div","class","basicList_title__3P9Q7","a","class","basicList_link__1MaTN")
#-------------naver_video-------------
#webScraping_Naver("https://search.naver.com/search.naver?where=video&sm=tab_jum&query={}&nso=so%3Ar%2Cp%3Aall%2Ca%3Aall".format(search_word),"div","class","info_area","a","class","info_title")
#-------------google-------------
#webScraping_Google_Daum("https://www.google.com/search?q={}&start=0".format(search_word),"div","class","yuRUbf","a")
#-------------daum_brunch-------------
#webScraping_Google_Daum("https://search.daum.net/search?w=brunch&DA=PGD&enc=utf8&q={}&page=1".format(search_word),"strong","class","tit_cont","a")
#-------------daum_news-------------
#webScraping_Google_Daum("https://search.daum.net/search?w=news&DA=PGD&enc=utf8&cluster=y&cluster_page=1&q={}&p=1".format(search_word),"div","class","wrap_cont","a")
#-------------daum_fusion-------------
#webScraping_Google_Daum("https://search.daum.net/search?w=fusion&DA=PGD&enc=utf8&q={}8&p=1".format(search_word),"div","class","wrap_cont","a")

'''
if(current_time>=0 and current_time<=9):        #뉴스
    webScraping_Naver("https://search.naver.com/search.naver?where=news&sm=tab_jum&query="+search_word,"div","class","news_wrap api_ani_send","a","class","news_tit")
    webScraping_Naver("https://search.naver.com/search.naver?where=news&sm=tab_jum&query="+search_word+"&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=82&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=11","div","class","news_wrap api_ani_send","a","class","news_tit")
    webScraping_Naver("https://search.naver.com/search.naver?where=news&sm=tab_jum&query="+search_word+"&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=82&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=21","div","class","news_wrap api_ani_send","a","class","news_tit")
    webScraping_Naver("https://search.naver.com/search.naver?where=news&sm=tab_jum&query="+search_word+"&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=82&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=31","div","class","news_wrap api_ani_send","a","class","news_tit")
    webScraping_Naver("https://search.naver.com/search.naver?where=news&sm=tab_jum&query="+search_word+"&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=82&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=41","div","class","news_wrap api_ani_send","a","class","news_tit")
elif(current_time>=10 and current_time<=16):    #view, 쇼핑, 도서
    webScraping_Naver("https://search.naver.com/search.naver?where=view&sm=tab_jum&query="+search_word,"div","class","total_wrap api_ani_send","a","class","api_txt_lines total_tit _cross_trigger")
    webScraping_Naver("https://search.shopping.naver.com/search/all?where=all&frm=NVSCTAB&query="+search_word,"div","class","basicList_title__3P9Q7","a","class","basicList_link__1MaTN")
    webScraping_Naver("https://book.naver.com/search/search.nhn?query="+search_word,"dl","style","width:654px","a","target","_blank")
elif(current_time>=17 and current_time<=23):    #뉴스, 동영상, 쇼핑, 도서
    webScraping_Naver("https://search.naver.com/search.naver?where=news&sm=tab_jum&query="+search_word,"div","class","news_wrap api_ani_send","a","class","news_tit")
    webScraping_Naver("https://search.naver.com/search.naver?where=news&sm=tab_jum&query="+search_word+"&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=82&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=11","div","class","news_wrap api_ani_send","a","class","news_tit")
    webScraping_Naver("https://search.naver.com/search.naver?where=news&sm=tab_jum&query="+search_word+"&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=82&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=21","div","class","news_wrap api_ani_send","a","class","news_tit")
    webScraping_Naver("https://search.naver.com/search.naver?where=news&sm=tab_jum&query="+search_word+"&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=82&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=31","div","class","news_wrap api_ani_send","a","class","news_tit")
    webScraping_Naver("https://search.naver.com/search.naver?where=news&sm=tab_jum&query="+search_word+"&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=82&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=41","div","class","news_wrap api_ani_send","a","class","news_tit")
    webScraping_Naver("https://search.naver.com/search.naver?where=video&sm=tab_jum&query={}&nso=so%3Ar%2Cp%3Aall%2Ca%3Aall".format(search_word),"div","class","info_area","a","class","info_title")
    webScraping_Naver("https://search.shopping.naver.com/search/all?where=all&frm=NVSCTAB&query="+search_word,"div","class","basicList_title__3P9Q7","a","class","basicList_link__1MaTN")
    webScraping_Naver("https://book.naver.com/search/search.nhn?query="+search_word,"dl","style","width:654px","a","target","_blank")
'''