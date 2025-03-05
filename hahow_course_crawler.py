import requests
import pandas as pd

import os

from dotenv import load_dotenv
load_dotenv()

url="https://api.hahow.in/api/products/search?category=COURSE&filter=PUBLISHED&limit=24&page=0&sort=TRENDING"

headers = {'User-Agent': os.getenv('USER_AGENT')}

response = requests.get(url,headers=headers)
if response.status_code == 200:
    data = response.json()
    products = data['data']['courseData']['products']
    course_list = []
    for product in products:
        course_data = [
            product['title'],
            product['averageRating'],
            product['price'],
            product['numSoldTickets']
        ]
        course_list.append(course_data)
    df = pd.DataFrame(course_list, columns=["課程名稱","評價","價格","購買人數"])
    df.to_excel('courses.xlsx', index=False, engine="openpyxl")
    print("成功！")
else:
    print("無法取得網頁")