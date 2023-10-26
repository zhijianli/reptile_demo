import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# 发送HTTP请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}



for i in range(1, 7):
    # 目标网页URL
    url = 'https://www.haodf.com/hospital/145/keshi/440/tuijian.html?type=keshi&p='+str(i)

    response = requests.get(url, headers=headers)

    # 确保请求成功
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # 获取医生姓名和推荐度
        doctors_info = []
        doctoer_list  = soup.find_all('li', class_='item')
        for doctor in doctoer_list:
            name_span = doctor.find('span', class_='name')
            if name_span is None:
                continue

            goodat = doctor.find('p', class_='goodat')
            if goodat is None:
                continue
            goodat_txt = goodat.get_text(strip=True)
            if "抑郁" not in goodat_txt:
                continue

            avatar = doctor.find('img', class_='avatar').get('src')
            if "https://n1.hdfimg.com/g2/M03/71/DC/yIYBAFw8OIyAQbw2AAAWC2_R7lQ743_200_200_1.png?8901" in avatar:
                continue

            name = name_span.get_text(strip=True)
            grade = doctor.find('span', class_='grade').get_text(strip=True)
            recommendation = doctor.find('span', class_='score').get_text(strip=True)
            doctors_info.append([name, grade,recommendation])

        # 创建DataFrame
        df = pd.DataFrame(doctors_info, columns=['Doctor_Name','Grade', 'Recommendation'])
        filename = 'doctors_info.xlsx'

        if os.path.exists(filename):
            # 读取已存在的Excel文件
            existing_df = pd.read_excel(filename)

            # 将新的数据追加到已有的DataFrame中
            df = pd.concat([existing_df, df], ignore_index=True)

        # 保存为Excel文件
        df.to_excel('doctors_info.xlsx', index=False)

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")