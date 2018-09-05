# coding:utf-8
import time
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.'
                  '84 Safari/537.36'
}
s = requests.session()
try:
    proxies = {'http':'http://58.212.43.10:44686'}
    start = time.time()
    response = requests.get('http://www.baidu.com/', proxies=proxies, headers=headers, timeout=5)
    req_time = time.time() - start

    if response.status_code == 200:
        print('true')
    else:
        print(response.status_code)
except Exception:
    print('ip 代理不可用')
# while True:
#     # proxies = {'http':'http://123.57.52.171:80'}
#     url = 'http://www.mimiip.com'
#     response = s.get(url=url, headers=headers, timeout=5)
#     if response.status_code == 200:
#         print('true')
#     else:
#         print(response)
#         break
#     time.sleep(1)

