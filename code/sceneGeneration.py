
import pandas as pd
from itertools import product
import itertools
import operator
import chardet
import numpy as np
def generation(static_filename,people_filename,car_filename,light_filename,peopleNum,carNum,lightNum):
    # 读取静态csv文件，staticdata.columns里面存放着目录，staticarray里面存放这文件里的内容
    with open(static_filename, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']
    staticdata = pd.read_csv(static_filename,sep=',',header='infer',encoding=encoding)
    staticarray=staticdata.values[0::,0::]  #读取全部行，全部列
    ## 行人csv
    with open(people_filename, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']
    
    peopledata = pd.read_csv(people_filename,sep=',',header='infer',encoding=encoding)
    peoplearray=peopledata.values[0::,0::]  #读取全部行，全部列
    ##机动车csv
    with open(car_filename, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']
    cardata = pd.read_csv(car_filename,sep=',',header='infer',encoding=encoding)
    cararray=cardata.values[0::,0::]  #读取全部行，全部列
    ##红绿灯csv
    with open(light_filename, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']
    lightdata = pd.read_csv(light_filename,sep=',',header='infer',encoding=encoding)
    lightarray=lightdata.values[0::,0::]  #读取全部行，全部列
    list_people = list(itertools.combinations(peoplearray, peopleNum))
    
    
    for i in range(len(list_people)):
        list_people[i] = list(list_people[i])
        for j in range(len(list_people[i])):
            list_people[i][j] = list(list_people[i][j])
    ##去除相同的
    if peopleNum>0:
        for cur in list_people[:]:
            isSame = False
            temp = cur[0]
            for j in range(peopleNum-1):
                if temp[1] == cur[j+1][1]:
                    isSame = True
            if isSame:
                list_people.remove(cur)

    ## 对机动车按照输入的数量进行排列组合
    list_car =list(itertools.combinations(cararray, carNum))
    
    for i in range(len(list_car)):
        list_car[i] = list(list_car[i])
        for j in range(len(list_car[i])):
            list_car[i][j] = list(list_car[i][j])
    ##去除相同的
    if carNum>0:
        for cur in list_car[:]:
            isSame = False
            temp = cur[0]
            for j in range(carNum-1):
                if temp[1] == cur[j+1][1]:
                    isSame = True
            if isSame:
                list_car.remove(cur)
    print(len(list_car))

    ## 对红绿灯按照输入的数量进行排列组合
    list_light = list(itertools.combinations(lightarray, lightNum))
    
    for i in range(len(list_light)):
        list_light[i] = list(list_light[i])
        for j in range(len(list_light[i])):
            list_light[i][j] = list(list_light[i][j])
    ##去除相同的
    if lightNum > 0:
        for cur in list_light[:]:
            isSame = False
            temp = cur[0]
            for j in range(lightNum-1):
                if temp == cur[j+1]:
                    isSame = True
            if isSame:
                list_light.remove(cur)

    endcolumns = []
    for i in staticdata.columns:
        endcolumns.append(i)

    for i in range(peopleNum):
        endcolumns.append("行人"+str(i+1))
    for i in range(carNum):
        endcolumns.append("机动车"+str(i+1))
    for i in range(lightNum):
        endcolumns.append("红绿灯"+str(i+1))
    print(endcolumns)
    res = product(staticarray,list_people,list_car,list_light,repeat=1)
    
    df = pd.DataFrame(columns=endcolumns)
    num = 0
    for i in list(res):
        temp = []
        for j in i:
            for k in j:
                temp.append(k)
        df.loc[len(df)]=temp
        num = num+1
        if num >=10000:
            break
    print(3)
    df.to_csv('场景.csv',index=False)
    
