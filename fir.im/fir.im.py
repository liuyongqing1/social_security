# -*- coding:utf-8 -*-
'''
此程序用作检查fir.im剩余的付费次数用。
'''
import requests,json,re,time
from pyquery import PyQuery as pq
import sys,getopt

def first():
    try:
        Fir=r.get('http://account.fir.im/signin',headers={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
        })
        doc=pq(Fir.text)
        token=doc.find('meta[name="csrf-token"]').attr('content')
        return token
    except Exception as f:
        print(f)
        exit(2)

def secound(token,username,password):
    try:
        data={
            'utf8':'',
            'authenticity_token':token,
            'user[email]':username,
            'user[password]':password,
            'user[remember_me]':'0',
            'user[remember_me]':1
        }
        Login=r.post('http://account.fir.im/signin',data=data,headers=r.headers)
        three()
    except:
        print('应该是请求超时了')
        exit(2)
def three():
    try:
        API=r.get('https://account.fir.im/oauth/authorize?response_type=code&redirect_uri=http%3A%2F%2Ffir.im%2Foauth%2Fcallback&client_id=c29dd25a3727c8d5',headers={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
        },allow_redirects=False)
        doc=pq(API.text)
        CODE_URL=doc('a').attr('href')
        four(CODE_URL)
    except:
        print('应该是请求超时了')
        exit(2)
def four(CODE_URL):
    try:
        REQ_accesstoken=r.get(CODE_URL,headers={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
        },allow_redirects=False)
        _code=CODE_URL.split('?')[1]
        FULL_URL='https://api.fir.im/login?{0}&redirect_uri=http%3A%2F%2Ffir.im%2Foauth%2Fcallback'.format(_code)
        token=r.post(FULL_URL)
        access_token=json.loads(token.text)['access_token']
        userinfo(access_token)
        # print(requests.utils.cookiejar_from_dict(r.cookies))
    except:
        print('应该是请求超时了')
        exit(2)
#获取用户信息
def userinfo(access_token):
    try:
        user_URL='https://api.fir.im/user?access_token={0}'.format(access_token)
        user_info=r.get(user_URL)
        # print(json.loads(user_info.text))
        id=json.loads(user_info.text)['orgs'][0]['user']['default_org_id']
        reqcount(id,access_token)
    except:
        print('应该是请求超时了')
        exit(2)
#请求剩余数量数据
def reqcount(id,access_token):
    try:
        count_url='https://api.fir.im/orgs/{0}/surplus?d={1}'.format(id,int(round(time.time() * 1000)))
        # print(count_url)
        he={
            'access-control-request-method': 'GET',
            'origin': 'https://fir.im',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
            'access-control-request-headers': 'accesstoken',
            'accept': '*/*',
            'referer': 'https://fir.im/apps',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4'
        }
        req_option=r.options(count_url,headers=he)
        h={
            'accept':'application/json, text/plain, */*',
            'origin':'https://fir.im',
            'accesstoken':access_token,
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
            'referer':'https://fir.im/apps',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4',
        }
        req_count=r.get(count_url,headers=h)
        obj_cout=json.loads(req_count.text)
        result='免费次数剩余{0},付费次数为{1}'.format(obj_cout['packet_surplus'] , obj_cout['flow_surplus'])
        print(result)
    except:
        print('应该是请求超时了')
        exit(2)
if __name__ == '__main__':

    usage='Usage  本程序用于查询fir.im的免费及付费次数 \n       -u --user       登陆用户名(必选) \n       -p --password 登陆密码(必选) \n       -h --help     查看帮助信息'
    config={
    'user':'',
    'password':'',
    }
    try:
        options, args = getopt.getopt(sys.argv[1:], "hu:p:", ["help", "user=", "password="])
        for name, value in options:
            if name in ("-h", "--help"):
                print(usage)
                sys.exit()
            elif name in ("-u", "--user"):
                config['user'] = value
            elif name in ("-p", "--password"):
                config['password'] = value
        for key,value in config.items():
            if value == '':
               sys.exit()
    except:
        print(usage)
        sys.exit()

    r = requests.session()
    first()
    secound(first(),config['user'],config['password'])