import requests
import json
import base64
import cv2
import numpy as np

a1 = 'G:/python project/project_practice/face/1.jpg'
a2 = 'G:/python project/project_practice/face/2.JPG'
a3 = 'G:/python project/project_practice/face/3.JPG'
faces = {'9559980210373015416': a1, '6224211100235159200': a2, '9559980461946691213': a3}
informations = {a1: ['郑秀妍', '15108220418'], a2: ['李晗', '15103220404'], a3: ['王笙', '15108211818']}

def card_recognition(img_path):
    http_url = 'https://api-cn.faceplusplus.com/cardpp/v1/ocrbankcard'
    data = {"api_key": 'xo87FRq-A2JSd0OEjCm-ayclcIShyiI1',
            "api_secret": 'Qe8K8p8RAJ57b13TtzXKaeiHPOyUyyzq',
                }
    files = {"image_file": open(img_path, "rb")}
    response = requests.post(http_url, data=data, files=files)
    print(response.text)
    data = json.loads(response.text)
    attr = data['bank_cards'][0]['number']
    print(attr)
    return attr

def person_beauty(img_path):
    http_url = 'https://api-cn.faceplusplus.com/facepp/v1/beautify'
    data = {"api_key": 'xo87FRq-A2JSd0OEjCm-ayclcIShyiI1',
            "api_secret": 'Qe8K8p8RAJ57b13TtzXKaeiHPOyUyyzq',
            "whitening": 100,
            "smoothing": 100
                }
    files = {"image_file": open(img_path, "rb")}
    response = requests.post(http_url, data=data, files=files)
    print(response.text)
    data = json.loads(response.text)
    img_data = base64.b64decode(data['result'])
    img_array = np.fromstring(img_data, np.uint8)
    img = cv2.imdecode(img_array, cv2.COLOR_RGB2BGR)
    return img



if __name__ == "__main__":
    b = card_recognition('bank_card/3.jpg')
    img = faces[b]
    name = informations[img][0]
    person_number = informations[img][1]
    img = person_beauty(img)
    text = "name:{0},phone_number:{1}".format(name, person_number)
    cv2.putText(img, text, (30, 40), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow('image', img)
    cv2.waitKey(0)


