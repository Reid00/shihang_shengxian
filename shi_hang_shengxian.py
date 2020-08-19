# -*- encoding: utf-8 -*-
'''
@File        :shi_hang_shengxian.py
@Time        :2020/08/17 16:00:49
@Author      :Reid
@Version     :1.0
@Desc        :苏州食行生鲜签到脚本
'''


import requests
import json
from faker import Faker


faker = Faker()

def login(user='18896510223', password='584a58a1d207b8b2983d9cf45c98018d'):
    """
    登陆页面
    :param user: 登陆的账号
    :param password: passwd
    """
    url = 'https://api1.34580.com/sz/Sign/SignInV2?sourcetype=9'
    print('start login...')
    payload = {
        'DeviceId':'',
        'PassWord':password,
        'Phone': user,
        'SourceType': '9',
        'ZhuGeDeviceMD5':''
    }
    headers = {
        'User-Agent': faker.user_agent(),
        'Referer':'https://wechatx.34580.com/mart/'
    }
    res = requests.post(url, data=json.dumps(payload), headers=headers)
    data = json.loads(res.text)
    if not data.get('Error'):
        print('login successfully!')
        return data['Data']['CustomerGuid'], data['Data']['AccessToken']
    return None, None


def sign_in(CustomerGuid, AccessToken):
    """
    签到脚本
    """
    # url = f'https://api1.34580.com/sz/Logs/LogV2?accesstoken={AccessToken}&customerguid={CustomerGuid}&sourcetype=9'
    auto_login = 'https://api1.34580.com/sz/duiba/autoLogin'
    sign_action = 'https://activity-3.m.duiba.com.cn/signactivity/doSign'
    headers = {
        'User-Agent': faker.user_agent(),
        'Refer':'https://wechatx.34580.com/duiba/',
    }
    params = {
        'customerguid': CustomerGuid,
        'accesstoken': AccessToken,
        'sourcetype': '9'
    }
    sign_form = {
        'id':90
    }
    with requests.Session() as sess:
        print('start go to auto login page...')
        log_res = sess.get(auto_login, params=params, headers=headers)
        data = json.loads(log_res.text)
        #response is {"Error":0,"Message":"","Data":"https://activity-3.m.duiba.com.cn/autoLogin/autologin?uid=adaf2997-7867-43c0-999f-42e1399ab4b4&credits=37&sign=f5da5ae159c82be342e30b46b72b0abb&appKey=4JG2CKkeAVxFzRK7iTWuP9imPtNK&timestamp=1597740357184&","Exception":null}
        if not data.get('Error'):
            new_url = data['Data']
            new_response = sess.get(new_url, allow_redirects=False)
            if new_response.status_code == 302:
                jar = new_response.cookies
                redirect_url = new_response.headers['Location']
                print('redirect_url: ', redirect_url)
                res2 = sess.get(redirect_url, cookies=jar)
            cookies = new_response.cookies.get_dict()
            print('cookies:', cookies)
            print('start sign in...')
            headers = {
                'User-Agent': faker.user_agent(),
                'Refer': redirect_url,
            }
            sign_res = sess.post(sign_action, data=sign_form, cookies=cookies, headers=headers)
            data = sign_res.text
            print(data)

if __name__ == '__main__':
    CustomerGuid, AccessToken = login()
    sign_in(CustomerGuid, AccessToken)
    # ShiHang = ShiHang()
    # A, B  = ShiHang.login()
    # ShiHang.signin(A, B)
