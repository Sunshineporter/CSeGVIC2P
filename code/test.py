import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Query, Form
from typing import List,Dict
from pydantic import BaseModel
import staticGeneration
import dynamicGeneration
import functionGeneration
import sceneGeneration
import pandas as pd
import generationSpaceTime as generationSpaceTime
import numpy as np
from matplotlib import pyplot as plt
import mysql.connector
from mpl_toolkits.mplot3d import Axes3D
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

##静态场景对象
class demo(object):
  def __init__(self, date, name):
    self.date = date
    self.name = name

##动态场景对象
class demo1(object):
  def __init__(self, date, name,data):
    self.date = date
    self.name = name
    self.data = data

##动态文件上传
@app.get("/upLode2")
def read_root1(aa: str=Query()):
    bb = aa.split("\n")
    ll = []
    for x in bb:
        cc = x.split("\t")
        if "\r" in cc[2]:
           cc[2] = cc[2].replace('\r','')
        cur = demo1(cc[0], cc[1],cc[2])
        ll.append(cur)
        
    return {"da": ll}


##功能对象
class function(object):
  def __init__(self, date, name,data):
    self.date = date ##功能名称
    self.name = name    ##功能具体分类
    self.data = data    ##功能具体数据
##功能文件上传
@app.get("/upLode3")
def read_root2(aa: str=Query()):
    bb = aa.split("\n")
    ll = []
    for x in bb:
        cc = x.split("\t")
        if "\r" in cc[2]:
           cc[2] = cc[2].replace('\r','')
        cur = function(cc[0], cc[1],cc[2])
        ll.append(cur)
        
    return {"da": ll}


##静态文件上传
@app.get("/upLode")
def read_root(aa: str=Query()):
    bb = aa.split("\n")
    ll = []
    for x in bb:
        # print(x)
        cc = x.split("\t")
        if "\r" in cc[1]:
           cc[1] = cc[1].replace('\r','')
        cur = demo(cc[0], cc[1])
        ll.append(cur)
    return {"da": ll}


##导出静态txt文件
class Cur(BaseModel):
  index : int
  date : str
  name : str
class CurList(BaseModel):
    data: List[Cur]
@app.post("/statictxt/")
def login(tabledata:CurList):
    f=open("静态场景.txt",encoding='utf-8',mode ="w")
    print(tabledata.data)
    print(type(tabledata.data))
    for d in tabledata.data:
        f.write(d.date+'\t'+d.name+'\n') 
    f.truncate(f.tell()-2)
    f.close
    return {"aa": "成功"}
##生成表格
@app.post("/staticGen/")
def login(tabledata:CurList):
    
    staticGeneration.generation(tabledata.data)
  
    return {"aa": "成功"}

##导出动态txt文件
class Cur2(BaseModel):
  index : int
  date : str
  name : str
  data : str
class CurList2(BaseModel):
    data: List[Cur2]
@app.post("/dynamictxt/")
def login2(tabledata:CurList2):
    f=open("动态场景.txt",encoding='utf-8',mode ="w")
    
    for d in tabledata.data:
        f.write(d.date+'\t'+d.name+'\t'+d.data+'\n') 
    f.truncate(f.tell()-2)
    f.close
    return {"aa": "成功"}
##导出功能txt文件  和动态共用一个类
@app.post("/functiontxt/")
def login3(tabledata:CurList2):
    f=open("输出功能.txt",encoding='utf-8',mode ="w")
    for d in tabledata.data:
        f.write(d.date+'\t'+d.name+'\t'+d.data+'\n') 
    f.truncate(f.tell()-2)
    f.close
    return {"aa": "成功"}

##生成动态上下文表格
@app.post("/dynamicGen/")
def dynamicGen(tabledata:CurList2):
    ##去除表格中相同元素
    for i in range(len(tabledata.data)-1):
       j = i+1
       while j < len(tabledata.data):
          if compare(tabledata.data[i],tabledata.data[j]):
             tabledata.data.remove(tabledata.data[j])
          j = j+1
    # for i in tabledata.data:
    #    print(i)
    dynamicGeneration.generation(tabledata.data)
  
    return {"aa": "成功"}
##生成输出功能表格
@app.post("/functionGen/")
def functionGen(tabledata:CurList2):
    ##去除表格中相同元素
    for i in range(len(tabledata.data)-1):
       j = i+1
       while j < len(tabledata.data):
          if compare(tabledata.data[i],tabledata.data[j]):
             tabledata.data.remove(tabledata.data[j])
          j = j+1
    # for i in tabledata.data:
    #    print(i)
    functionGeneration.generation(tabledata.data)

    return {"aa": "成功"}
## 对比元素是否相同
def compare(a,b):
   if a.date == b.date and a.name == b.name and a.data == b.data:
      return True
   else:
      return False


## 生成场景
# function_filename:str,,function_filename
@app.get("/sceneGen/")
def functionGen(static_filename:str,people_filename:str,car_filename:str,light_filename:str,peopleNum:int,carNum:int,lightNum:int):
    sceneGeneration.generation(static_filename,people_filename,car_filename,light_filename,peopleNum,carNum,lightNum)
    return {"aa": "成功"}



# 合成的场景类
class allSecne(object):
    #name 影响因素名称
    #data 同一影响因素的不同情况,类型为list[]
    def __init__(self, rodeNum,trafficSign,weather,rodeType,rodeCondition,position,people1='无',people2='无',car1='无',car2='无',light='无') -> None:
        self.rodeNum = rodeNum
        self.trafficSign = trafficSign
        self.weather = weather
        self.rodeType = rodeType
        self.rodeCondition = rodeCondition
        self.position = position
        self.people1 = people1
        self.people2 = people2
        self.car1 = car1
        self.car2 = car2
        self.light = light
        
##查看场景上传文件
@app.get("/upLodeScene")
def read_root1(aa: str=Query()):
     # 读取静态csv文件，staticdata.columns里面存放着目录，staticarray里面存放这文件里的内容
    scenedata = pd.read_csv(aa,sep=',',header='infer')
    staticarray=scenedata.values[0::,0:6:] #读取指定列
    tempData = []
    for i in staticarray:
       cur = allSecne(i[0],i[1],i[2],i[3],i[4],i[5])
       tempData.append(cur)

    try:
       peoplecarray = scenedata[["行人1"]].values[0::,0::]
       for i in range(len(peoplecarray)):
          tempData[i].people1 = str(peoplecarray[i])
    except:
       print("没有行人1")
    
    try:
       peoplecarray2 = scenedata[["行人2"]].values[0::,0::]
       for i in range(len(peoplecarray2)):
          tempData[i].people2 = str(peoplecarray2[i])
    except:
       print("没有行人2")

    try:
       carcarray = scenedata[["机动车1"]].values[0::,0::]
       
       for i in range(len(carcarray)):
          tempData[i].car1 = str(carcarray[i])
    except:
       print("没有机动车1")
       
    try:
       carcarray2 = scenedata[["机动车2"]].values[0::,0::]
       for i in range(len(carcarray2)):
          tempData[i].car2 = str(carcarray2[i])   
    except:
       print("没有机动车2")
    
    try:
       light = scenedata[["红绿灯1"]].values[0::,0::]
       for i in range(len(light)):
          tempData[i].light = str(light[i])   
    except:
       print("没有红绿灯")
    

    return {"da": tempData}


## 用户登录
@app.get("/login/")
def login(username: str, password: str):
    mydb = mysql.connector.connect(
       host = "localhost",
       user = "root",
       password = "Whz352904.",
       database = "graduation"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM user")
    myresult = mycursor.fetchall()
    for x in myresult:
       if x[0] == username and x[1] == password:
          return {"aa": "成功"}
    return {"aa": "用户或密码错误"}
##输出的功能类
class funn(BaseModel):
    id:int
    time : str
    speed : str
    light : str
    direction : str
    position : str
    dx : str
    dy : str
    dz : str
    description : str
class funnList(BaseModel):
   data:List[funn]

class curScene(BaseModel):
    rodeNum : int
    trafficSign : str
    weather : str
    rodeType : str
    rodeCondition : str
    position : str
    people1 : str
    people2 : str
    car1 : str
    car2 : str
    light : str


##输出功能
@app.post("/outFunction/")
def outFunction(scene:curScene,funn:funnList):
   mydb = mysql.connector.connect(
       host = "localhost",
       user = "root",
       password = "Whz352904.",
       database = "graduation"
    )
   mycursor = mydb.cursor()
   sql = "INSERT INTO scene(车道数, 交通标识, 天气, 路口类型, 道路状况, UAV坐标, 行人1, 行人2, 机动车1, 机动车2, 红绿灯1) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
   val = (scene.rodeNum,scene.trafficSign,scene.weather,scene.rodeType,scene.rodeCondition,scene.position,scene.people1,scene.people2,scene.car1,scene.car2,scene.light)
   mycursor.execute(sql,val)
   mydb.commit()

   sql = "INSERT INTO funnn(时间, 速度, 灯光, 方向, 坐标, dx, dy, dz, 描述) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
   for x in funn.data:
      val = (x.time,x.speed,x.light,x.direction,x.position,x.dx,x.dy,x.dz,x.description)
      mycursor.execute(sql,val)
      mydb.commit()
   return 0
##加载功能
class funnn(object):
    def __init__(self,id,time,speed,light,direction,position,dx,dy,dz,description):
        self.id = id 
        self.time = time
        self.speed = speed
        self.light = light 
        self.direction = direction
        self.position = position
        self.dx = dx 
        self.dy = dy
        self.dz = dz
        self.description = description
import math
@app.get("/getFunction/")
def outFunction():
   mydb = mysql.connector.connect(
       host = "localhost",
       user = "root",
       password = "Whz352904.",
       database = "graduation"
    )
   mycursor = mydb.cursor()
   mycursor.execute("SELECT * FROM funnn")
   myresult = mycursor.fetchall()
   funnnList = []
   for x in myresult:
      curfunn = funnn(math.ceil(x[0] / 3),x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9])
      funnnList.append(curfunn)
   return funnnList

##生成单个时空数据图
import generationSpaceTime
@app.post("/genSpaceTime/")
def genSpaceTime(fun1:funn,fun2:funn,fun3:funn,ff:str):
   generationSpaceTime.GenerationOne(fun1,fun2,fun3,ff)
   return {"data":"成功"}


## 获取时空数据图
import getSpaceTimeImage
@app.get("/getSpaceTime/")
def getSpaceTime():
   curlist,sceneList = getSpaceTimeImage.getSpaceAndTime()
   return {'curlist':curlist,'scenelist':sceneList}
if __name__ == "__main__":
    uvicorn.run('test:app', host="localhost", port=9090, reload=True)