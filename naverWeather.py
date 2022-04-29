import requests
from bs4 import BeautifulSoup
import re
import csv

class naverWeather():
    session = requests.Session() 
    # 예전 url 주소
    # addr = "http://weather.naver.com/rgn/cityWetrCity.nhn?cityRgnCd=CT"
    addr = "https://weather.naver.com/today/"
    map_cityNum = {}


    with open('cityNumber.csv', mode='r', encoding="utf-8") as inp:
        reader = csv.reader(inp)
        map_cityNum = {rows[0]:rows[1].replace('"','').strip() for rows in reader}
    
    def __init__(self, area):
        self.area = area
        self.addr = None
        self.result = None

        cityNum = naverWeather.map_cityNum[area]
        self.addr = naverWeather.addr + cityNum
        
        self.search()

    def search(self):
        naverWeather.session.encoding = 'utf-8'

        req = naverWeather.session.get(self.addr)
        soup = BeautifulSoup(req.text, "html.parser")
        location = soup.find(class_='location_name')
        table = soup.find(class_="week_list")
        t_ary = list(table.stripped_strings)

                        
        self.result = ("[" + self.area + "(" + location.text +")"+" 날씨 검색 결과]\n"
                    + "- 오늘(" + t_ary[1] +")\n"
                    + " \t 오전 - " + t_ary[11][:-1] + "℃ (" + t_ary[5] + ", 강수확률 : " + t_ary[4] + ")\n"
                    + " \t 오후 - " + t_ary[14][:-1] + "℃ (" + t_ary[9] + ", 강수확률 : " + t_ary[8] + ")\n"
                    + "- 내일(" + t_ary[16] + ")\n"
                    + " \t 오전 - " + t_ary[26][:-1] + "℃ (" + t_ary[20] + ", 강수확률 : " + t_ary[19] + ")\n"
                    + " \t 오후 - " + t_ary[29][:-1] + "℃ (" + t_ary[24] + ", 강수확률 : " + t_ary[23] + ")\n")

    def getWeather(self):
        if not self.result:
            # 도시명을 잘못 입력한 경우 결과가 나오지 않는다.
            return "잘못된 도시명입니다"
        return self.result