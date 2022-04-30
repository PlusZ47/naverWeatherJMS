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
    temp_wearingFits = list()

    # csv 파일 open 후 딕셔너리, 리스트에 저장. 지역번호, 옷관련 정보 파일은 csv에 저장되어있음.
    with open('cityNumber.csv', mode='r', encoding="utf-8") as citys:
        reader = csv.reader(citys)
        map_cityNum = {rows[0]:rows[1].replace('"','').strip() for rows in reader}

    with open('wearing.csv', mode='r', encoding="utf-8") as clothes:
        reader = csv.reader(clothes)
        temp_wearingFits = list(reader)

    def __init__(self, area):
        self.area = area
        self.addr = None
        self.result = None
        self.fits = list()

        cityNum = naverWeather.map_cityNum[area]
        self.addr = naverWeather.addr + cityNum
        
        self.search()

    # 네이버 날씨 data 크롤링
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

        self.fits = self.recommandFits(t_ary)

    # 기온에 맞게 옷 정보를 반환
    def recommandFits(self, t_ary):
        fits = list()
        avr = (int(t_ary[11][:-1]) + int(t_ary[14][:-1])) / 2

        if (avr >= 28):
            fits = self.temp_wearingFits[0]
        elif (avr >= 23 and avr <= 27):
            fits = self.temp_wearingFits[1]
        elif (avr >= 20 and avr <= 22):
            fits = self.temp_wearingFits[2]
        elif (avr >= 17 and avr <= 19):
            fits = self.temp_wearingFits[3]
        elif (avr >= 12 and avr <= 16):
            fits = self.temp_wearingFits[4]
        elif (avr >= 9 and avr <= 11):
            fits = self.temp_wearingFits[5]
        elif (avr >= 5 and avr <= 8):
            fits = self.temp_wearingFits[6]
        else:
            fits = self.temp_wearingFits[7]
        
        return fits
    
    def getWeather(self):
        if not self.result:
            # 도시명을 잘못 입력한 경우 결과가 나오지 않는다.
            return "잘못된 도시명입니다"
        return self.result

    def getFits(self):
        if not self.fits:
            return "기온이 잘못되었습니다."
        return self.fits