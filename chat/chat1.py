#!/usr/bin/python3
# -*- coding:utf-8 -*-


import aiml
import os
import hashlib
import requests
import time
import tkinter as tk
from tkinter import *
from tkinter import messagebox, scrolledtext

#启动aiml,连接语料库
mybot_path = 'D:\\python3.9\\Lib\\site-packages\\aiml\\botdata\\alice'
os.chdir(mybot_path)
mybot = aiml.Kernel()#启动aiml服务
mybot.learn("startup.xml")#以下两句用于导入语料库
mybot.respond('LOAD ALICE')

def Judge_CH(content):#判断翻译成什么语言
    for ch in content:
        if u'\u4e00' <= ch <= u'\u9fff':
            return "en"
    return "zh"

def translate(mes):#使用百度翻译API翻译
    if(mes==""):
      return "对不起，我不知道你在说什么"
    url = "http://api.fanyi.baidu.com/api/trans/vip/translate?from=auto&appid=20201029000602088&salt=1435660288&q="
    appid="20201029000602088"
    salt="1435660288"
    key="Z0xMCmJwjtPHZYZcMb7D"
    createString=appid+mes+salt+key
    md5 = hashlib.md5(createString.encode("utf8")).hexdigest()    
    #识别输入中是否有中文
    tolang=Judge_CH(mes)
    translateUrl=url+mes+"&sign="+md5+"&to="+tolang
    #print(translateUrl)
    result = requests.post(translateUrl).json()
    result = result['trans_result'][0]['dst']
    return result

#def getWeather():
    # #whereUrl="https://geoapi.qweather.com/v2/city/lookup?location="+locathion
    # gpsUrl="https://restapi.amap.com/v3/geocode/geo?city="+city+"&key=d5312a530725f6e983041af92701912f"
    # location=requests.get(gpsUrl).json()
    # gps=location['geocodes']['0']['location']
    #location="118.58,31.37"
    #weatherUrl="https://devapi.qweather.com/v7/weather/now?location="+location+"&key=b3739edbc6af49ae8cae923b49ce7049"
    # print(url)
    #result=requests.get(weatherUrl).json()
    #return result['now']['text']+",当前体感温度"+result['now']['feelsLike']+"℃"
    
def sendmes_self(self):#发送消息事件
    sendmes()

def sendmes():
    content = entry.get()
    #当没有输入却点击发送的时候弹出警告
    if len(content) == 0:
        messagebox.showinfo(title='警告', message='你要输入文字才行哦!')
        return
    torboot = "我:"+content+"\n"
    scr.insert(END, torboot)
    entry.delete(0,'end')#将输入框已有内容删除，以便于下次输入
    #sendtoroot = translate(content)
    response = mybot.respond(translate(content))#aiml人工智能标记语言，
    print(response)
    #print(sendtoroot)
    #print(response)
    # recvfromroot=getWeather()
    # print(recvfromroot)
    if(response==""):
        recvfromroot = "机器人:"+"我现在的知识满足不了你的提问"+"\n"
    #elif(response=="pleseaReturnWeather"):
        #recvfromroot="机器人:"+getWeather()+"\n"
    else:
        time.sleep(1)
        recvfromroot = "机器人:"+translate(response)+"\n"
    scr.insert(END,recvfromroot)
 
#初始化窗口
root = tk.Tk()
enres = StringVar() #设置变量
root.title("闲聊") #设置窗口标题
root.minsize(300, 200 )
root.maxsize(900, 500) #固定窗口大小
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
size = '%dx%d+%d+%d' % (400, 200, (screenwidth - 300)/2, (screenheight - 200)/2)
root.geometry(size)
#root.geometry("350x150+800+450")  #固定串口位置
 
lable = Label(root,text="我：",font=("微软雅黑",10))
lable.grid(row=1,column=0)
# lable1 = Label(root,text="小岳：",font="微软雅黑")
# lable1.grid(row=0,column=0)#固定位置
 
#设置输入框
entry = Entry(root,font=("微软雅黑",10),width=28)
entry.grid(row=1,column=1)#固定位置
entry.bind("<Return>", sendmes_self)
 
# 对话消息框设置成滚动文本框
scrolW = 30 # 设置文本框的长度
scrolH = 10 # 设置文本框的高度
scr = scrolledtext.ScrolledText(root, width=scrolW, height=scrolH,wrap=tk.WORD,font=("隶书",11))
scr.grid(row=0,column=1)#固定位置


#显示在线人数
lable = Label(root,text="当前聊天室人数",font=("微软雅黑",10))
lable.grid(row=0,column=3)
 
#设置发送按钮，点击的时候去执行sendmes函数
button = Button(root,text="发送",font=("微软雅黑",10),command=sendmes)
button.grid(row=1,column=3,sticky=E)#固定位置,sticky位置微调

 
# #设置退出按钮，点击的时候退出程序
#button1 = Button(root,text="退出",font=("微软雅黑",10),command=root.quit)
#button1.grid(row=1,column=3,sticky=E)#固定位置
 
 
root.mainloop()

#while True:
   # text = input("用户 >> ")
    #if text == 'exit':
    #    break
    #else:
    #    truetext=mybot.respond(translate(text))
    #    time.sleep(1)
    #    text=translate(truetext)
    #    print("小杰 >> ",truetext)
    # print("小杰 >> ",text)