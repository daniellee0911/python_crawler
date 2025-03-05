import requests
import os
import json
import pandas as pd
from bs4 import BeautifulSoup

from dotenv import load_dotenv
load_dotenv()

headers = {'User-Agent': os.getenv('USER_AGENT')}
url = "https://www.ptt.cc/bbs/NBA/index.html"


def download_html(page_url):
    response = requests.get(page_url,headers=headers)
    
    if response.status_code == 200:
        with open('ptt_nba.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("寫入成功！")
    else:
        print("沒有抓到網頁")


def parser_html_and_export_json(page_url):
    response = requests.get(page_url,headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("div", class_="r-ent")
    data_list = []
    for article in articles:
        data = {}
        title = article.find("div", class_="title")
        if title and title.a:
            title = title.a.text
        else:
            title= "沒有標題"
        data["標題"] = title

        popular = article.find("div", class_="nrec")
        if popular and popular.span:
            popular = popular.span.text
        else:
            popular = "N/A" 
        data["人氣"] = popular

        date = article.find("div", class_="date")
        if date:
            date = date.text
        else:
            date = "N/A"   
        data["日期"] = date
        data_list.append(data)       
        # print(f"標題：{title} 人氣：{popular} 日期：{date}")
    with open('ppt_nba_data.json', 'w', encoding='utf-8') as f:
        json.dump(data_list,f, ensure_ascii=False, indent=4)
    print("資料已經儲存為 ppt_nba_data.json")



def parser_html_and_export_excel(page_url):
    response = requests.get(page_url,headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("div", class_="r-ent")
    data_list = []
    for article in articles:
        data = {}
        title = article.find("div", class_="title")
        if title and title.a:
            title = title.a.text
        else:
            title= "沒有標題"
        data["標題"] = title

        popular = article.find("div", class_="nrec")
        if popular and popular.span:
            popular = popular.span.text
        else:
            popular = "N/A" 
        data["人氣"] = popular

        date = article.find("div", class_="date")
        if date:
            date = date.text
        else:
            date = "N/A"   
        data["日期"] = date
        data_list.append(data)       
        # print(f"標題：{title} 人氣：{popular} 日期：{date}")
    df = pd.DataFrame(data_list)
    df.to_excel("ptt_nba.xlsx", index=False, engine="openpyxl")

    
download_html(url)
parser_html_and_export_json(url)
parser_html_and_export_excel(url)