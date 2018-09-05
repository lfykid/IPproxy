# encoding:utf-8
import urlparse
from pprint import pprint

from lxml import etree
import requests
import re
import json
import time
from handlers.mysql_handler import MysqlHandler

mysql = MysqlHandler()


# 设置请求头信息
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15'
}
s = requests.session()


def test_ip(proxy):
    try:
        if proxy.startswith('https'):
            proxies = {'https':proxy}
        else:
            proxies = {"http":proxy}
        test_url = "http://www.baidu.com/"
        response = requests.get(test_url, headers=headers, proxies=proxies, timeout=3)
        return response.status_code
    except :
        pass


def to_text(proxy):
    print("########{}写入中##########".format(proxy))
    with open("ip_pool.txt","a") as f:
        f.write(proxy+"\n")
        f.close()


def crawl_66ip():
    all_result = []
    for i in range(1, 15):
        result = []
        url = 'http://www.66ip.cn/{}.html'.format(i)
        print('crawler 66ip', url)
        response = s.get(url, headers=headers)
        html = etree.HTML(response.content.decode('gbk'))
        tr_lists = html.xpath('//div[@class="containerbox boxindex"]/div/table//tr[position()>1]')
        ip_list = []
        if tr_lists:
            for td in tr_lists:
                ip = {}
                ip['source'] = '66ip'
                # IP地址
                ip_server = td.xpath('td[1]/text()')[0]
                port = td.xpath('td[2]/text()')[0]
                ip_url = ":".join([ip_server, port])
                if ip_url in ip_list:
                    ip_server += '__' + str(ip_list.count(ip_url) + 1)
                ip['ip_server'] = ip_server
                ip_list.append(ip_url)
                # IP端口
                ip['ip_port'] = port
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
                result.append(ip)
            all_result.extend(result)

    return all_result
                # proxy = "http://" + ip['ip_server'] + ":" + ip['ip_port']
                # status = test_ip(proxy)
                # if status == 200:
                #     to_text(proxy)
                # else:
                #     print("#############链接失败：{}不可用##############".format(proxy))


def crawl_xici():
    all_result = []
    for i in range(1, 6):
        result = []
        url = 'http://www.xicidaili.com/nn/{}'.format(i)
        print('crawler xici', url)
        ip_list = []
        response = s.get(url, headers=headers)
        html = etree.HTML(response.content.decode('utf-8'))
        if html.xpath('//table[@id="ip_list"]'):
            for td in html.xpath('//table[@id="ip_list"]//tr[position()>1]'):
                ip = {}
                ip['source'] = 'xici'
                # IP地址
                ip_server = td.xpath('td[2]/text()')[0]
                port = td.xpath('td[3]/text()')[0]
                type = td.xpath('td[6]/text()')[0]
                ip_url = ":".join([ip_server, port, type])
                if ip_url in ip_list:
                    ip_server += '__' + str(ip_list.count(ip_url) + 1)
                ip['ip_server'] = ip_server
                ip_list.append(ip_url)
                # IP端口
                ip['ip_port'] = port
                # 服务器地址
                ip_address = td.xpath('td[4]/a/text()')
                if ip_address:
                    ip['ip_address'] = ip_address[0]
                else:
                    ip['ip_address'] = 'no info'
                # 是否高匿
                ip['ip_clear'] = td.xpath('td[5]/text()')[0]
                # 类型
                ip['ip_type'] = type
                ip['stay_time'] = td.xpath('td[9]/text()')[0]
                ip['created'] = int(time.time())
                result.append(ip)
            all_result.extend(result)
    return all_result


def crawl_iphai():
    all_result = []
    urls = ['http://www.iphai.com/free/ng',
            'http://www.iphai.com/free/wg']
    for url in urls:
        result = []
        print('crawler iphai', url)
        ip_list = []
        response = s.get(url, headers=headers)
        html = etree.HTML(response.content)
        tr_lists = html.xpath('//table//tr[position()>1]')
        if tr_lists:
            for td in tr_lists:
                ip = {}
                ip['source'] = 'iphai'
                # IP地址
                ip_server = td.xpath('td[1]/text()')[0].strip()
                port = td.xpath('td[2]/text()')[0].strip()
                ip_url = ":".join([ip_server, port])
                if ip_url in ip_list:
                    ip_server += '__' + str(ip_list.count(ip_url) + 1)
                ip['ip_server'] = ip_server
                ip_list.append(ip_url)
                # IP端口
                ip['ip_port'] = port
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
                # if ip['ip_type'] != 'no info' and u',' not in ip['ip_type']:
                #     proxy = ip['ip_type'].lower() + '://' + ip['ip_server'] + ':' + ip['ip_port']
                # else:
                #     proxy = "http://" + ip['ip_server'] + ":" + ip['ip_port']
                # status = test_ip(proxy)
                # if status == 200:
                #     to_text(json.dumps(ip))
                # else:
                #     print("#############链接失败：{}不可用##############".format(proxy))

                result.append(ip)
            all_result.extend(result)
    return all_result


def crawl_kuaidaili():
    all_result = []
    for i in range(2, 6):
        result = []
        url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
        print('crawel kuaidaili', url)
        ip_list = []
        response = s.get(url, headers=headers)
        html = etree.HTML(response.content.decode('utf-8'))
        for tr in html.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr'):
            ip = {}
            ip['source'] = 'kuaidaili'
            # IP地址
            ip_server = tr.xpath('td[1]/text()')[0]
            port = tr.xpath('td[2]/text()')[0]
            ip_url = ":".join([ip_server, port])
            if ip_url in ip_list:
                ip_server += '__' + str(ip_list.count(ip_url) + 1)
            ip['ip_server'] = ip_server
            ip_list.append(ip_url)
            # IP端口
            ip['ip_port'] = port
            # 服务器地址
            ip['ip_address'] = tr.xpath('td[5]/text()')[0]
            # 高匿
            ip['ip_clear']= tr.xpath('td[3]/text()')[0]
            # 类型
            ip['ip_type'] = tr.xpath('td[4]/text()')[0]
            ip['created'] = int(time.time())
            result.append(ip)
        all_result.extend(result)

    return all_result


def crawl_yunip():
    all_result = []
    urls = ['http://www.ip3366.net/free/?stype=1',
            'http://www.ip3366.net/free/?stype=3'
            ]
    for url in urls:
        results = []
        for i in range(1, 6):
            result = []
            r_url = url + '&page={}'.format(i)
            print('crawel yunip', r_url)
            ip_list = []
            response = s.get(r_url, headers=headers)
            html = etree.HTML(response.content.decode('gbk'))
            tr_list = html.xpath('//table/tbody/tr')
            for tr in tr_list:
                ip = {}
                ip['source'] = 'ip3366'
                # IP地址
                ip_server = tr.xpath('td[1]/text()')[0]
                port = tr.xpath('td[2]/text()')[0]
                ip_url = ":".join([ip_server, port])
                if ip_url in ip_list:
                    ip_server += '__' + str(ip_list.count(ip_url) + 1)
                ip['ip_server'] = ip_server
                ip_list.append(ip_url)
                # IP端口
                ip['ip_port'] = port
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
                result.append(ip)
            results.extend(result)
        all_result.extend(results)
    return all_result


def crawl_jiangxianli():
    all_result = []
    for i in range(1, 11):
        result = []
        url = 'http://ip.jiangxianli.com/?page={}'.format(i)
        print('crawler jiangxianli', url)
        ip_list = []
        response = s.get(url, headers=headers)
        html = etree.HTML(response.content.decode('utf-8'))
        tr_lists = html.xpath('//table/tbody/tr')
        if tr_lists:
            for td in tr_lists:
                ip = {}
                ip['source'] = 'jiangxianli'
                # IP地址
                ip_server = td.xpath('td[2]/text()')[0]
                port = td.xpath('td[3]/text()')[0]
                ip_url = ":".join([ip_server, port])
                if ip_url in ip_list:
                    ip_server += '__' + str(ip_list.count(ip_url) + 1)
                ip['ip_server'] = ip_server
                ip_list.append(ip_url)
                # IP端口
                ip['ip_port'] = port
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
                result.append(ip)
            all_result.extend(result)

    return all_result

# data5u  测试有问题
def crawl_data5u():
    ip = {}
    urls = ['http://www.data5u.com/free/gngn/index.shtml',
            'http://www.data5u.com/free/gwgn/index.shtml'
            ]
    for url in urls:
        for i in range(1, 6):
            url = urlparse.urljoin(url, 'index{}.shtml'.format(i))
            print('crawel data5u', url)
            response = s.get(url, headers=headers)
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


def crawl_mimidaili():
    all_result = []
    urls = ['http://www.mimiip.com/gngao/',
            'http://www.mimiip.com/hw/'
            ]
    for url in urls:
        results = []
        for i in range(1, 6):
            result = []
            url = urlparse.urljoin(url, '{}'.format(i))
            print('crawel mimidaili', url)
            ip_list = []
            response = s.get(url, headers=headers)
            html = etree.HTML(response.content.decode('utf-8'))
            tr_list = html.xpath('//table[@class="list"]//tr[position()>1]')
            for tr in tr_list:
                ip = {}
                ip['source'] = 'mimidaili'
                # IP地址
                ip_server = tr.xpath('td[1]/text()')[0]
                port = tr.xpath('td[2]/text()')[0]
                ip_url = ":".join([ip_server, port])
                if ip_url in ip_list:
                    ip_server += '__' + str(ip_list.count(ip_url) + 1)
                ip['ip_server'] = ip_server
                ip_list.append(ip_url)
                # IP端口
                ip['ip_port'] = port.strip()
                # 服务器地址
                ip_address = tr.xpath('td[3]//text()')
                if ip_address:
                    ip['ip_address'] = "".join(ip_address).strip('\r\n')
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
                result.append(ip)
            results.extend(result)
        all_result.extend(results)
    return all_result


def crawl_xiaohexia():
    all_result = []
    for i in range(1, 8):
        result = []
        url = 'http://www.xiaohexia.cn/index.php?page={}'.format(i)
        print('crawler xiaohexia', url)
        ip_list = []
        response = s.get(url, headers=headers)
        html = etree.HTML(response.content.decode('utf-8'))
        tr_lists = html.xpath('//table//tr[position()>1]')
        if tr_lists:
            for td in tr_lists:
                ip = {}
                ip['source'] = 'xiaohexia'
                # IP地址
                ip_server = td.xpath('td[1]/text()')[0]
                port = td.xpath('td[2]/text()')[0]
                ip_url = ":".join([ip_server, port])
                if ip_url in ip_list:
                    ip_server += '__' + str(ip_list.count(ip_url) + 1)
                ip['ip_server'] = ip_server
                ip_list.append(ip_url)
                # IP端口
                ip['ip_port'] = port
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
                result.append(ip)
            all_result.extend(result)
    return all_result


def crawl_swei360():
    all_result = []
    urls = ['http://www.swei360.com/free/?stype=1',
            'http://www.swei360.com/free/?stype=3'
            ]
    for url in urls:
        results = []
        for i in range(1, 6):
            result = []
            r_url = url + '&page={}'.format(i)
            print('crawel swei360', r_url)
            ip_list = []
            response = s.get(r_url, headers=headers)
            html = etree.HTML(response.content.decode('gbk'))
            tr_list = html.xpath('//table/tbody/tr')
            for tr in tr_list:
                ip = {}
                ip['source'] = '360daili'
                # IP地址
                ip_server = tr.xpath('td[1]/text()')[0]
                port = tr.xpath('td[2]/text()')[0]
                ip_url = ":".join([ip_server, port])
                if ip_url in ip_list:
                    ip_server += '__' + str(ip_list.count(ip_url) + 1)
                ip['ip_server'] = ip_server
                ip_list.append(ip_url)
                # IP端口
                ip['ip_port'] = port
                # 服务器地址
                ip['ip_address'] = tr.xpath('td[5]/text()')[0]
                # 高匿
                ip['ip_clear'] = tr.xpath('td[3]/text()')[0]
                # 类型
                ip['ip_type'] = tr.xpath('td[4]/text()')[0]
                result.append(ip)
            results.extend(result)
        all_result.extend(results)
    return all_result


def store():
    post = crawl_swei360()
    for ip in post:
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


if __name__ == '__main__':

    # get_66ip()
    store()
    # for ip in crawl_mimidaili():
    #     print(ip)