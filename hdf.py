import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

# 爬取好大夫网页的爬虫代码




def extract_number(text):
    # 使用正则表达式查找括号中的数字
    match = re.search(r'\((\d+)\)', text)

    # 如果找到匹配项，则返回数字
    if match:
        return int(match.group(1))
    else:
        return None


# 定义一个函数来处理链接
def process_url(url):
    # 首先，我们使用split方法根据斜杠('/')拆分URL
    parts = url.split('/')

    # 然后，我们获取最后一个元素，也就是最后一个斜杠后面的部分
    last_part = parts[-1]

    # 最后，我们使用replace方法去掉.html
    result = last_part.replace('.html', '')

    return result

# 发送HTTP请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}



for i in range(1, 7):
    # 目标网页URL
    url = 'https://www.haodf.com/hospital/827/keshi/17753/tuijian-yiyuzheng.html?p='+str(i)

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

            # goodat = doctor.find('p', class_='goodat')
            # if goodat is None:
            #     continue
            # goodat_txt = goodat.get_text(strip=True)
            # if "抑郁" not in goodat_txt:
            #     continue

            avatar = doctor.find('img', class_='avatar').get('src')
            if "https://n1.hdfimg.com/g2/M03/71/DC/yIYBAFw8OIyAQbw2AAAWC2_R7lQ743_200_200_1.png?8901" in avatar:
                continue

            # 判断评价数据
            is_continue = False
            doctor_href = doctor.find('a', class_='item-bd').get('href')
            doctor_id = process_url(doctor_href)
            pingjia_url = "https://www.haodf.com/doctor/"+str(doctor_id)+"/pingjia-zhenliao.html"
            ping_response = requests.get(pingjia_url, headers=headers)

            if ping_response.status_code == 200:
                ping_soup = BeautifulSoup(ping_response.text, 'html.parser')

                ping_num_list = ping_soup.find_all('a', class_='sift-href')
                for ping_num in ping_num_list:
                    ping_num_text = ping_num.get_text(strip=True)
                    if "全部" in ping_num_text:
                        ping_number = extract_number(ping_num_text)
                        if ping_number < 10:
                            is_continue = True
                    elif "一般/不满意" in ping_num_text:
                        ping_number = extract_number(ping_num_text)
                        if ping_number > 5:
                            is_continue = True
                if is_continue:
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