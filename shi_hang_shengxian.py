import requests, json, sys


def login(Phone='***', PassWord='***'):
    url = 'https://api1.34580.com/sz/Sign/SignInV2'
    headers = {

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    payload = {

        'SourceType': 9,
        'Phone': Phone,
        'PassWord': PassWord
    }

    res = requests.post(url, json=payload, headers=headers)
    print(res.url)
    # print(res.status_code)
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
    url = 'https://api1.34580.com/sz/Logs/LogV2?'
    # auto_login = 'https://api1.34580.com/sz/duiba/autoLogin?'
    # get_sign_info = 'https://activity-3.m.duiba.com.cn/signactivity/getSignInfo'
    do_sign = 'https://activity-3.m.duiba.com.cn/signactivity/doSign'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    }
    payload = {
        'Host': 'activity - 3.m.duiba.com.cn',
        'Connection': 'keep - alive',
        'Content - Length': '6',
        'Accept': 'application / json, text / plain, * / *',
        'Origin': 'https: // activity - 3.m.duiba.com.cn',
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, like  Gecko) Chrome / 72.0 .3626 .121 Safari / 537.36',
        'Content - Type': 'application / x - www - form - urlencoded',
        'Referer': 'https: // activity - 3.m.duiba.com.cn / chome / index?from=login & spm = 52819.1.1.1',
    }

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
        res = s.post(url, json=querystring, headers=headers)
        print(res.status_code)
        data = res.json()
        print(data)
        is_error = data['Error']
        if is_error:
            print(data['Message'])
        else:
            print('Message: {}'.format(data['Message']))

        res_dosign = s.post(do_sign, cookies=cookie, headers=headers, data=forms)
        dosign_cont = res_dosign.json()
        if dosign_cont['success']:
            print('today sign status {}'.format(dosign_cont['signInfoVO']['todaySigned']))
        else:
            print('sign failed')


if __name__ == '__main__':
    # Phone = input('please enter phone number:')
    # PassWord = input('please enter password:')
    # 584a58a1d207b8b2983d9cf45c98018d
    # customerguid, accesstoken = login(Phone.strip(),PassWord.strip())
    customerguid, accesstoken = login()
    # signin()
    signin(customerguid, accesstoken)
