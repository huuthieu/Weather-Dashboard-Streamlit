from requests_html import HTMLSession, HTML
from selenium import webdriver
import time
import re
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

#Kiểm tra xem dữ liệu có hợp pháp không
import urllib.robotparser
rp = urllib.robotparser.RobotFileParser()
rp.set_url('https://www.worldweatheronline.com/robots.txt')
rp.read()
rp.can_fetch('*', 'https://www.worldweatheronline.com/ho-chi-minh-city-weather-history/vn.aspx')

session = HTMLSession()

#Tên file chứa data
filename='weather_data'

url = "https://www.worldweatheronline.com/ho-chi-minh-city-weather-history/vn.aspx"

#tập hợp các loại thời tiết (để phân loại và chuyển về 1 số loại nhất định)
list_w = set()

def create_df(titles, data):
    df = pd.DataFrame(data, columns=titles)
    return df

def process_data(data, day, month):

    titles = [data[0][0]] + ["Temperature"] + data[0][1:-1] + ["Weather","Dir","Day","Month"]
    new_data = []
    for data in data[2:]:
        fix_data = [data[0][:5]] + [data[0][5:]] + data[1:] + [day, month]
        new_data.append(fix_data)

    return titles, new_data

def parse_data (url,filename,year):
    name = f"../data/{filename}_{year}_1.csv"
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(executable_path='/home/primedo/hcmus/DA/Datascience_2016-2/code/chromedriver', chrome_options=chrome_options)
    first = True
    browser.get(url)
    for y in year:
        if ((y%4 == 0)|(y%400==0)):
            ferb_day=30
        else:
            ferb_day = 29
        #danh sách ngày trong tháng (để tìm kiếm ngày trong web)
        #thêm 0 để chỉ số bằng số tháng
        day = [[0],
                  range(1,32),
                  range(1,ferb_day),
                  range(1,32),
                  range(1,31),
                  range(1,32),
                  range(1,31),
                  range(1,32),
                  range(1,32),
                  range(1,31),
                  range(1,32),
                  range(1,31),
                  range(1,32)]    
        for m in range(12):
            m +=1
            if ((m==12)&(y==2019)):
                break;#Chỉ lấy đến tháng 11 năm 2019
            for d in day[m]:
                if (d<10):
                    d = f"0{d}"
                if (m<10):
                    m_str = f"0{m}"
                    text = f"{m_str}{d}{y}"
                else:
                    text = f"{m}{d}{y}"
                #Xác định vị trí của textbox và điền giá trị vào
                textbox = browser.find_element_by_xpath("//input[@id='ctl00_MainContentHolder_txtPastDate']")
                # textbox = browser.find_element("xpath", "//input[@id='ctl00_MainContentHolder_txtPastDate']")
                textbox.click()
                print(text)
                textbox.send_keys(text)
                #Bấm nút để lấy dữ liệu
                button = browser.find_element_by_xpath("//input[@id='ctl00_MainContentHolder_butShowPastWeather']")
                # button = browser.find_element("xpath", "//input[@id='ctl00_MainContentHolder_butShowPastWeather']")
                button.click()
                time.sleep(1)#Nghỉ 1 giây để trang có thời gian load
                
                # r = HTML(html=browser.page_source)
                soup = BeautifulSoup(browser.page_source, 'lxml')
                data = []
                table = soup.find_all('table')[0]
                table_body = table.find('tbody')

                rows = table_body.find_all('tr')
                for i, row in enumerate(rows):
                    cols = row.find_all('td')
                    weather = []
                    dir = []
                    cols_text = [ele.text.strip() for ele in cols]
                    if i > 0 and cols_text != ['']:
                        weather = [cols[1].find_all('img')[0]['alt']]
                        dir =  [re.findall("\(.*\)",cols[-1].find_all('svg')[0]["style"])[0].strip('()')]
                    data.append([ele for ele in cols_text if ele] + weather + dir) # Get rid of empty values
                titles, new_data = process_data(data, d, m)

                if first:
                    df = create_df(titles, new_data)
                    first = False
                else:
                    df = df.append(create_df(titles, new_data), ignore_index=True)
                
                #kiểm tra xem page đã load đúng chưa
                #nếu sai thì tăng thời gian sleep
                # print(r.find(".block_title",first=True).text)
                
                #lấy dữ liệu
                
                # row = r.find(".tb_date",first=True)
                
                # times =re.findall("\d{2}:\d{2}", row.text)
                
                #ghi dữ liệu ra file csv
                if (m==6) and (d==30):
                    df.to_csv(name, index=False)
                    print(f"{y} done")
                    break;

parse_data(url,filename,[2022])