import requests
import base64
import os
import json
from utils.config import globalconfig
 
def ocr(imgfile):
     

    headers = {
        'authority': 'aidemo.youdao.com',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://ai.youdao.com',
        'referer': 'https://ai.youdao.com/',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }
    with open(imgfile,'rb') as ff:
        f=ff.read()
    b64=base64.b64encode(f)
    data = {
        'imgBase': 'data:image/jpeg;base64,'+str(b64,encoding='utf8'),
        'lang': '',
        'company': '',
    }

    response = requests.post('https://aidemo.youdao.com/ocrtransapi1', headers=headers, data=data, proxies=  {'http': None,'https': None})
    res=''
    try:
        for l in response.json()['lines']:
            if res!='':
                res+='\n'
            res+=l['tranContent']
    except:
        print(response.json())
    return '<notrans>'+res
 