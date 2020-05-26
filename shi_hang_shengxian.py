import requests, json, sys
from faker import Faker

class ShiHang:
    # 食行生鲜 登录签到脚本

    faker = Faker()
    def __init__(self,user='your user account', password='your password'):
        #　初始化
        self.user = user
        self.password = password
        self.headers = {'User-Agent':self.faker.user_agent()}

    def login(self):
        # 登录食行生鲜
        print('开始登录...')
        url = 'https://api1.34580.com/sz/Sign/SignInV2'

        payload = {
            'DeviceId':'',
            'PassWord': self.password,
            'Phone': self.user,
            'SourceType': '9',
            'ZhuGeDeviceMd5':''
        }
        print(payload)
        res = requests.post(url, json=payload, headers=self.headers)

        print('response is:',res.json())
        data = res.json()
        is_error = data['Error']
        if is_error:
            print('Login Failed, {}'.format(data['Message']))
            sys.exit(1)
        else:
            print('Login Successfully.')
            return data['Data']['CustomerGuid'], data['Data']['AccessToken']


    def signin(self,customerguid, accesstoken):
        # 进行脚本签到
        print('开始签到...')
        url = 'https://api1.34580.com/sz/Logs/LogV2?'
        do_sign = 'https://activity-3.m.duiba.com.cn/signactivity/doSign'
        cookie = {
            '_ac': 'eyJhaWQiOjUyODE5LCJjaWQiOjI5MzQ1NjA2MjN9',
            'acw_tc': '76b20fe715522894476124948e62309daddb6eee59da9076ed6fc2e34bc95c',
            'tokenId': 'b8cd760480a00623d717930c139217c3',
            'wdata3': 'jaH8Bq8XcNMD5YguCwRQ1xEb44U5Fuy5u7ZESkAzK4s2DWGtZYqXpuyZSYb8oB7rohMZvnrdafqvBp5jaekHcKgwgWm9hkkUCFYVw1xUUFByLP1FAyFAoFkF28ZU1k5gcBgY8oAgsCPxq7znG2Uk3uyGTfu6rBa6xTNqbdP8',
            'wdata4': 'UJg2alH4X2YBGV4bUc2Dxjf7rpXb4bExzJdKKn42Prr0WEkqBhLdpH49b7Rrnm8sMfPW6KUG4H9ciu1iI+/RgJecoRk+7PEKu+B1OWNiP1qGDFh4ttahxfKEZXvuNbLXiv7RY+UmbNOHbHeeEyiT2wk2HWXoMLGuHl0AmhSlAys=',
        }
        forms = {
            'id': 90
        }
        querystring = {
            # 'cityId': 1,
            'sourcetype': 9,
            'accesstoken': accesstoken,
            'customerguid': customerguid,
        }

        with requests.Session() as s:
            res = s.post(url, json=querystring, headers=self.headers)
            print(res.status_code)

            data = res.json()
            print(data)

            is_error = data['Error']
            if is_error:
                print(f'go sign in page failed with error message: {data["Message"]}')
            else:
                print(f'go sign in successfully with message: {data["Message"]}')

            res_dosign = s.post(do_sign, cookies=cookie, headers=self.headers, data=forms)
            dosign_cont = res_dosign.json()
            
            if dosign_cont['success']:
                print('today sign status {}'.format(dosign_cont['signInfoVO']['todaySigned']))
                # print(f'sign in successfully, get {dosign_cont["Data"]["GetPoints"]} points')
            else:
                print(f'sign in failed with message: {dosign_cont["message"]}')

if __name__ == '__main__':
    client = ShiHang()
    customerguid, accesstoken = client.login()
    client.signin(customerguid, accesstoken)
