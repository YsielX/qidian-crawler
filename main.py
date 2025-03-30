from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from Crypto.Cipher import DES3, AES
from Crypto.Util.Padding import pad
from hashlib import md5
import requests
import base64
import time
import gzip
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

session = requests.Session()

def encrypt_password(password):

    public_key_str = """MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC+ca+tWW42rQyjC4r4iefGj+vNpZWe4frxl/u1CBYxjCwMT1E+v6PxEPf0CKya7o7SfAcNsKhiN6YIRYMXnEvvRsZRlrvA0UicWZMCLBAMI6TnCz2vlKfjolORmp112j4iOCH6S+v/UomGuMvyW1KuOM0ttpEDkW/NiKNke0rJQQIDAQAB"""

    public_key_bytes = base64.b64decode(public_key_str)
    public_key = serialization.load_der_public_key(public_key_bytes)

    # 使用 RSA/ECB/PKCS1Padding 加密
    encrypted = public_key.encrypt(
        password.encode(),
        padding.PKCS1v15()
    )

    encrypted_base64 = base64.b64encode(encrypted).decode()

    # print("加密后的 Base64 编码字符串：", encrypted_base64)
    return encrypted_base64

def get_signature():
    data = f"867262039360829|258cd120c69ca5bdf0ec1505100018d17217|{int(time.time())}".encode()

    key = DES3.adjust_key_parity(b'sewxf03hhz3ew9qcCXMHiDMk')

    iv = 0x31746E3133336873.to_bytes(8, byteorder='little')

    cipher = DES3.new(key, DES3.MODE_CBC, iv)

    encrypted_data = cipher.encrypt(pad(data, DES3.block_size))
    # print("Encrypted data:", base64.b64encode(encrypted_data).decode())
    return base64.b64encode(encrypted_data).decode()

def fock_sign(x: bytes):
    v2 = -1
    for i in range(len(x)):
        v3 = x[i]
        v4 = v2 ^ v3
        v5 = -(v4 & 1) & 0xEDB88320 ^ (v4 >> 1)
        v6 = -((v4 >> 1) & 1) & 0xEDB88320 ^ (v5 >> 1)
        v7 = -((v5 >> 1) & 1) & 0xEDB88320 ^ (v6 >> 1)
        v8 = -((v6 >> 1) & 1) & 0xEDB88320 ^ (v7 >> 1)
        v9 = -((v7 >> 1) & 1) & 0xEDB88320 ^ (v8 >> 1)
        v10 = -((v8 >> 1) & 1) & 0xEDB88320 ^ (v9 >> 1)
        v2 = -((v10 >> 1) & 1) & 0xEDB88320 ^ ((-((v9 >> 1) & 1) & 0xEDB88320 ^ (v10 >> 1)) >> 1)
    func_index = ~v2 & 0xFFFFFFFF
    
def SDK_sign(timestamp: int, data={}):
    data = {k.lower(): v for k, v in sorted(data.items(), key=lambda item: item[0].lower())}
    url = '&'.join([f'{k}={v}' for k, v in data.items()])
    data = f"qYJ]Q9FYhq?|{timestamp}|305355756|864651032226271_02:00:00:00:00:00|1|7.9.374|0|{md5(url.encode()).hexdigest()}|f189adc92b816b3e9da29ea304d4a7e4".encode()
    key = DES3.adjust_key_parity(b'8YV#U2Butm,VutR2B_W[*}6t')

    iv = 0x3736353433323130.to_bytes(8, byteorder='little')

    cipher = DES3.new(key, DES3.MODE_CBC, iv)

    encrypted_data = cipher.encrypt(pad(data, DES3.block_size))
    # print("Encrypted data:", base64.b64encode(encrypted_data).decode())
    return base64.b64encode(encrypted_data).decode()

def check_captcha():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'turing.captcha.qcloud.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'com.qidian.QDReader',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 9; CLT-AL00 Build/HUAWEICLT-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 TCSDK/1.0.2'
    }
    data = {
        'aid': '1600000770',
        'protocol': 'https',
        'accver': '1',
        'showtype': 'popup',
        'ua': 'TW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDk7IENMVC1BTDAwIEJ1aWxkL0hVQVdFSUNMVC1BTDAwOyB3dikgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi80LjAgQ2hyb21lLzc0LjAuMzcyOS4xMzYgTW9iaWxlIFNhZmFyaS81MzcuMzYgVENTREsvMS4wLjI=',
        'noheader': '0',
        'fb': '1',
        'aged': '0',
        'enableAged': '0',
        'enableDarkMode': '0',
        'grayscale': '1',
        'clientype': '1',
        'cap_cd': '',
        'uid': '',
        'lang': 'zh-cn',
        'entry_url': 'file:///android_asset/tcaptcha_webview.html',
        'elder_captcha': '0',
        'js': '/tcaptcha-frame.5e0f125a.js',
        'login_appid': '',
        'wb': '1',
        'subsid': '1',
        'callback': '_aq_243916',
        'sess': '',
    }
    r = session.get(
        'https://turing.captcha.qcloud.com/cap_union_prehandle',
        headers=headers,
        params=data,
        verify=False,
    )
    print(r.text)

    cap_union_prehandle = json.loads(r.text[11:-1])
    url = cap_union_prehandle['data']['dyn_show_info']['sprite_url']
    print(url)
    

def login(username, password):
    headers = {
        'referer': 'http://android.qidian.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'ptlogin.qidian.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.12.6',
    }
    data = {
        'referer': 'http://android.qidian.com',
        'auto': '1',
        'ticket': '0',
        'signature': get_signature(),
        'format': 'json',
        'source': '1000027',
        'version': '1416',
        'devicetype': 'HUAWEI_CLT-AL00',
        'sdkversion': '360',
        'password': encrypt_password(password),
        'areaid': '30',
        'autotime': '30',
        'appid': '12',
        'devicename': 'HUAWEI P20 Pro',
        'returnurl': 'http://www.qidian.com',
        'osversion': 'Android9_7.9.374_1416',
        'username': username,
    }
    r = session.post(
        'https://ptlogin.qidian.com/sdk/staticlogin',
        data=data,
        headers=headers,
        verify=False,
    )
    print(r.text)
    ywkey = json.loads(r.text)['data']['ywKey']

    # check_captcha()

    bind_alias = {
        's_id': '2',
        'qimei': '258cd120c69ca5bdf0ec1505100018d17217',
        'alias': '305355756'
    }
    reports =  json.dumps(bind_alias).replace(' ', '').encode()
    reports = base64.b64encode(gzip.compress(reports)).decode()
    key, iv = "55d69739044b4901", "9268774885601032"
    aes = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
    sign = aes.encrypt(pad(reports[-8:].encode(), AES.block_size))
    sign = base64.b64encode(sign).decode()
    timestamp = int(time.time()*1000)
    data = {
        'reports': 'H4sIAAAAAAAAABXKMQ6AIAwF0Lt0dmghH9DLGGwhaaKDYTTeXdze8B4auxttFGih26/mv1HUJLCmVSsO69xUwBBmlmKSg+TZ6+l1zB4ZEchI9H5JPXJLTwAAAA==',
        'sign': sign,
        'timetamp': timestamp,
    }
    headers['Host'] = 'upush.qidian.com'
    headers['Content-Type'] = 'application/json'
    r = session.post(
        'https://upush.qidian.com/submit/bindingAlias',
        headers=headers,
        json=data,
        verify=False,
    )
    print(r.text)

    return ywkey

def get_activity(task='everyday'):
    timestamp = int(time.time()*1000)
    headers = {
        'Host': 'h5.if.qidian.com',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json, text/plain, */*',
        'helios': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; ANA-AN00 Build/HUAWEIANA-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/109.0.5414.86 MQQBrowser/6.2 TBS/047109 Mobile Safari/537.36 QDJSSDK/1.0  QDNightStyle_1  QDReaderAndroid/7.9.374/1416/1000032/HUAWEI/QDShowNativeLoading',
        'SDKSign': SDK_sign(timestamp),
        'tstamp': str(timestamp),
        'Origin': 'https://h5.if.qidian.com',
        'X-Requested-With': 'com.qidian.QDReader',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://h5.if.qidian.com/h5/adv-develop/entry2?_viewmode=0&jump=zhanghu',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-CN;q=0.8,en-US;q=0.7,en;q=0.6',
    }
    cookies = {
        'lang': 'cn',
        'mode': 'normal',
        'bar': '141',
        'qid': '864651032226271_02:00:00:00:00:00',
        'appId': '12',
        'areaId': '30',
        'ywguid': '332494219',
        'ywkey': 'yw8tytZC86dt',
        'QDInfo': 'U+yF4OhFarDr6lFKb9LpJIwUvq8A3EIcKc6t6TqoksekM7Wg5Rj+Q1gaOSo8OjsyTeu1Gh/V7HG8r3SjyMhyrgEEGhXMuLgqF6xT+h/DKZC9uOp0cDeOqQ793sbo0pC3lxputhqg7plixdmdPjnCeAccyvfArUV//+JwzHva8bIMaXAv/aTiJImDBremLKeAHJpbVdnrM2r4qOSV6EMP7Iu7ZpKVN1cFMDZOYegygfLZ0lxZkwX/x6lZjIgH/Dqk6qXwHZfanY1kqRECHq3A/T9AyJfUaGeHvR4cMbN1e3DJ5JlJsrwStkHre06gdIw4Te2BvwMPAAw=', # TODO
    }
    r = session.get(
        'https://h5.if.qidian.com/argus/api/v1/video/adv/mainPage',
        headers=headers,
        cookies=cookies,
        verify=False,
    )
    main_page = json.loads(r.text)
    if task == 'everyday':
        taskId = main_page['Data']['VideoBenefitModule']['TaskList'][0]['TaskId']
    elif task == 'treasure':
        taskId = main_page['Data']['TreasureBox']['TaskId']
    elif task == 'countdown':
        tasks = main_page['Data']['CountdownBenefitModule']['TaskList']
        for task in tasks:
            if '章节卡' in task['BubbleText'] and task['Total'] == 3:
                taskId = task['TaskId']
                break
        else:
            return
    else:
        return

    data = {
        'taskId': taskId,
        'BanId': '0',
        'BanMessage': '',
        'CaptchaAId': '',
        'CaptchaType': '0',
        'CaptchaURL': '',
        'Challenge': '',
        'Gt': '',
        'NewCaptcha': '0',
        'Offline': '0',
        'PhoneNumber': '',
        'SessionKey': '',
    }
    headers['SDKSign'] = SDK_sign(timestamp, data)
    r = session.post(
        'https://h5.if.qidian.com/argus/api/v1/video/adv/finishWatch',
        headers=headers,
        cookies=cookies,
        data=data,
        verify=False,
    )
    print(r.text, flush=True)

def get_game_play():
    headers = {
        'Host': 'lygame.qidian.com',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; ANA-AN00 Build/HUAWEIANA-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/109.0.5414.86 MQQBrowser/6.2 TBS/047109 Mobile Safari/537.36 QDJSSDK/1.0  QDNightStyle_1  QDReaderAndroid/7.9.374/1416/1000032/HUAWEI/QDShowNativeLoading',
        'X-Requested-With': 'com.qidian.QDReader',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://qdgame.qidian.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-CN;q=0.8,en-US;q=0.7,en;q=0.6',
    }
    cookies = {
        'lang': 'cn',
        'mode': 'normal',
        'bar': '141',
        'qid': '864651032226271_02:00:00:00:00:00',
        'appId': '12',
        'areaId': '30',
        'ywguid': '332494219',
        'ywkey': 'yw8tytZC86dt',
        'QDInfo': 'U+yF4OhFarDr6lFKb9LpJIwUvq8A3EIcKc6t6TqoksekM7Wg5Rj+Q1gaOSo8OjsyTeu1Gh/V7HG8r3SjyMhyrgEEGhXMuLgqF6xT+h/DKZC9uOp0cDeOqQ793sbo0pC3lxputhqg7plixdmdPjnCeAccyvfArUV//+JwzHva8bIMaXAv/aTiJImDBremLKeAHJpbVdnrM2r4qOSV6EMP7Iu7ZpKVN1cFMDZOYegygfLZ0lxZkwX/x6lZjIgH/Dqk6qXwHZfanY1kqRECHq3A/T9AyJfUaGeHvR4cMbN1e3DJ5JlJsrwStkHre06gdIw4Te2BvwMPAAw=', # TODO
    }
    data = {
        'gameId': '201709',
        'platformId': '1',
    }
    r = session.get(
        'https://lygame.qidian.com/home/log/heartbeat',
        headers=headers,
        cookies=cookies,
        data=data,
        verify=False,
    )
    print(r.text, flush=True)

def receive_reward():
    timestamp = int(time.time()*1000)
    headers = {
        'Host': 'h5.if.qidian.com',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json, text/plain, */*',
        'helios': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; ANA-AN00 Build/HUAWEIANA-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/109.0.5414.86 MQQBrowser/6.2 TBS/047109 Mobile Safari/537.36 QDJSSDK/1.0  QDNightStyle_1  QDReaderAndroid/7.9.374/1416/1000032/HUAWEI/QDShowNativeLoading',
        'SDKSign': SDK_sign(timestamp),
        'tstamp': str(timestamp),
        'Origin': 'https://h5.if.qidian.com',
        'X-Requested-With': 'com.qidian.QDReader',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://h5.if.qidian.com/h5/adv-develop/entry2?_viewmode=0&jump=zhanghu',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-CN;q=0.8,en-US;q=0.7,en;q=0.6',
    }
    cookies = {
        'lang': 'cn',
        'mode': 'normal',
        'bar': '141',
        'qid': '864651032226271_02:00:00:00:00:00',
        'appId': '12',
        'areaId': '30',
        'ywguid': '332494219',
        'ywkey': 'yw8tytZC86dt',
        'QDInfo': 'U+yF4OhFarDr6lFKb9LpJIwUvq8A3EIcKc6t6TqoksekM7Wg5Rj+Q1gaOSo8OjsyTeu1Gh/V7HG8r3SjyMhyrgEEGhXMuLgqF6xT+h/DKZC9uOp0cDeOqQ793sbo0pC3lxputhqg7plixdmdPjnCeAccyvfArUV//+JwzHva8bIMaXAv/aTiJImDBremLKeAHJpbVdnrM2r4qOSV6EMP7Iu7ZpKVN1cFMDZOYegygfLZ0lxZkwX/x6lZjIgH/Dqk6qXwHZfanY1kqRECHq3A/T9AyJfUaGeHvR4cMbN1e3DJ5JlJsrwStkHre06gdIw4Te2BvwMPAAw=', # TODO
    }
    r = session.get(
        'https://h5.if.qidian.com/argus/api/v1/video/adv/mainPage',
        headers=headers,
        cookies=cookies,
        verify=False,
    )
    main_page = json.loads(r.text)
    tasks = main_page['Data']['CountdownBenefitModule']['TaskList']
    for task in tasks:
        if '签到互动' in task['BubbleText']:
            taskId = task['TaskId']
            break
    else:
        return
    
    data = {
        'taskId': taskId,
    }
    headers['SDKSign'] = SDK_sign(timestamp, data)
    r = session.post(
        'https://h5.if.qidian.com/argus/api/v1/video/adv/receiveTaskReward',
        headers=headers,
        cookies=cookies,
        data=data,
        verify=False,
    )
    print(r.text, flush=True)

if __name__ == '__main__':
    # ywkey = login('17723605491', 'Xia937910632434!')
    # print(ywkey)
    # exit()
    # get_activity('countdown2')
    while True:
        for i in range(10):
            try:
                get_activity('everyday')
            except:
                pass
            time.sleep(15)
        for i in range(3):
            try:
                get_activity('countdown')
            except:
                pass
            time.sleep(15)
        for i in range(20):
            try:
                get_game_play()
            except:
                pass
            time.sleep(30)
        for i in range(24):
            try:
                get_activity('treasure')
            except:
                time.sleep(30)
                continue
            time.sleep(3610)
    
