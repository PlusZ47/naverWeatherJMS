from naverWeather import *

while True:  
    print("\n날씨를 알고 싶은 도시명을 입력하세요(ex: 서울, 제주) : ", end="")
    print("\nq를 누르면 종료합니다.")
    print(">> ", end="")
    city = input()
    print("\n")

    if city == "q":
        print("종료.")
        break
    if city not in naverWeather.map_cityNum:
        print("잘못된 도시명입니다.")
        continue

    temp = naverWeather(city)
    
    print(temp.getWeather())
    print("====== 오늘 기온에 맞는 옷 추천 ======")
    for fits in temp.getFits():
        print(fits.replace('"','').strip())

