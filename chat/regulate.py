import aiml
import os
import hashlib
import requests
import time
import tkinter
import tkinter as tk
import threading
from tkinter import *
from tkinter import messagebox, scrolledtext
import json,urllib
from urllib.parse import urlencode
import urllib.request
import io  
from PIL import Image, ImageTk 
import pygame
from py2neo import Graph, Node, Relationship
import Stroke

#启动aiml,连接语料库
mybot_path = 'D:\\chat\\'
os.chdir(mybot_path)
mybot = aiml.Kernel()#启动aiml服务
mybot.learn("std-startup.xml")#以下两句用于导入语料库
mybot.respond('LOAD AIML A')

def getWeather():#获得当天实时天气的API
    url = 'http://api.k780.com'
    params = {
      'app' : 'weather.today',
      'weaid' : 'zhenjiang',
      'appkey' : '55198',
      'sign' : '41c4453f512e07ba8c808a1d1569cc38',
      'format' : 'json',
    }
    params = urlencode(params)

    f = urllib.request.urlopen('%s?%s' % (url, params))
    nowapi_call = f.read()
    #print content
    a_result = json.loads(nowapi_call)
    if a_result:
      if a_result['success'] != '0':
        return a_result['result']['citynm']+"今天的温度区间为："+ a_result['result']['temperature']+",当前温度和天气情况："+a_result['result']['temperature_curr']+a_result['result']['weather']+",今日最高温度为："+a_result['result']['temp_high']+"℃；最低温度为："+a_result['result']['temp_low']+"℃"
      else:
        print (a_result['msgid']+' '+a_result['msg'])
    else:
      print ('Request nowapi fail.')   

def director(input):#连接neo4j进行查询并返回结果。1、某某导演导演了什么电影？
    #连接数据库
    directorGraph = Graph("http:localhost:7474",username="neo4j",password="myneo4j")
    #查找节点
    cypher_text ="""
        MATCH (n:director{{director:'{first_name}'}})-[:directed]->(m:movie)  RETURN m.name
        """.format(first_name=input)
    result =directorGraph.run(cypher_text)
    return result

def actor(input1):#2、某某演员参演了什么电影？
    actorGraph = Graph("http:localhost:7474",username="neo4j",password="myneo4j")
    cypher_text ="""
        MATCH (n:actor{{actor:'{name}'}})-[:acted]->(m:movie)  RETURN m.name
        """.format(name=input1)
    result =actorGraph.run(cypher_text)
    return result

def coop(input2):#3、和某某导演合作过的演员有那些？
    coopGraph = Graph("http:localhost:7474",username="neo4j",password="myneo4j")
    cypher_text ="""
        MATCH (:director{{director:'{name}'}})-[:cooperate]->(m:actor) RETURN m.actor
        """.format(name=input2)
    result =coopGraph.run(cypher_text)
    #print(result)
    return result

def rcoo(input3):#4、某某演员和那些导演合作过？MATCH (n:director)-[:cooperate]->(:actor{actor:"张国荣"}) RETURN n;
    rcooGraph = Graph("http:localhost:7474",username="neo4j",password="myneo4j")
    cypher_text ="""
        MATCH (n:director)-[:cooperate]->(:actor{{actor:'{name}'}}) RETURN n.director
        """.format(name=input3)
    result =rcooGraph.run(cypher_text)
    return result

def movie(input4):#5、某某电影参演的演员有哪些?
    movieGraph = Graph("http:localhost:7474",username="neo4j",password="myneo4j")
    cypher_text ="""
        MATCH  (n:actor)-[:acted]->(:movie{{name:'{name}'}})  RETURN n.actor;
        """.format(name=input4)
    result =movieGraph.run(cypher_text)
    return result

#def Judge_CH(content):#判断翻译成什么语言
   # for ch in content:
       # if u'\u4e00' <= ch <= u'\u9fff':
        #    return "en"
    #return "zh"

#def translate(mes):#使用百度翻译API翻译
    #if(mes==""):
     # return "对不起，我不知道你在说什么"
    #url = "http://api.fanyi.baidu.com/api/trans/vip/translate?from=auto&appid=20201029000602088&salt=1435660288&q="
    #appid="20201029000602088"
    #salt="1435660288"
    #key="Z0xMCmJwjtPHZYZcMb7D"
    #createString=appid+mes+salt+key
    #md5 = hashlib.md5(createString.encode("utf8")).hexdigest()    
    #识别输入中是否有中文
    #tolang=Judge_CH(mes)
    #translateUrl=url+mes+"&sign="+md5+"&to="+tolang
    #print(translateUrl)
    #result = requests.post(translateUrl).json()
    #result = result['trans_result'][0]['dst']
    #return result

def main():
      
    def sendMsg():#发送消息
        strMsg ="我"+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+":" 
        txtMsgList.insert(END, strMsg, 'greencolor')
        content=txtMsg.get('0.0', END)
        txtMsgList.insert(END,content+"\n",'greencolor')
        #txtMsgList.insert(END, getWeather(),'greencolor')
        response =mybot.respond(content)#aiml人工智能标记语言，
        txtMsgList.insert(END,"机器人:"+response+"\n")
        txtMsgList.insert(END,"\n")
        txtMsgList.see(END)
        #print(response)         
        if(response==""):
            recvfromroot ="我现在还不能回答你，也可能你根本上就没问问题，对不对？"+"\n"
            txtMsgList.insert(END, recvfromroot)
            txtMsg.delete('0.0', END)
        elif(response=="查询天气"):
           recvfromroot=" "+getWeather()+"\n"
           txtMsgList.insert(END, recvfromroot)
        elif(response=="正在为你播放周杰伦：夜曲"):
           play_music()
        if(response[0] == '#'):#连接neo4j进行查询并返回结果。1、某某导演导演了什么电影？
                if response.__contains__("neo4j"):#判断neo4j这个字符串是否存在于response中
                  res = response.split(':')#将response通过split()函数分成两部分
                  entity = str(res[1].replace(" ",""))#replace去掉空白,neo4j返回的中文字符中间会加上空格得先去掉才能查询，这里的res[1]既为返回的文字部分回答
                  recvfromroot = director(entity)
                  for i in recvfromroot:
                       txtMsgList.insert(END, i)
                       txtMsgList.insert(END,"\n")
        elif(response[0] == '@'):#2、某某演员参演了什么电影？
                if response.__contains__("neo4j"):#判断neo4j这个字符串是否存在于response中
                  res = response.split(':')#将response通过split()函数分成两部分
                  entity = str(res[1].replace(" ",""))#replace去掉空白，这里的res[1]既为返回的文字部分回答
                  recvfromroot = actor(entity)
                  for i in recvfromroot:
                       txtMsgList.insert(END, i)
                       txtMsgList.insert(END,"\n")
        elif(response[0] == '0'):#3、和某某导演合作过的演员有那些？
                if response.__contains__("neo4j"):#判断neo4j这个字符串是否存在于response中
                  #print(response)
                  res = response.split(':')#将response通过split()函数分成两部分
                  entity = str(res[1].replace(" ",""))#replace去掉空白，这里的res[1]既为返回的文字部分回答
                  print(entity)
                  recvfromroot = coop(entity)
                  for i in recvfromroot:
                       txtMsgList.insert(END, i)
                       txtMsgList.insert(END,"\n")
        elif(response[0] == '1'):#4、某某演员和那些导演合作过？
                if response.__contains__("neo4j"):#判断neo4j这个字符串是否存在于response中
                  #print(response)
                  res = response.split(':')#将response通过split()函数分成两部分
                  entity = str(res[1].replace(" ",""))#replace去掉空白，这里的res[1]既为返回的文字部分回答
                  recvfromroot = rcoo(entity)
                  for i in recvfromroot:
                       txtMsgList.insert(END, i)
                       txtMsgList.insert(END,"\n")
        elif(response[0] == '2'):#5、某某电影参演的演员有哪些?
                if response.__contains__("neo4j"):#判断neo4j这个字符串是否存在于response中
                  #print(response)
                  res = response.split(':')#将response通过split()函数分成两部分
                  entity = str(res[1].replace(" ",""))#replace去掉空白，这里的res[1]既为返回的文字部分回答
                  recvfromroot = movie(entity)
                  for i in recvfromroot:
                       txtMsgList.insert(END, i)
                       txtMsgList.insert(END,"\n")

        if(response[0] == 'S'):#查询致病原因
                if response.__contains__("neo4j"):
                  #print(response)
                  res = response.split(':')
                  entity = str(res[1].replace(" ",""))
                  recvfromroot = Stroke.reason(entity)
                  for i in recvfromroot:
                       txtMsgList.insert(END, i)
                       txtMsgList.insert(END,"\n")        

        if(response[0] == 'P'):#查询预防措施
                if response.__contains__("neo4j"):
                  #print(response)
                  res = response.split(':')
                  entity = str(res[1].replace(" ",""))
                  recvfromroot = Stroke.pm(entity)
                  for i in recvfromroot:
                       txtMsgList.insert(END, i)
                       txtMsgList.insert(END,"\n")  

        if(response[0] == 'M'):#对节点信息进行修改
                if response.__contains__("neo4j"):
                  #print(response)
                  res = response.split(':')
                  entity = str(res[1].replace(" ",""))
                  entity1 = str(res[2].replace(" ",""))
                  entity2 = str(res[3].replace(" ",""))
                  entity3 = str(res[4].replace(" ",""))
                  recvfromroot = Stroke.Modify(entity,entity1,entity2,entity3)
                  txtMsgList.insert(END,"修改之后的结果为:\n")
                  for i in recvfromroot:
                       txtMsgList.insert(END,i)
                       txtMsgList.insert(END,"\n")

        if(response[0] == 'a'):#新增预防措施
                if response.__contains__("neo4j"):
                  #print(response)
                  res = response.split(':')
                  entity = str(res[1].replace(" ",""))
                  entity1 = str(res[2].replace(" ",""))
                  recvfromroot = Stroke.nadd(entity,entity1)
                  txtMsgList.insert(END,"新增节点完成！")
                #   for i in recvfromroot:
                #        txtMsgList.insert(END, i)
                #        txtMsgList.insert(END,"\n")
                
        if(response[0] == 'd'):#删除预防措施
                if response.__contains__("neo4j"):
                  #print(response)
                  res = response.split(':')
                  entity = str(res[1].replace(" ",""))
                  recvfromroot = Stroke.delete(entity)
                  txtMsgList.insert(END,"已经删除节点及关系！")
                #   for i in recvfromroot:
                #        txtMsgList.insert(END, i)
                #        txtMsgList.insert(END,"\n")  
        
        #else:
           #time.sleep(1)
           # recvfromroot = "机器人:"+translate(response)+"\n"
        
        txtMsg.delete('0.0', END)

    def play_music_start():
        filepath = "D:\\周杰伦 - 夜曲.mp3";
        pygame.mixer.init()
          # 加载音乐
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play(start=0.0)
          #播放时长，没有此设置，音乐不会播放，会一次性加载完
        time.sleep(227)
        pygame.mixer.music.stop()

    def play_music():#给播放音乐开一个单独的线程。   
        thread=threading.Thread(target=play_music_start)
        thread.start()

    def cancelMsg():#取消信息
        txtMsg.delete('0.0', END)

    def sendMsgEvent(event):#发送消息事件
        if event.keysym =='Up':
            sendMsg()
    
    #将窗口居中显示
    def set_win_center(root, curWidth='', curHight=''):
        if not curWidth:
         '''获取窗口宽度，默认200'''
        curWidth = root.winfo_width()
        if not curHight:
         '''获取窗口高度，默认200'''
        curHight = root.winfo_height()
        print(curWidth, curHight)
        scn_w, scn_h = root.maxsize()# 获取屏幕宽度和高度
        cen_x = (scn_w - curWidth) / 2# 计算中心坐标
        cen_y = (scn_h - curHight) / 2
        print(cen_x, cen_y)
        size_xy = '%dx%d+%d+%d' % (curWidth, curHight, cen_x, cen_y)# 计算出面积和坐标，%d表示整数。设置窗口初始大小和位置
        root.geometry(size_xy)   

    
    def resize(w, h, w_box, h_box, pil_image):#图片同比例缩放  
      f1 = 1.0*w_box/w  
      f2 = 1.0*h_box/h  
      factor = min([f1, f2])    
      width = int(w*factor)  
      height = int(h*factor)  
      return pil_image.resize((width, height), Image.ANTIALIAS) 

    #创建窗口
    app = Tk()
    app.title('aiml对话框')

    
    canvas = Canvas(app, width=720,height=520,highlightthickness=0)
    imgpath = 'D:\\chat\\3.gif'
    img = Image.open(imgpath)
    #w, h = img.size
    #pil_image_resized = resize(w, h, 720, 520,img)
    photo = ImageTk.PhotoImage(img)
    canvas.create_image(420, 450,image=photo)#里面的前两个参数为坐标
    canvas.grid(columnspan = 3,rowspan = 3)

    #label=tkinter.Label(app,image=photo)  #图片
    #label.grid()

    #创建frame容器
    frmLT = Frame(width = 500, height = 320, bg = 'white')
    frmLC = Frame(width = 515, height = 150, bg = 'white')
    frmLB = Frame(width = 130, height = 26)
    #frmRT = Frame(width = 200, height =250)

    #创建控件
    txtMsgList = Text(frmLT)
    txtMsgList=scrolledtext.ScrolledText(width=62, height=20)
    txtMsgList.tag_config('greencolor',foreground = '#008C00')#创建tag
    #txtMsgList = Text(app,font=("华文彩云",8),fg="black")
    txtMsgList.grid(row=0,column=0,sticky=W)

    txtMsg = Text(frmLC)
    txtMsg.bind("<KeyPress-Up>", sendMsgEvent)#向上键发送
    txtMsg.grid(row =1, column = 0)

    btnSend = Button(frmLB, text = '发送', width = 8, command = sendMsg)#加入bg="red"可修改按钮背景颜色。
    btnCancel =Button(frmLB, text = '取消', width = 8, command = cancelMsg)

    #读取图片，并自适应标签大小
    #pil_image = Image.open('D://chat//2.png')
    #w, h = pil_image.size
    #pil_image_resized = resize(w, h, 200, 320, pil_image)
    #tk_image = ImageTk.PhotoImage(pil_image_resized) 
    #lblImage = Label(frmRT)
    #lblImage = Label(image=tk_image) 
    #lblImage.grid(row = 0, column = 2,sticky=N)

    #窗口布局 使用grid网格布局，读者需要理解参数row、column等的意思。
    frmLT.grid(row = 0, column = 0, columnspan = 2, padx = 1, pady = 3,sticky=NW)
    frmLC.grid(row = 1, column = 0, columnspan = 2, padx = 1, pady = 3,stick=NW)
    frmLB.grid(row = 2, column = 0, columnspan = 2,sticky=NW)
    #frmRT.grid(row = 0, column =2,columnspan = 2, rowspan = 3, padx =2, pady = 3,sticky=N)

    #固定大小
    frmLT.grid_propagate(0)
    frmLC.grid_propagate(0)
    frmLB.grid_propagate(0)
    #frmRT.grid_propagate(0)

    btnSend.grid(row = 2, column = 0)
    btnCancel.grid(row = 2, column = 1)

    #窗口居中
    app.resizable(False, False)#窗口大小不能改变
    app.update()
    set_win_center(app, 720, 520)
    #主事件循环
    app.mainloop()

if  __name__ == "__main__":
   main()