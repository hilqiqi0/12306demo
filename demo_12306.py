# -*- coding: utf-8 -*-

'''
时间：2018年1月18日
题目：12306自动抢票
版本：V1.3
作者: hilqiqi0
'''

import json
from urllib import parse
from io import BytesIO
#from config import *
from json import loads
import requests
from PIL import Image
from fake_useragent import UserAgent
import re
import cons
import urllib.request
import time
import json
import os
import smtplib  
from email.header import Header  
from email.mime.text import MIMEText

# 禁用安全请求警告
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
disable_warnings(InsecureRequestWarning)

session = requests.session()
session.verify = False

ua = UserAgent(verify_ssl=False)
headers = {
    "User-Agent": ua.random,
    "Host":"kyfw.12306.cn",
    "Referer":"https://kyfw.12306.cn/otn/passport?redirect=/otn/"
}

number = 0

#各个站对应编码
station = {}
for i in cons.station_names.split('@'):
    if i:
        tmp = i.split('|')
        station[tmp[1]] = tmp[2]

#需要修改的信息
#USERNAME = "小明"  #登录完成时候的验证 	你账号的名字：假设你叫小明
##train_date = "2018-01-21"
##from_station = station["深圳"]
##to_station = station["平顶山"]
#ordername = "小明" #指定乘车人						你登陆的账号中添加的乘车人：假设本次是你自己乘车，所以是小明


###输入信息
##print("提示（请输入出发时间）：2018-01-21")
##train_date = input("请输入出发时间：")
##cmp = "2018-02-25"
##print("初版：截至订票日期2018-02-25")
##while True:
##    try:       
##        time.strptime(train_date, "%Y-%m-%d")
##    except ValueError as err:
##        print('Exception: ', err)
##        print("输入格式错误，重新输入")
##        train_date = input("请输入出发时间：")
##    else:
##        #print(print("出发时间 %s" %(train_date)))
##        if train_date > cmp:          
##            print("超出截至时间，重新输入")
##            train_date = input("请输入出发时间：")
##        else:            
##            break
##

time_list = []
##
##print(是否购票验证，验证的话需要手动输入，不验证可以离开电脑忙其他的)
##order_check = input("是否购票验证:Y/N")
order_check = "N"

#输入信息
print("提示（请输入出发时间）：2018-01-21,2018-02-01")
train_date_input = input("请输入出发时间：")
cmp = "2018-02-30"
print("初版：截至订票日期2018-02-30")

train_date_num = train_date_input.split(',')
#print(train_date_num)
for i in train_date_num:
    try:       
        time.strptime(i, "%Y-%m-%d")
    except ValueError as err:
        print('Exception: ', err)
        print("输入格式错误，重新输入")
        input("输入错误，请关闭软件，从新打开")

    else:
        #print(print("出发时间 %s" %(train_date)))
        if i > cmp:          
            print("超出截至时间，重新输入")
            input("输入错误，请关闭软件，从新打开")

        else:
            time_list.append(i)
            
for i in time_list:
    print(i)
    
from_station_name = input("请输入出发城市：")
while True:
    try:
        from_station = station[from_station_name]
        if from_station != "":
            #print("出发城市 %s" %(from_station))
            break
    except KeyError as err:
        print('Exception: ', err)
        print("输入错误，重新输入")
        from_station_name = input("请输入出发城市：")
to_station_name=input("请输入到达城市：")
while True:
    try:
        to_station = station[to_station_name]
        if to_station != "":
            #print("到达城市 %s" %(to_station))
            break
    except KeyError as err:
        print('Exception: ', err)
        print("输入错误，重新输入")
        to_station_name=input("请输入到达城市：")     

###座位信息
##seatlist={
##    "商务座":"9",
##    "特等座":"P",
##    "一等座":"M",
##    "二等座":"O",
##    "高级软卧":"6",
##    "软卧":"4",
##    "动卧":"F",
##    "硬卧":"3",
##    "软座":"2",
##    "硬座":"1"
##    }
##print("是否指定座位类型（不进行坐票类型的确定将自动选择票种订票）：Y/N")
##seatType_flag = input("是否指定座位类型：")
##if seatType_flag == "Y":
##    print("提示（座位类型）：商务座、一等座、二等座、高级软卧、软卧、动卧、硬卧、软座、硬座")
##    seatType_num = input("座位类型：")
##    seatType = seatlist.get(seatType_num)
##    #print(seatType)

#多座位类型
seatlist={
    "9":"商务座",
    "P":"特等座",
    "M":"一等座",
    "O":"二等座",
    "6":"高级软卧",
    "4":"软卧",
    "F":"动卧",
    "3":"硬卧",
    "2":"软座",
    "1":"硬座"
    }
ok_seat={
    "商务座":"9",
    "特等座":"P",
    "一等座":"M",
    "二等座":"O",
    "高级软卧":"6",
    "软卧":"4",
    "动卧":"F",
    "硬卧":"3",
    "软座":"2",
    "硬座":"1"
    }
seatType_list = []
seatType_flag = 'Y'
if seatType_flag == "Y":
    print(
'''座位类型:请输入后面数字或者英文大写，逗号隔开
"商 务 座":"9",
"特 等 座":"P",
"一 等 座":"M",
"二 等 座":"O",
"高级软卧":"6",
"软    卧":"4",
"动    卧":"F",
"硬    卧":"3",
"软    座":"2",
"硬    座":"1"
        ''')
    seatType_input_x = input("座位类型：")
    seatType_input = seatType_input_x.upper()  
    seatType_num = seatType_input.split(',') 
    for i in seatType_num:
        print(i)
        seatType = seatlist.get(i.upper())
        seatType_list.append(seatType)
    print(seatType_list)
       


#车次信息
print("是否指定车次（不进行车次的确定将自动选择车次订票）：Y/N")
stationTrain_flag = input("是否指定车次：")
if stationTrain_flag == "Y":
    print("提示（车次【英文大写】）：K238")
    stationTrain = input("车次：")
    #print(stationTrain)

print("用户登录")
username = input("用户名：")
password = input("密码：")
ordername = input("指定乘车人：")


# 第三方 SMTP 服务  
mail_host = "smtp.163.com"      # SMTP服务器  
mail_user = "180xxxxxxxx@163.com"                  # 用户名  发件人邮箱账号
mail_pass = "hxxxxxx"               # 授权密码，非登录密码  
  
sender = '180xxxxxxxx@163.com'    # 发件人邮箱(最好写全, 不然会失败)  
receivers = ["2xxxxxxxx@qq.com"]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱  
  
content = '你好，抢到了，去登陆付款吧。'  
title = '抢到票了'  # 邮件主题  

add = input("请输入邮箱地址：")
receivers.append(add)
  
def sendEmail(SMTP_host, from_account, from_passwd, to_account, subject, content):  
    email_client = smtplib.SMTP(SMTP_host)  
    email_client.login(from_account, from_passwd)  
    # create msg  
    msg = MIMEText(content, 'plain', 'utf-8')  
    msg['Subject'] = Header(subject, 'utf-8')  # subject  
    msg['From'] = from_account  
    msg['To'] = to_account  
    email_client.sendmail(from_account, to_account, msg.as_string())  
  
    email_client.quit()  

#输入信息确认
##print(print("出发时间： %s" %(train_date)))
##print("出发城市： %s" %(from_station))
##print("到达城市： %s" %(to_station))
##print("座    位： %s" %(seatType_num))

def login():
    # 打开登录页面
    print("打开登录页面")
    url = "https://kyfw.12306.cn/otn/login/init"
    session.get(url, headers=headers)
    
    # 发送验证码
    while not captcha():
        print("循环")
    print("验证码检验成功")
    
    # 发送登录信息
    print("开始用户登录")
    data = {
        "username":username,
        "password":password,
        "appid":"otn"
    }
    url = "https://kyfw.12306.cn/passport/web/login"
    #登陆失败后再登陆，match是匹配错的返回
    match = True
    while match:
        response = session.post(url, headers=headers, data=data)
        responseMatch = re.search(r'www.w3.org/1999/xhtml', response.text)
        if responseMatch: 
          #print(responseMatch.group(0))
          print("用户登录失败，重新登录")
          match = True
        else:
          print("用户登录成功！！！")
          match = False
    #print(response.text)
    if response.status_code == 200:
        result = json.loads(response.text)
        #print(result.get("result_message"), result.get("result_code"))
        if result.get("result_code") != 0:
            print("用户登录无响应")
            return False

    print("验证用户登录")
    data = {
        "appid":"otn"
    }
    url = "https://kyfw.12306.cn/passport/web/auth/uamtk"
    response = session.post(url, headers=headers, data=data)
    if response.status_code == 200:
        result = json.loads(response.text)
        #print(result.get("result_message"))
        newapptk = result.get("newapptk")

    print("用户登录：服务器验证")
    data = {
        "tk":newapptk
    }
    url = "https://kyfw.12306.cn/otn/uamauthclient"
    response = session.post(url, headers=headers, data=data)
    if response.status_code == 200:
        #print(response.text)
        print("验证通过")

    print("进入登陆界面")
    url = "https://kyfw.12306.cn/otn/index/initMy12306"
    response = session.get(url, headers=headers)
    with open('response.txt','w',encoding='utf-8') as f:
        f.write(response.text)
    #if response.status_code == 200 and response.text.find(USERNAME) != -1:
    if response.status_code == 200:    
        #print(response)
        return True
    return False

def captcha():
    data = {
        "login_site": "E",
        "module": "login",
        "rand": "sjrand",
        "0.17231872703389062":""
    }

    # 获取验证码
    print("获取验证码图片")
    param = parse.urlencode(data)
    url = "https://kyfw.12306.cn/passport/captcha/captcha-image?{}".format(param)
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        file = BytesIO(response.content)
        img = Image.open(file)
        img.show()       
    
    Reminder ='''
    #################
    #   #   #   #   #
    # 0 # 1 # 2 # 3 # 
    #   #   #   #   #
    #################
    #   #   #   #   #
    # 4 # 5 # 6 # 7 # 
    #   #   #   #   #
    #################
    '''
    print("提示信息：(格式：3,6)")
    print(Reminder)
    captcha_solution = input("请输入验证码: ")
    
    #解析验证码
    soList = captcha_solution.split(',')
    # 由于12306官方验证码是验证正确验证码的坐标范围,我们取每个验证码中点的坐标(大约值)
    yanSol = ['35,60','105,60','175,60','245,60','35,120','105,120','175,120','245,120']
    yanList = []
    for item in soList:
        print(item)
        yanList.append(yanSol[int(item)])
    # 正确验证码的坐标拼接成字符串，作为网络请求时的参数
    positions = ','.join(yanList)
    
    # 发送验证码
    data = {
        "answer": positions,
        "login_site": "E",
        "rand": "sjrand"
    }  
    url = "https://kyfw.12306.cn/passport/captcha/captcha-check"
    response = session.post(url, headers=headers, data=data)
    result = json.loads(response.text) 
    if response.status_code == 200 and result.get("result_code") == "4":            
        #print(result.get("result_message"))
        return True 
    return False

def ordercheck():
    data = {
        "login_site": "E",
        "module": "login",
        "rand": "sjrand",
        "0.17231872703389062":""
    }

    # 获取验证码
    print("获取验证码图片")
    param = parse.urlencode(data)
    url = "https://kyfw.12306.cn/otn/passcodeNew/checkRandCodeAnsyn?{}".format(param)
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        file = BytesIO(response.content)
        img = Image.open(file)
        img.show()       
    
    Reminder ='''
    #################
    #   #   #   #   #
    # 0 # 1 # 2 # 3 # 
    #   #   #   #   #
    #################
    #   #   #   #   #
    # 4 # 5 # 6 # 7 # 
    #   #   #   #   #
    #################
    '''
    print("提示信息：(格式：3,6)")
    print(Reminder)
    captcha_solution = input("请输入验证码: ")
    
    #解析验证码
    soList = captcha_solution.split(',')
    # 由于12306官方验证码是验证正确验证码的坐标范围,我们取每个验证码中点的坐标(大约值)
    yanSol = ['35,60','105,60','175,60','245,60','35,120','105,120','175,120','245,120']
    yanList = []
    for item in soList:
        print(item)
        yanList.append(yanSol[int(item)])
    # 正确验证码的坐标拼接成字符串，作为网络请求时的参数
    positions = ','.join(yanList)
    
    # 发送验证码
    data = {
        "answer": positions,
        "login_site": "E",
        "rand": "sjrand"
    }  
    url = "https://kyfw.12306.cn/passport/captcha/captcha-check"
    response = session.post(url, headers=headers, data=data)
    result = json.loads(response.text) 
    if response.status_code == 200 and result.get("result_code") == "4":            
        #print(result.get("result_message"))
        return True 
    return False

def getList(train_date):
    print("开始查询余票")
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=' + train_date + '&leftTicketDTO.from_station=' + from_station +  '&leftTicketDTO.to_station=' + to_station + '&purpose_codes=ADULT'
    #查询失败，重新查询    
    match = True
    while match:
        response = session.get(url, headers=headers)
        responseMatch = re.search(r'www.w3.org/1999/xhtml', response.text)
        if responseMatch: 
          #print(responseMatch.group(0))
          print("车站信息获取失败，重新查询")
          match = True
        else:
          print("车站信息查询成功")
          match = False
    #print(response.text)
    

    try:
        result = json.loads(response.text)
    except:
        return False
    if result.get("status") != True:
        print("查询余票失败")
        return False
    map = result.get("data").get("map")
    print(map)
    result = result.get("data").get("result")
    print('____________________________') 
    #print(result)
    print('__________查询结果___________') 
    for i in result:
        #填充过滤信息
        lst = i.split('|')
        item = {
            "预定号":lst[0], #secretStr
            "train_no":lst[2],
            "车次":lst[3], #车次
            "始发站":lst[4], #start_station_code
            "终点站":lst[5], #end_station_code
            "起始站":lst[6], #from_station_code
            "目标站":lst[7], #to_station_code
            "出发时间": lst[8], #出发时间
            "到达时间":lst[9], #到达时间
            "历时":lst[10], #历时
            "是否售票":lst[11], #历时
            "列车出发日期":lst[13],#start_train_date
            "train_location":lst[15],
            "高级动卧":lst[21], #高级动卧
            "其他":lst[22], #软卧
            "软卧":lst[23], #软卧
            "软座":lst[24], #软座
            "特等座":lst[25], #特等座
            "无座":lst[26], #无座
            "硬卧":lst[28], #硬卧
            "硬座":lst[29], #硬座
            "二等座":lst[30], #二等座
            "一等座":lst[31], #一等座
            "商务座":lst[32], #商务座
            "动卧":lst[33], #动卧
        }
        
        print("车次 %s" %(item.get("车次")))
        query_from_station_name = map.get(item.get("起始站"))
        query_to_station_name   = map.get(item.get("目标站"))
        print(query_from_station_name)
        print(query_to_station_name)
        #筛选车次
        if stationTrain_flag == "Y":
            if stationTrain == item.get("车次"):
                #判断是否开票了
                if item.get("是否售票") != "Y":
                    print("未开始售票")
                    return False
                    #continue
                print("已开始售票") 
                #筛选座位
                if seatType_flag == "Y":
                    for i in seatType_list:                        
                        if item.get(i) != "" and item.get(i) != "无":
                            print("预订")
                            print(i)
                            print(ok_seat.get(i))
                            secretStr_pre=item.get("预定号")
                            reserveInfo(parse.unquote(secretStr_pre),train_date,query_from_station_name,query_to_station_name)
                            if order(item.get("车次"),ok_seat.get(i)) == True:
                                return True
                            #找到车次后停止循环
                            break
                        else:
                            return False
                #未指定座位
                else:
                    pass

        #未指定车次
        else:
            #判断是否开票了
            if item.get("是否售票") != "Y":
                print("未开始售票")
                #return False
                continue
            print("已开始售票") 
            #筛选座位
            if seatType_flag == "Y":
                for i in seatType_list:                        
                    if item.get(i) != "" and item.get(i) != "无":
                        print("预订")
                        secretStr_pre=item.get("预定号")
                        reserveInfo(parse.unquote(secretStr_pre),train_date,query_from_station_name,query_to_station_name)
                        if order(item.get("车次"),ok_seat.get(i)) == True:
                            return True
                        #找到车次后停止循环
                        break
                    else:
                        pass
                        #return False
                        #continue
            #未指定座位
            else:
                pass

        
    return False

                           

def reserveInfo(secretStr,train_date,query_from_station_name,query_to_station_name):
    print("checkUser")
    url = "https://kyfw.12306.cn/otn/login/checkUser"
    data = {
        "_json_att":""
        }
    response = session.post(url, headers=headers, data=data)
    print(response.text)
    
    url = "https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest"
    data = {
        "secretStr":secretStr,
        "train_date":train_date,
        "back_train_date":train_date,
        "tour_flag":"dc",
        "query_from_station_name":query_from_station_name,
        "query_to_station_name"	:query_to_station_name,
        "purpose_codes":"ADULT"
    }
    response = session.post(url, headers=headers, data=data)
    #查询失败，重新查询    
    match = True
    match_submitOrderRequest_num = 0
    while match:
        response = session.get(url, headers=headers)
        responseMatch = re.search(r'www.w3.org/1999/xhtml', response.text)
        if responseMatch: 
          #print(responseMatch.group(0))
          print("车站信息获取失败，重新查询")
          match = True
          match_submitOrderRequest_num +=1
          if match_submitOrderRequest_num > 15:
              return False
        else:
          print("车站信息查询成功")
          match = False
    #print(response.text)    
    print(response.text)
    if response.status_code == 200:
        result = json.loads(response.text)
        print(result.get("status"))
        if result.get("status") != True:
            return False
        return True
            
    
def order(stationTrainCode,seatType):
    print(stationTrainCode)
    print(seatType)
    print("initDc")
    url = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"
    data={
        "_json_att":""
        }
    
    response = session.post(url, headers=headers, data=data)
    #保存数据
    with open('html.txt','w',encoding='utf-8') as f:
        f.write(response.text)
    #打开数据文件
    c=1#行数
    match=0
    with open("html.txt", mode='r', encoding='UTF-8') as f:
        for line in f:
            c =c+1
            match =re.search("var globalRepeatSubmitToken = '(.*?)';", line)           
            if match:
                print(c)
                ticketToken=match.group(1)
                print("ticketToken")
                print(ticketToken)
            match =re.search("'key_check_isChange':'(.*?)'", line)
            if match:
                print(c)
                key_check_isChange=match.group(1)
                print("key_check_isChange")
                print(key_check_isChange)
                match = False
            match =re.search("'leftTicketStr':'(.*?)'", line)
            if match:
                print(c)
                leftTicketStr=match.group(1)
                print("leftTicketStr")
                print(leftTicketStr)
                match = False            
            match =re.search("'train_location':'(.*?)'", line)
            if match:
                print(c)
                train_location=match.group(1)
                print("train_location")
                print(train_location)
                match = False             
            match =re.search("'purpose_codes':'(.*?)'", line)
            if match:
                print(c)
                purpose_codes=match.group(1)
                print("purpose_codes")
                print(purpose_codes)
                match = False                

    #获取联系人列表
    print("联系人列表")
    data={
        "REPEAT_SUBMIT_TOKEN":ticketToken,
        "_json_att":""
        }
    url = "https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs"
    response = session.post(url, headers=headers, data=data)
    if response.status_code == 200:
        result = json.loads(response.text)
        print(result.get("status"))
        if result.get("status") == True:
            data = result.get("data")
            normal_passengers_pro = data.get("normal_passengers")
            print(normal_passengers_pro)
            #提取联系人信息

            for i in range(len(normal_passengers_pro)):
                #print(normal_passengers_pro[i])
                result = normal_passengers_pro[i]
                if ordername == result.get("passenger_name"):
                    passenger_name = result.get("passenger_name")
                    passenger_id = result.get("passenger_id_no")
                    passenger_mobile = result.get("mobile_no")
                    passenger_id_type_code = result.get("passenger_id_type_code")
                    passenger_type = result.get("passenger_type")
                    passenger_email =result.get("email")

                    
    #passengerTicketStr组成的格式：seatType,0,票类型（成人票填1）,乘客名,passenger_id_type_code,passenger_id_no,mobile_no,’N’
    passengerTicketStr = seatType + ",0,1," + passenger_name + "," + passenger_id_type_code + "," + passenger_id + "," + passenger_mobile + ",N"
    #oldPassengerStr组成的格式：乘客名,passenger_id_type_code,passenger_id_no,passenger_type，’_’
    oldPassengerStr = passenger_name + "," + passenger_id_type_code + "," + passenger_id + "," + passenger_type + "_"
    
    #提交订单
    print("购票人确定")
    while True:
        url="https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo"    
        data={
            "cancel_flag":"2",
            "bed_level_order_num":"000000000000000000000000000000",
            "passengerTicketStr":passengerTicketStr,
            "oldPassengerStr":oldPassengerStr,
            "tour_flag":"dc",
            "randCode":"",
            "whatsSelect":"1",
            "_json_att":"",        
            "REPEAT_SUBMIT_TOKEN":ticketToken
            }
        print(data)
        response = session.post(url, headers=headers, data=data)
        if response.status_code == 200:
            result = json.loads(response.text) 
            if result.get("status") == True:
                if order_check == "Y":
                    #需要验证
                    if result.get("data").get("ifShowPassCode") == "Y":
                        print("55")
                        # 发送验证码
                        while not ordercheck():
                            print("循环")
                        print("验证码检验成功")
                        break
                else:
                    if result.get("data").get("ifShowPassCode") == "N":
                        print("44")
                        break
                    else:
                        return False
                print("33")                   
            print("22")
        print("11")
        pass

    #准备进入队列
    print("准备进入队列")
    url="https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount" 
    data={
        "train_date":"Thu Jan 18 2018 00:00:00 GMT+0800 (中国标准时间)",
        "train_no":"690000K2380B",
        "stationTrainCode":stationTrainCode,
        "seatType":seatType,
        "fromStationTelecode":from_station ,
        "toStationTelecode":to_station,
        "leftTicket":leftTicketStr,
        "purpose_codes":"00",
        "train_location":train_location,
        "_json_att":"",
        "REPEAT_SUBMIT_TOKEN":ticketToken
        }
    response = session.post(url, headers=headers, data=data)
    if response.status_code != 200:
        return False
    result = json.loads(response.text) 
    if result.get("status") != True:
        return False
    
    print("确认购买")
    url="https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue"
    data={   
        "passengerTicketStr":passengerTicketStr,
        "oldPassengerStr":oldPassengerStr,
        "randCode":"",
        "purpose_codes":purpose_codes,
        "key_check_isChange":key_check_isChange,
        "leftTicketStr":leftTicketStr,
        "train_location":train_location,
        "choose_seats":"",
        "seatDetailType":"000",
        "whatsSelect":"1",
        "roomType":"00",
        "dwAll":"N",
        "_json_att":"",
        "REPEAT_SUBMIT_TOKEN":ticketToken
        }
    response = session.post(url, headers=headers, data=data)
    if response.status_code != 200:
        return False
    result = json.loads(response.text) 
    if result.get("status") != True:
        return False
    if result.get("data").get("submitStatus") != True:
        return False
    print("循环发送队列消息")
    while True:
        orderWaitReq= session.post("https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime",data={
            "REPEAT_SUBMIT_TOKEN":ticketToken,
            "_json_att":"",
            "random":time.time(),
            "tourFlag":"dc"
            },headers=headers)
        print(orderWaitReq.content)
        orderWaitJson=orderWaitReq.json()
        if orderWaitJson.get("status") and orderWaitJson.get("httpstatus")==200:
            if orderWaitJson.get("data") is not None and orderWaitJson.get("data").get("orderId") is not None:
                orderId=orderWaitJson.get("data").get("orderId")
                break
            pass
        pass
    #进入队列
    print("进入队列")
    dcQueueReq=session.post("https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue",data={
        "REPEAT_SUBMIT_TOKEN":ticketToken,
        "_json_att":"",
        "orderSequence_no":orderId
        },headers=headers)
    dcQueueJson=dcQueueReq.json()
    if dcQueueJson.get("status") and dcQueueJson.get("httpstatus")==200 and dcQueueJson.get("data") is not None and dcQueueJson.get("data").get("submitStatus"):
        print("订票成功")
        pass
    else:
        print(dcQueueJson.content)
        print("订票失败")
        pass



        
if __name__ == "__main__":
    #登录
    if login():
        print("Success")
    else:
        print("Failed")

    #下订单
##    while True:
##        if getList():
##            print("订票成功")
##            os.system("甩葱歌.mp3")
##            break
##        else:
##            number +=1
##            print("查询次数 %d" %(number))
##            time.sleep(1)
    flag = True
    t_flag =0
    while flag ==True:
        for i in time_list:
            number +=1
            print("-----------------------")
            print("查询次数 %d" %(number))
            time.sleep(2)
            train_date = i
            print(train_date)
            #print(type(train_date))
            if getList(train_date):
                print("有剩余票。。。。。。。。。。。。。。")
                os.system("甩葱歌.mp3")
                for receiver in receivers:
                    sendEmail(mail_host, mail_user, mail_pass, receiver, title, content) 
                t_flag = 1
                input("结束。。。。。")
                break
                
        if t_flag ==1:
            flag = False

