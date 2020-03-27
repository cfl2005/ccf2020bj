import requests

import sys
import time
import xlwt
 
word_url = 'http://index.baidu.com/api/SearchApi/thumbnail?area=0&word={}'
COOKIES = 'BIDUPSID=84A5A425F78E7C3DE5BB7305B7B9EC39; PSTM=1542886758; BAIDUID=FB50141361C1DEF3ED1D3B52B9DAEDFD:FG=1; BDUSS=ZjfnVzdExheVBDZ1ozdm1VaG1yYnNXZHYwYmZIRjRvNXhZak9peHVpanVUWU5lRVFBQUFBJCQAAAAAAAAAAAEAAABY2FvRYWNnamtnAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAO7AW17uwFteUU; ZD_ENTRY=baidu; delPer=0; PSINO=1; H_PS_PSSID=30962_1445_21086_30905_31085; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; bdindexid=9pnhui45uvpc2o8p2c43bflmt7; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1584947953,1585025541; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1585034857; RT="sl=0&ss=k85j4rb6&tt=0&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&z=1&dm=baidu.com&si=9kbgg6v3m99"'
 
def decrypt(t,e):
    n = list(t)
    i = list(e)
    a = {}
    result = []
    ln = int(len(n)/2)
    start = n[ln:]
    end = n[:ln]
    for j,k in zip(start, end):
        a.update({k: j})
    for j in e:
        result.append(a.get(j))
    return ''.join(result)
    
    
def get_index_home(keyword):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
        'Cookie': COOKIES
    }
    resp = requests.get(word_url.format(keyword), headers=headers)
    j = resp.json()
    uniqid = j.get('data').get('uniqid')
    return get_ptbk(uniqid)
    
 
def get_ptbk(uniqid):
    url = 'http://index.baidu.com/Interface/ptbk?uniqid={}'
    ptbk_headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Cookie': COOKIES,
        'DNT': '1',
        'Host': 'index.baidu.com',
        'Pragma': 'no-cache',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://index.baidu.com/v2/main/index.html',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    resp = requests.get(url.format(uniqid), headers=ptbk_headers)
    if resp.status_code != 200:
        print('获取uniqid失败')
        sys.exit(1)
    return resp.json().get('data')
    
 
def get_index_data(keyword, start='2019-09-23', end='2020-03-22'):
    url = f'http://index.baidu.com/api/SearchApi/index?word={keyword}&area=0&startDate={start}&endDate={end}'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Cookie': COOKIES,
        'DNT': '1',
        'Host': 'index.baidu.com',
        'Pragma': 'no-cache',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://index.baidu.com/v2/main/index.html',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print('获取指数失败')
        sys.exit(1)
    data = resp.json().get('data').get('userIndexes')[0]
    uniqid = data.get('uniqid')
    ptbk = get_index_home(uniqid)
    while ptbk is None or ptbk == '':
        ptbk = get_index_home(uniqid)
    all_data = data.get('all').get('data')
    result = decrypt(ptbk, all_data)
    result = result.split(',')
    print(result)
    
 
if __name__ == '__main__':
    get_index_data('网购')


    
    
 
   
