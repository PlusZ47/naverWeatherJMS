from naverWeather import *
from flask import Flask, request, jsonify

kakapBot = Flask(__name__)

@kakapBot.route("/")
def hello():
    return "Hello goorm!"

@kakapBot.route("/weather",methods=['POST'])
def weather():
    req = request.get_json()
    
    location = req["action"]["detailParams"]["sys_location"]["value"]	# json파일 읽기

    temp = naverWeather(location)
    
    answer = temp.getWeather()
    
    # 답변 텍스트 설정
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer
                    }
                }
            ]
        }
    }

    # 답변 전송
    return jsonify(res)

if __name__ == "__main__":
    kakapBot.run(host="0.0.0.0", port=5000, threaded=True)