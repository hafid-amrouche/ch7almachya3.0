import requests
import json
import os
from ch7almachya.settings import BASE_DIR
import time

url = "https://api.ouedkniss.com/graphql"
headers = {
  'authority': 'api.ouedkniss.com',
  'accept': '*/*',
  'accept-language': 'fr',
  'authorization': '',
  'content-type': 'application/json',
  'dnt': '1',
  'locale': 'en',
  'origin': 'https://www.ouedkniss.com',
  'referer': 'https://www.ouedkniss.com/',
  'save-data': 'on',
  'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67',
  'x-app-version': '"2.1.28"'
}



file = open(os.path.join(BASE_DIR, 'webscrape_ouedkniss-master/data.json'))
file_data = json.load(file)     
data = file_data['data']     
ann_list = list(data.values())  


def phone_number(id):
    payload = '{\"query\":\"query UnhidePhone($id: ID!) {\\n  phones: announcementPhoneGet(id: $id) {\\n    id\\n    phone\\n    phoneExt\\n    hasViber\\n    hasWhatsapp\\n    hasTelegram\\n    __typename\\n  }\\n}\\n","variables":{"id":"'+id+'"}}'
    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.json())
    return response.json()

i = 0
def func():
    global i
    global current_number
    global prev_number
    j = int(i/2)
    id = ann_list[0]['id']
    current_number = phone_number('37395945')
    print(current_number['data']['phones'][0]['phone'])

    try:
        print(current_number == prev_number)
    except:
        pass

    prev_number = current_number
    i+=1


def setInterval(interval, func):
    while True:
        func()
        time.sleep(interval / 1000)

setInterval(5000, func)

