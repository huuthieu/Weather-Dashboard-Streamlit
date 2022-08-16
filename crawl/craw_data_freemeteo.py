from bs4 import BeautifulSoup
import requests
import re
import time
import pandas as pd

def get_url():
    dict_url = {
    "An Giang": "https://freemeteo.vn/thoi-tiet/long-xuyen/history/daily-history/?gid=1575627&station=11437&date=2022-07-22&language=vietnamese&country=vietnam",
    "Bà Rịa - Vũng Tàu": "https://freemeteo.vn/thoi-tiet/vung-tau/history/daily-history/?gid=1562414&station=11437&date=2022-07-22&language=vietnamese&country=vietnam",
    "Bạc Liêu": "https://freemeteo.vn/thoi-tiet/bac-lieu/history/daily-history/?gid=1591474&station=11437&date=2022-07-22&language=vietnamese&country=vietnam",
    "Bắc Giang": "https://freemeteo.vn/thoi-tiet/bac-giang/history/daily-history/?gid=1591527&station=11376&date=2022-07-22&language=vietnamese&country=vietnam",
    "Bắc Kạn": "https://freemeteo.vn/thoi-tiet/bac-kan/history/daily-history/?gid=1591538&station=11376&date=2022-07-22&language=vietnamese&country=vietnam",
    "Bắc Ninh": "https://freemeteo.vn/thoi-tiet/bac-ninh/history/daily-history/?gid=1591449&station=11376&date=2022-07-22&language=vietnamese&country=vietnam",
    "Bến Tre": "https://freemeteo.vn/thoi-tiet/ben-tre/history/daily-history/?gid=1587976&station=11437&date=2022-07-22&language=vietnamese&country=vietnam",
    "Bình Định": "https://freemeteo.vn/thoi-tiet/quy-nhon/history/daily-history/?gid=1568574&station=11397&date=2022-07-22&language=vietnamese&country=vietnam",
    "Bình Dương": "https://freemeteo.vn/thoi-tiet/thu-dau-mot/history/daily-history/?gid=1565022&station=11437&date=2022-07-22&language=vietnamese&country=vietnam",
    "Bình Phước": "https://freemeteo.vn/thoi-tiet/dong-xoai/history/daily-history/?gid=1582436&station=11437&date=2022-07-22&language=vietnamese&country=vietnam",
    "Bình Thuận": "https://freemeteo.vn/thoi-tiet/phan-thiet/history/daily-history/?gid=1571058&station=11437&date=2022-07-22&language=vietnamese&country=vietnam",
    
    # "Cà Mau": "https://freemeteo.vn/thoi-tiet/ca-mau/history/daily-history/?gid=1586443&station=11437&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Cao Bằng": "https://freemeteo.vn/thoi-tiet/cao-bang/history/daily-history/?gid=1586185&station=11376&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Cần Thơ": "https://freemeteo.vn/thoi-tiet/can-tho/history/daily-history/?gid=1586203&station=11437&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Đà Nẵng":"https://freemeteo.vn/thoi-tiet/da-nang/history/daily-history/?gid=1583992&station=11397&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Đắk Lắk": "https://freemeteo.vn/thoi-tiet/buon-ma-thuot/history/daily-history/?gid=1586896&station=11437&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Đắk Nông": "https://freemeteo.vn/thoi-tiet/ban-ndoh/history/daily-history/?gid=1589388&station=11437&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Đồng Nai": "https://freemeteo.vn/thoi-tiet/bien-hoa/history/daily-history/?gid=1587923&station=11437&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Đồng Tháp": "https://freemeteo.vn/thoi-tiet/cao-lanh/history/daily-history/?gid=1586151&station=11437&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Gia Lai": "https://freemeteo.vn/thoi-tiet/pleiku/history/daily-history/?gid=1569684&station=11397&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Hà Giang": "https://freemeteo.vn/thoi-tiet/ha-giang/history/daily-history/?gid=1581349&station=11376&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Hà Nam": "https://freemeteo.vn/thoi-tiet/phu-ly/history/daily-history/?gid=1570449&station=11376&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Hà Nội": "https://freemeteo.vn/thoi-tiet/hanoi/history/daily-history/?gid=1581130&station=11376&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Hà Tây": "https://freemeteo.vn/thoi-tiet/ba-dinh/history/daily-history/?gid=7289846&station=11376&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Hà Tĩnh": "https://freemeteo.vn/thoi-tiet/ha-tinh/history/daily-history/?gid=1581047&station=11394&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Thành phố Hồ Chí Minh" : "https://freemeteo.vn/thoi-tiet/ho-chi-minh-city/history/daily-history/?gid=1566083&station=11437&date=2022-07-25&language=vietnamese&country=vietnam",

    # "Hải Dương": "https://freemeteo.vn/thoi-tiet/hai-duong/history/daily-history/?gid=1581326&station=11376&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Hải Phòng": "https://freemeteo.vn/thoi-tiet/haiphong/history/daily-history/?gid=1581298&station=11376&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Hậu Giang": "https://freemeteo.vn/thoi-tiet/ap-dong-binh-1/history/daily-history/?gid=1593537&station=11437&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Hòa Bình": "https://freemeteo.vn/thoi-tiet/hoa-binh/history/daily-history/?gid=1580830&station=11376&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Điện Biên": "https://freemeteo.vn/thoi-tiet/dien-bien-phu/history/daily-history/?gid=1583477&station=11376&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Hưng Yên": "https://freemeteo.vn/thoi-tiet/hung-yen/history/daily-history/?gid=1580142&station=11376&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Kiên Giang": "https://freemeteo.vn/thoi-tiet/rach-gia/history/daily-history/?gid=1568510&station=11437&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Kon Tum": "https://freemeteo.vn/thoi-tiet/kon-tum/history/daily-history/?gid=1578500&station=11397&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Khánh Hòa": "https://freemeteo.vn/thoi-tiet/nha-trang/history/daily-history/?gid=1572151&station=11437&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Lai Châu": "https://freemeteo.vn/thoi-tiet/a-me/history/daily-history/?gid=1594542&station=11376&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Lạng Sơn": "https://freemeteo.vn/thoi-tiet/lang-son/history/daily-history/?gid=1576633&station=11376&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Lào Cai": "https://freemeteo.vn/thoi-tiet/lao-cai/history/daily-history/?gid=1576303&station=11376&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Lâm Đồng": "https://freemeteo.vn/thoi-tiet/da-lat/history/daily-history/?gid=1584071&station=11437&date=2022-07-22&language=vietnamese&country=vietnam",
    
    # "Long An": "https://freemeteo.vn/thoi-tiet/tan-an/history/daily-history/?gid=1567069&station=11437&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Nam Định": "https://freemeteo.vn/thoi-tiet/nam-dinh/history/daily-history/?gid=1573517&station=11376&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Ninh Bình": "https://freemeteo.vn/thoi-tiet/ninh-binh/history/daily-history/?gid=1571968&station=11376&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Ninh Thuận": "https://freemeteo.vn/thoi-tiet/phan-rang-thap-cham/history/daily-history/?gid=1571067&station=11437&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Nghệ An": "https://freemeteo.vn/thoi-tiet/vinh/history/daily-history/?gid=1562798&station=11376&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Phú Thọ": "https://freemeteo.vn/thoi-tiet/viet-tri/history/daily-history/?gid=1562820&station=11376&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Phú Yên": "https://freemeteo.vn/thoi-tiet/tuy-hoa/history/daily-history/?gid=1563281&station=11397&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Quảng Bình": "https://freemeteo.vn/thoi-tiet/dong-hoi/history/daily-history/?gid=1582886&station=11394&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Quảng Nam":"https://freemeteo.vn/thoi-tiet/tam-ky/history/daily-history/?gid=1567148&station=11397&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Quảng Ninh": "https://freemeteo.vn/thoi-tiet/ha-long/history/daily-history/?gid=1580410&station=11376&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Quảng Ngãi": "https://freemeteo.vn/thoi-tiet/quang-ngai/history/daily-history/?gid=1568770&station=11397&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Quảng Trị": "https://freemeteo.vn/thoi-tiet/dong-ha/history/daily-history/?gid=1582926&station=11394&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Sóc Trăng": "https://freemeteo.vn/thoi-tiet/soc-trang/history/daily-history/?gid=1567788&station=11437&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Sơn La": "https://freemeteo.vn/thoi-tiet/son-la/history/daily-history/?gid=1567681&station=11376&date=2022-07-22&language=vietnamese&country=vietnam",
    
    # "Tây Ninh": "https://freemeteo.vn/thoi-tiet/tay-ninh/history/daily-history/?gid=1566559&station=11437&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Tiền Giang": "https://freemeteo.vn/thoi-tiet/my-tho/history/daily-history/?gid=1574023&station=11437&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Tuyên Quang": "https://freemeteo.vn/thoi-tiet/tuyen-quang/history/daily-history/?gid=1563287&station=11376&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Thái Bình": "https://freemeteo.vn/thoi-tiet/thai-binh/history/daily-history/?gid=1566346&station=11376&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Thái Nguyên": "https://freemeteo.vn/thoi-tiet/thai-nguyen/history/daily-history/?gid=1566319&station=11376&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Thanh Hóa": "https://freemeteo.vn/thoi-tiet/thanh-hoa/history/daily-history/?gid=1566166&station=11376&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Thừa Thiên Huế": "https://freemeteo.vn/thoi-tiet/hue/history/daily-history/?gid=1580240&station=11394&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Trà Vinh": "https://freemeteo.vn/thoi-tiet/tra-vinh/history/daily-history/?gid=1563926&station=11437&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Vĩnh Long": "https://freemeteo.vn/thoi-tiet/vinh-long/history/daily-history/?gid=1562693&station=11437&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Vĩnh Phúc": "https://freemeteo.vn/thoi-tiet/vinh-yen/history/daily-history/?gid=1562548&station=11376&date=2022-07-22&language=vietnamese&country=vietnam",
    # "Yên Bái": "https://freemeteo.vn/thoi-tiet/yen-bai/history/daily-history/?gid=1560349&station=11376&date=2022-07-22&language=vietnamese&country=vietnam"
}
    return dict_url

def parse_data(url,province,year):
    name = f"../data/{year[0]}/weather_data_{province}_{year}.csv"
    print(name)

    first = True
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

            for d in day[m]:
                if (d<10):
                    d = f"0{d}"
                if (m<10):
                    m_str = f"0{m}"
                    # text = f"{m_str}{d}{y}"
                    text = f"{y}-{m_str}-{d}"
                else:
                    # text = f"{m}{d}{y}"
                    text = f"{y}-{m}-{d}"
                print(text)
            
                url = re.sub("date=[0-9\-]*", "=".join(["date",text]), url)
                print(url)
                r = requests.get(url)
                print(r.status_code)
                if r.status_code != 200:
                    time.sleep(5)
                    r = requests.get(url)
                # soup = BeautifulSoup(r.text, 'lxml')
                y_1, m_1 ,d_1 = text.split("-")
                if first:               
                    df = pd.read_html(r.text)[-3].drop(["Mô tảChi tiết"],axis=1)  
                    df["date"] = d_1
                    df["month"] = m_1
                    df["year"] = y_1
                    first = False
                else:
                    tmp_df = pd.read_html(r.text)[-3].drop(["Mô tảChi tiết"],axis=1)
                    tmp_df["date"] = d_1
                    tmp_df["month"] = m_1
                    tmp_df["year"] = y_1
                    df = df.append(tmp_df, ignore_index=True)
                
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
                    return

def parse_data_province(years):
    dict_url = get_url()
    for key in dict_url:
        parse_data(dict_url[key],key,years)


parse_data_province([2022])