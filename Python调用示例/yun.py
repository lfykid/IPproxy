# coding:utf-8
import json
import time
import requests

# 用户名
username = ''
# 登录密码
password = ''
# 文件名支持jpg,png
file_name = 'getimage.jpg'
# 打码类型
code_type = 1004
# id
app_id=1
# 密钥
app_key='22cc5376925e9387a23cf797cb9ba745'
# 超时
time_out=60

apiurl = 'http://api.yundama.com/api.php'


class YDMHttp:
    def __init__(self, name, passwd, app_id, app_key):
        self.username = name
        self.password = passwd
        self.appid = str(app_id)
        self.appkey = app_key

    def request(self, fields, files=[]):
        response = self.post_url(apiurl, fields, files)
        response = json.loads(response)
        return response

    def balance(self):
        data = {
            'method': 'balance',
            'username': self.username,
            'password': self.password,
            'appid': self.appid,
            'appkey': self.appkey
        }
        response = self.request(data)
        if response:
            if response['ret'] and response['ret'] < 0:
                return response['ret']
            else:
                return response['balance']
        else:
            return -9001

    def login(self):
        data = {'method': 'login', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey}
        response = self.request(data)
        if response:
            if response['ret'] and response['ret'] < 0:
                return response['ret']
            else:
                return response['uid']
        else:
            return -9001

    def upload(self, filename, codetype, timeout):
        data = {'method': 'upload', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey, 'codetype': str(codetype), 'timeout': str(timeout)}
        file = {'file': filename}
        response = self.request(data, file)
        if response:
            if response['ret'] and response['ret'] < 0:
                return response['ret']
            else:
                return response['cid']
        else:
            return -9001

    def result(self, cid):
        data = {'method': 'result', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey, 'cid': str(cid)}
        response = self.request(data)
        return response and response['text'] or ''

    def decode(self, file_name, code_type, time_out):
        cid = self.upload(file_name, code_type, time_out)
        if cid > 0:
            for i in range(0, time_out):
                result = self.result(cid)
                if result != '':
                    return cid, result
                else:
                    time.sleep(1)
            return -3003, ''
        else:
            return cid, ''

    def post_url(self, url, fields, files=[]):
        for key in files:
            files[key] = open(files[key], 'rb')
        res = requests.post(url, files=files, data=fields)
        return res.text

    def report_error(self, cid):
        data = {
            'method': 'report',
            'username': self.username,
            'password': self.password,
            'appid': self.appid,
            'appkey': self.appkey,
            'flag': 0,
            'cid': cid
        }

        response = self.request(data)
        if response:
            if response['ret']:
                return response['ret']
        else:
            return -9001


def code_verificate():

    yundama_obj = YDMHttp(username, password, app_id, app_key)
    yundama_obj.login()

    rest = yundama_obj.balance()
    if rest <= 0:
        raise Exception('云打码已经欠费了，请及时充值')
    if rest <= 100:
        print('云打码余额已不多，请注意及时充值')

    # 开始识别，图片路径，验证码类型ID，超时时间（秒），识别结果
    cid, result = yundama_obj.decode(file_name, code_type, time_out)
    return result, yundama_obj, cid


if __name__ == '__main__':

    rs = code_verificate()
    print(rs)
