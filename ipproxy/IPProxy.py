# encoding:utf-8
import urlparse

from lxml import etree
import requests
import re
import json
import time
from handlers.mysql_handler import MysqlHandler


# 设置请求头信息
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.'
                  '84 Safari/537.36'
}
s = requests.session()


# 西刺代理
def crawl_xici():
    ip = {}
    for i in range(1, 11):
        url = 'http://www.xicidaili.com/nn/{}'.format(i)
        print('crawler xici', url)
        response = s.get(url, headers=headers)
        html = etree.HTML(response.content.decode('utf-8'))
        if html.xpath('//table[@id="ip_list"]'):
            for td in html.xpath('//table[@id="ip_list"]//tr[position()>1]'):
                ip['source'] = 'xici'
                # IP地址
                ip['ip_server'] = td.xpath('td[2]/text()')[0]
                # IP端口
                ip['ip_port'] = td.xpath('td[3]/text()')[0]
                # 服务器地址
                ip_address = td.xpath('td[4]/a/text()')
                if ip_address:
                    ip['ip_address'] = ip_address[0]
                else:
                    ip['ip_address'] = 'no info'
                # 高匿
                ip['ip_clear'] = td.xpath('td[5]/text()')[0]
                # 类型
                ip['ip_type'] = td.xpath('td[6]/text()')[0]
                ip['stay_time'] = td.xpath('td[9]/text()')[0]
                ip['created'] = int(time.time())
                yield ip


# 快代理
def crawl_kuaidaili():
    ip = {}
    for i in range(1, 11):
        url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
        print('crawel kuaidaili', url)
        response = s.get(url, headers=headers)
        html = etree.HTML(response.content.decode('utf-8'))
        for tr in html.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr'):
            ip['source'] = 'kuaidaili'
            # IP地址
            ip['ip_server'] = tr.xpath('td[1]/text()')[0]
            # IP端口
            ip['ip_port'] = tr.xpath('td[2]/text()')[0]
            # 服务器地址
            ip_address = tr.xpath('td[5]/text()')
            if ip_address:
                ip['ip_address'] = ip_address[0]
            # 高匿
            ip['ip_clear'] = tr.xpath('td[3]/text()')[0]
            # 类型
            ip['ip_type'] = tr.xpath('td[4]/text()')[0]
            ip['created'] = int(time.time())
            yield ip


# 云ip
def crawl_yunip():
    ip = {}
    urls = ['http://www.ip3366.net/free/?stype=1',
            'http://www.ip3366.net/free/?stype=3'
            ]
    for url in urls:
        for i in range(1, 11):
            r_url = url + '&page={}'.format(i)
            print('crawel yunip', r_url)
            response = s.get(r_url, headers=headers)
            html = etree.HTML(response.content.decode('gbk'))
            tr_list = html.xpath('//table/tbody/tr')
            for tr in tr_list:
                ip['source'] = 'ip3366'
                # IP地址
                ip['ip_server'] = tr.xpath('td[1]/text()')[0]
                # IP端口
                ip['ip_port'] = tr.xpath('td[2]/text()')[0]
                # 服务器地址
                ip_address = tr.xpath('td[5]/text()')
                if ip_address:
                    ip['ip_address'] = ip_address[0]
                else:
                    ip['ip_address'] = 'no info'
                # 高匿
                ip['ip_clear'] = tr.xpath('td[3]/text()')[0]
                # 类型
                ip['ip_type'] = tr.xpath('td[4]/text()')[0]
                ip['created'] = int(time.time())
                yield ip


# 66ip
def crawl_66ip():
    ip = {}
    for i in range(1, 6):
        url = 'http://www.66ip.cn/{}.html'.format(i)
        print('crawler 66ip', url)
        response = s.get(url, headers=headers)
        html = etree.HTML(response.content.decode('gbk'))
        tr_lists = html.xpath('//div[@class="containerbox boxindex"]/div/table//tr[position()>1]')
        if tr_lists:
            for td in tr_lists:
                ip['source'] = '66ip'
                # IP地址
                ip['ip_server'] = td.xpath('td[1]/text()')[0]
                # IP端口
                ip['ip_port'] = td.xpath('td[2]/text()')[0]
                # 服务器地址
                ip_address = td.xpath('td[3]/text()')
                if ip_address:
                    ip['ip_address'] = ip_address[0]
                else:
                    ip['ip_address'] = 'no info'
                # 是否高匿
                ip_clear = td.xpath('td[4]/text()')[0]
                if u'高' not in ip_clear:
                    continue
                else:
                    ip['ip_clear'] = ip_clear
                # 类型
                ip['ip_type'] = 'no info'
                ip['created'] = int(time.time())
                yield ip


# ip海
def crawl_iphai():
    ip = {}
    urls = ['http://www.iphai.com/free/ng',
            'http://www.iphai.com/free/wg']
    for url in urls:
        print('crawler iphai', url)
        response = s.get(url, headers=headers)
        html = etree.HTML(response.content)
        tr_lists = html.xpath('//table//tr[position()>1]')
        if tr_lists:
            for td in tr_lists:
                ip['source'] = 'iphai'
                # IP地址
                ip['ip_server'] = td.xpath('td[1]/text()')[0].strip()
                # IP端口
                ip['ip_port'] = td.xpath('td[2]/text()')[0].strip()
                # 服务器地址
                ip_address = td.xpath('td[5]/text()')
                if ip_address:
                    ip['ip_address'] = ip_address[0].strip()
                else:
                    ip['ip_address'] = 'no info'
                # 高匿
                ip['ip_clear'] = td.xpath('td[3]/text()')[0].strip()
                # 类型
                ip_type = td.xpath('td[4]//text()')
                if len(ip_type[0].strip()):
                    ip['ip_type'] = ip_type[0].strip()
                else:
                    ip['ip_type'] = 'no info'
                ip['created'] = int(time.time())
                yield ip

# jiangxianli
def crawl_jiangxianli():
    ip = {}
    for i in range(1, 11):
        url = 'http://ip.jiangxianli.com/?page={}'.format(i)
        print('crawler jiangxianli', url)
        response = s.get(url, headers=headers)
        html = etree.HTML(response.content.decode('utf-8'))
        tr_lists = html.xpath('//table/tbody/tr')
        if tr_lists:
            for td in tr_lists:
                ip['source'] = 'jiangxianli'
                # IP地址
                ip['ip_server'] = td.xpath('td[2]/text()')[0]
                # IP端口
                ip['ip_port'] = td.xpath('td[3]/text()')[0]
                # 服务器地址
                ip_address = td.xpath('td[6]/text()')
                if ip_address:
                    ip['ip_address'] = ip_address[0]
                else:
                    ip['ip_address'] = 'no info'
                # 是否高匿
                ip_clear = td.xpath('td[4]/text()')[0]
                if u'高' not in ip_clear:
                    continue
                else:
                    ip['ip_clear'] = ip_clear
                # 类型
                ip['ip_type'] = td.xpath('td[5]/text()')[0]
                ip['created'] = int(time.time())
                yield ip


# 无忧  没有能用的
def crawl_data5u():
    ip = {}
    urls = ['http://www.data5u.com/free/gngn/index.shtml',
            'http://www.data5u.com/free/gwgn/index.shtml'
            ]
    for url in urls:
        for i in range(1, 6):
            r_url = urlparse.urljoin(url, 'index{}.shtml'.format(i))
            print('crawel data5u', r_url)
            response = s.get(r_url, headers=headers)
            html = etree.HTML(response.content.decode('utf-8'))
            tr_list = html.xpath('//ul[@class="l2"]')
            for tr in tr_list:
                ip['source'] = 'data5u'
                # IP地址
                ip['ip_server'] = tr.xpath('span[1]/li/text()')[0]
                # IP端口
                ip['ip_port'] = tr.xpath('span[2]/li/text()')[0]
                # 服务器地址
                ip_address = tr.xpath('span[5]/li//text()')
                if ip_address:
                    ip['ip_address'] = "".join(ip_address)
                else:
                    ip['ip_address'] = 'no info'
                # 高匿
                ip_clear = "".join(tr.xpath('span[3]/li//text()'))
                if u'高' not in ip_clear:
                    continue
                else:
                    ip['ip_clear'] = ip_clear
                # 类型
                ip['ip_type'] = "".join(tr.xpath('span[4]/li//text()'))
                yield ip


# 秘密代理
def crawl_mimidaili():
    ip = {}
    urls = ['http://www.mimiip.com/gngao/',
            'http://www.mimiip.com/hw/'
            ]
    for url in urls:
        for i in range(1, 11):
            r_url = urlparse.urljoin(url, '{}'.format(i))
            print('crawel mimidaili', r_url)
            response = s.get(r_url, headers=headers)
            html = etree.HTML(response.content.decode('utf-8'))
            tr_list = html.xpath('//table[@class="list"]//tr[position()>1]')
            for tr in tr_list:
                ip['source'] = 'mimidaili'
                # IP地址
                ip['ip_server'] = tr.xpath('td[1]/text()')[0]
                # IP端口
                ip['ip_port'] = tr.xpath('td[2]/text()')[0].strip()
                # 服务器地址
                ip_address = tr.xpath('td[3]//text()')
                if ip_address:
                    ip['ip_address'] = "".join(ip_address).strip()
                else:
                    ip['ip_address'] = 'no info'
                # 高匿
                ip_clear = tr.xpath('td[4]/text()')[0]
                if u'高' not in ip_clear:
                    continue
                else:
                    ip['ip_clear'] = ip_clear
                # 类型
                ip['ip_type'] = tr.xpath('td[5]/text()')[0]
                ip['created'] = int(time.time())
                yield ip


# 小河虾
def crawl_xiaohexia():
    ip = {}
    for i in range(1, 11):
        url = 'http://www.xiaohexia.cn/index.php?page={}'.format(i)
        print('crawler xiaohexia', url)
        response = s.get(url, headers=headers)
        html = etree.HTML(response.content.decode('utf-8'))
        tr_lists = html.xpath('//table//tr[position()>1]')
        if tr_lists:
            for td in tr_lists:
                ip['source'] = 'xiaohexia'
                # IP地址
                ip['ip_server'] = td.xpath('td[1]/text()')[0]
                # IP端口
                ip['ip_port'] = td.xpath('td[2]/text()')[0]
                # 服务器地址
                ip_address = td.xpath('td[6]/text()')
                if ip_address:
                    ip['ip_address'] = ip_address[0]
                else:
                    ip['ip_address'] = 'no info'
                # 是否高匿
                ip_clear = td.xpath('td[3]/text()')[0]
                if u'高' not in ip_clear:
                    continue
                else:
                    ip['ip_clear'] = ip_clear
                # 类型
                ip['ip_type'] = td.xpath('td[4]/text()')[0]
                ip['created'] = int(time.time())
                yield ip


#蚂蚁代理  不可用
def crawl_mayidaili():
    ip = {}
    for i in range(1, 6):
        url = 'http://www.mayidaili.com/free/anonymous/高匿/{}'.format(i)
        print('crawler mayidaili', url)
        response = s.get(url, headers=headers)
        html = etree.HTML(response.content.decode('utf-8'))
        tr_lists = html.xpath('//table/tbody/tr')
        if tr_lists:
            for td in tr_lists:
                ip['source'] = 'mayidaili'
                # IP地址
                ip['ip_server'] = td.xpath('td[1]/text()')[0].strip()
                # IP端口
                ip['ip_port'] = td.xpath('td[2]/img/@data-uri')[0].strip()
                # 服务器地址
                ip['ip_address'] = td.xpath('td[4]/a/text()')[0].strip()
                # 是否高匿
                ip_clear = td.xpath('td[3]/a/text()')[0].strip()
                if u'高' not in ip_clear:
                    continue
                else:
                    ip['ip_clear'] = ip_clear
                # 类型
                ip['ip_type'] = 'no info'
                ip['created'] = int(time.time())
                yield ip


#优优代理 不可用
def crawl_yoyodl():
    ip = {}
    url = 'http://www.yoyodl.com'
    print('crawel yoyodl', url)
    response = s.get(url, headers=headers)
    html = etree.HTML(response.content.decode('utf-8'))
    tr_list = html.xpath('//ul[@class="l2"]')
    for tr in tr_list:
        ip['source'] = 'yoyodl'
        # IP地址
        ip['ip_server'] = tr.xpath('span[1]/li/text()')[0]
        # IP端口
        ip['ip_port'] = tr.xpath('span[2]/li/text()')[0]
        # 服务器地址
        ip_address = tr.xpath('span[5]/li//text()')
        if ip_address:
            ip['ip_address'] = "".join(ip_address)
        else:
            ip['ip_address'] = 'no info'
        # 高匿
        ip_clear = "".join(tr.xpath('span[3]/li//text()'))
        if u'高' not in ip_clear:
            continue
        else:
            ip['ip_clear'] = ip_clear
        # 类型
        ip['ip_type'] = "".join(tr.xpath('span[4]/li//text()'))
        yield ip


# 31代理 少数能用
def crawl_31f():
    ip = {}
    url = 'http://31f.cn/high-proxy/'
    print('crawel 31dl', url)
    response = s.get(url, headers=headers)
    html = etree.HTML(response.content.decode('utf-8'))
    tr_list = html.xpath('//div[@class="container"]/table[1]//tr[position()>1]')
    for tr in tr_list:
        ip['source'] = '31daili'
        # IP地址
        ip['ip_server'] = tr.xpath('td[2]/text()')[0]
        # IP端口
        ip['ip_port'] = tr.xpath('td[3]/text()')[0]
        # 服务器地址
        ip_address = tr.xpath('td[4]//text()')
        if ip_address:
            ip['ip_address'] = "".join(ip_address)
        else:
            ip['ip_address'] = 'no info'
        # 高匿
        ip['ip_clear'] = "高匿"
        # 类型
        ip['ip_type'] = 'no info'
        ip['created'] = int(time.time())
        yield ip

#360代理
def crawl_swei360():
    ip = {}
    urls = ['http://www.swei360.com/free/?stype=1',
            'http://www.swei360.com/free/?stype=3'
            ]
    for url in urls:
        for i in range(1, 6):
            r_url = url + '&page={}'.format(i)
            print('crawel swei360', r_url)
            response = s.get(r_url, headers=headers)
            html = etree.HTML(response.content.decode('gbk'))
            tr_list = html.xpath('//table/tbody/tr')
            for tr in tr_list:
                ip['source'] = '360daili'
                # IP地址
                ip['ip_server'] = tr.xpath('td[1]/text()')[0]
                # IP端口
                ip['ip_port'] = tr.xpath('td[2]/text()')[0]
                # 服务器地址
                ip['ip_address'] = tr.xpath('td[5]/text()')[0]
                # 高匿
                ip['ip_clear'] = tr.xpath('td[3]/text()')[0]
                # 类型
                ip['ip_type'] = tr.xpath('td[4]/text()')[0]
                ip['created'] = int(time.time())
                yield ip


# 格式化
def ipinit(ip):
    proxies = {}
    if ip['ip_type'] != 'no info' and u',' not in ip['ip_type']:
        proxies[ip['ip_type']] = ip['ip_type'].lower() + '://' + ip['ip_server'] + ':' + ip['ip_port']
    else:
        proxies['http'] = "http://" + ip['ip_server'] + ":" + ip['ip_port']
    return proxies


def to_text(proxy):
    print("########{}写入中##########".format(proxy))
    with open("ip_pool.txt","a") as f:
        f.write(proxy+"\n")
        f.close()


# 生成格式化的ip
def create_ip():
    print('create ip resource')
    for ip in crawl_swei360():
        try:
            proxies = ipinit(ip)
            start = time.time()
            response = requests.get('http://www.baidu.com/', proxies=proxies, headers=headers, timeout=5)
            req_time = time.time() - start
            ip['req_time'] = round(req_time,2)
            if response.status_code == 200:
                mysql = MysqlHandler()
                is_existed = mysql.query(ip, "IPproxy", ['ip_server', 'ip_port', 'ip_type'])
                if len(is_existed):
                    if is_existed[0].source != ip['source']:
                        ip['ip_server'] += 'r_' + is_existed[0].source
                    else:
                        continue

                feed_back = mysql.store_one(ip, 'IPproxy', ['id'])
                id = int(feed_back.get("id", 0)) if feed_back else 0
                if id == 0:
                    return None
        except Exception:

            print('ip 代理不可用')
            continue


if __name__ == '__main__':
    # for ip in create_ip():
    #     print(ip)
    # pass
    create_ip()
    # for ip in crawl_swei360():
    #     print(ip)
