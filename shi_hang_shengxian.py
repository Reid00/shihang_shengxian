import requests, json, sys


def login(Phone='18896510223', PassWord='584a58a1d207b8b2983d9cf45c98018d'):
    url = 'https://api1.34580.com/sz/Sign/SignInV2'
    headers = {

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    payload = {

        'SourceType': 9,
        'Phone': Phone,
        'PassWord': PassWord
    }

    # res = requests.post(url, data=json.dumps(payload), headers=headers)
    res = requests.post(url, json=payload, headers=headers)
    print(res.url)
    print(res.status_code)
    print(res.json())
    data = res.json()
    is_error = data['Error']
    if is_error:
        print('Login Failed, {}'.format(data['Message']))
        sys.exit(1)
    else:
        print('Login Successfully.')
        return data['Data']['CustomerGuid'], data['Data']['AccessToken']


def signin(customerguid, accesstoken):
    # url = 'https://activity-3.m.duiba.com.cn/signactivity/doSign'
    url = 'https://wechat.34580.com/authorize?'
    auto_login = 'https://api1.34580.com/sz/duiba/autoLogin?'
    get_sign_info = 'https://activity-3.m.duiba.com.cn/signactivity/getSignInfo'

    do_sign = 'https://activity-3.m.duiba.com.cn/signactivity/doSign'

    headers = {

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Referer': 'https://wechatx.34580.com/home/'
    }

    querystring = {
        'cityId': 1,
        'accesstoken': accesstoken,
        'customerguid': customerguid,
    }
    get_payload = {
        'sourcetype': 9,
        'accesstoken': accesstoken,
        'customerguid': customerguid,
    }

    with requests.Session() as s:
        res = s.post(url, json=querystring, headers=headers)
        res = s.get(auto_login, json=get_payload, headers=headers)
        print(res.status_code)
        print(res.json())
        message = res.json()['msg']
        print(message)
        payload = {

            'signActivityId': '90'
        }
        res_get_sign = s.post(get_sign_info, json=payload, headers=headers)

        res_do_sign = s.post(do_sign, json=payload, headers=headers)
        data = res_do_sign.json()
        is_error = data['success']
        if is_error:
            print(data['signInfoVO'])
            print('签到成功，获取{}个积分'.format(data['Data']['GetPoints']))
        else:
            print('sign in failed.')


if __name__ == '__main__':
    Phone = input('please enter phone number:')
    PassWord = input('please enter password:')
    # 584a58a1d207b8b2983d9cf45c98018d
    # customerguid, accesstoken = login(Phone.strip(),PassWord.strip())
    customerguid, accesstoken = login()
    # signin()
    signin(customerguid, accesstoken)
