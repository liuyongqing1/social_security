#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import requests,time
from pyquery import PyQuery as pq
import pytesseract
from PIL import Image
import getopt,sys,time


def Login(user,password):
    header={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
    }
    r.get('http://www.bjrbj.gov.cn/csibiz/indinfo/login.jsp',headers=header)
    login_url='http://www.bjrbj.gov.cn/csibiz/indinfo/login_check'
    code_pic=r.get('http://www.bjrbj.gov.cn//csibiz/indinfo/validationCodeServlet.do')
    with open('pic.jpg','wb') as f:
        f.write(code_pic.content)
        f.close()
    imag=Image.open('pic.jpg')
    code = pytesseract.image_to_string(imag)
    log_data={
    'type':1,
    'flag':3,
    'j_username':user,
    'j_password':password,
    'safecode':code,
    'x':'40',
    'y':'20'
    }
    req_login_status=r.post(login_url,data=log_data,headers=header).text


def req_jsb(header,dic,year):
    for key,value in dic.items():
        url='http://www.bjrbj.gov.cn/csibiz/indinfo/search/ind/indPaySearchAction!{2}?searchYear={0}&time={1}'.format(year,int(round(time.time() * 1000)),key)
        req_status=r.get(url,headers=header)
        doc=pq(req_status.text)
        td=doc('td')
        obj_list=(td.text().split())
        for i in list(range(5)):
            obj_list.pop(0)
        _format='============================================{0}================================'.format(value)
        print(_format)
        if key == 'injuries' or key == 'maternity':
            cl(obj_list,3)
        elif key == 'unemployment':
            cl(obj_list,4)
        else:
            cl(obj_list,6)



def cl(obj_list,count):
    obj_list.insert(0,'asdfasdf')
    b=[]
    for i in range(len(obj_list)):
        if i == 0:
            pass
        elif int(i)%count == 0:
            b.append(obj_list[i])
            print('    '.join(b))
            b=[]
        else:
            b.append(obj_list[i])

def main():
    config={
    'user':'',
    'password':'',
    'year':''
    }
    now = time.strftime('%Y',time.localtime(time.time()))
    header={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
    }

    usage='Usage  本程序用于查看本人社保信息 \n       -i --id       个人身份证信息(必选) \n       -p --password 登陆密码(必选) \n       -y --year     查看社保年份 (可选,默认为今年) \n       -h --help     查看>帮助信息'

    dic={
        'unemployment':'失业',
        'injuries':'工伤',
        'maternity': '生育',
        'medicalcare' :'医疗',
        'oldage': '养老'
    }

    try:
        options, args = getopt.getopt(sys.argv[1:], "hi:p:y:", ["help", "id=", "password=", "year="])
        for name, value in options:
            if name in ("-h", "--help"):
                print(usage)
                sys.exit()
            elif name in ("-i", "--id"):
                config['user'] = value
            elif name in ("-p", "--password"):
                config['password'] = value
            elif name in ("-y", "--year"):
                config['year'] = value
        for key,value in config.items():
            if key == 'year' and value == '':
               config['year']= now
            elif value == '':
               sys.exit()

    except:
        print(usage)
        sys.exit()

    Login(config['user'],config['password'])
    req_jsb(header,dic,config['year'])


if __name__ == '__main__':
    r = requests.session()
    main()