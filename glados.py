# coding=utf-8
"""
 @Time : 2025/2/22
 @Author : wwf
 Description: 
"""
import requests
import json
import os

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    # "authorization": "88427466544403502978006267476007-900-1440",
    "cache-control": "no-cache",
    "content-type": "application/json;charset=UTF-8",
    "origin": "https://glados.one",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Microsoft Edge\";v=\"132\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"
}


class Glados:
    def __init__(self, cookie):
        cookies_dict = {}
        for cook in cookie.split(';'):
            name, value = cook.strip().split('=')
            cookies_dict[name] = value

        self.session = requests.Session()
        # 将Cookie字典添加到Session对象中
        self.session.cookies.update(cookies_dict)

    def main(self):
        if self.getState() > 0:
            self.checkin()
            print(self.email + '----结果--' + self.message + '----剩余(' + self.time + ')天')  # 日志输出

    def getState(self):
        url = "https://glados.one/api/user/status"
        response = self.session.get(url, headers=headers)
        if response.status_code != 200:
            print(f"status response.status_code is {response.status_code}")
            exit(1)
        res_json = response.json()
        # print(res_json)
        if res_json['code'] == 0:
            time = response.json()['data']['leftDays']
            self.time = str(time).split('.')[0]
            self.email = res_json['data']['email']
            return 1
        else:
            print(f"status 响应内容 code 为：{res_json['code']}")
            exit(1)

    def checkin(self):
        url = "https://glados.one/api/user/checkin"
        data = {
            "token": "glados.one"
        }
        data = json.dumps(data, separators=(',', ':'))
        response = self.session.post(url, headers=headers, data=data)
        if response.status_code != 200:
            print(f"checkin response.status_code is {response.status_code}")
            exit(1)
        res_json = response.json()
        self.message = res_json['message']
        if res_json['code'] == 1:
            print(res_json['list'][0])


if __name__ == '__main__':
    cookies = os.environ.get("GLADOS_COOKIE", []).split("&")
    # cookies = [
    #     'koa:sess=eyJ1c2VySWQiOjQ1NjgzNSwiX2V4cGlyZSI6MTc2NjExMDU2MDY5MywiX21heEFnZSI6MjU5MjAwMDAwMDB9; koa:sess.sig=cXzbdR5GUHZ_NbKGLY4SNMF7Hdo']
    if len(cookies) <= 0:
        print('未获取到COOKIE变量')
        exit(0)
    for cookie in cookies:
        glados = Glados(cookie)
        glados.main()
