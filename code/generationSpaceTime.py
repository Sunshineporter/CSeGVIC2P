import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import chardet
import os
import pandas as pd
import mysql.connector
def GenerationOne(fun1,fun2,fun3,ff):
        # 定义坐标轴范围
    x_min, x_max = 1, 7.5
    y_min, y_max = 1, 7.5
    time_min, time_max = 1, 30
    # 创建坐标轴数据
    x = np.linspace(x_min, x_max, 100)
    y = np.linspace(y_min, y_max, 100)
    time = np.linspace(time_min, time_max, 100)
    # 创建三维坐标网格
    X, Y, Z = np.meshgrid(x, y, time)
     # 绘制三维图形
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Time')
    ax.set_xlim3d(x_min, x_max)
    ax.set_ylim3d(y_min, y_max)
    ax.set_zlim3d(time_min, time_max)
    taskList = []
    taskList.append(fun1)
    taskList.append(fun2)
    taskList.append(fun3)
    curTaskTime = []
    curTaskXpos = []
    curTaskYpos = []
    dx = []
    dy = []
    dz = []
    curTaskDescribe = []
    for temp in taskList:
        curTaskTime.append(int(temp.time))
        curstr = temp.position.replace('(','')
        curstr = curstr.replace(')','')
        curstr = curstr.split(',')
        curTaskXpos.append(int(curstr[0]))
        curTaskYpos.append(int(curstr[1]))
        dx.append(int(temp.dx))
        dy.append(int(temp.dy))
        dz.append(int(temp.dz))
        curTaskDescribe.append(temp.description)
    for ccc in range(len(dx)):
        ax.text(curTaskXpos[ccc], curTaskYpos[ccc], dz[ccc]+curTaskTime[ccc]+1.0, curTaskDescribe[ccc])
    ax.bar3d(curTaskXpos, curTaskYpos, curTaskTime, dx, dy, dz, color=['red','green','blue'])
    ## 计算重要性
    Deltax = []
    Deltay = []
    Deltat = []
    for j in range(len(curTaskXpos)-1):
        tempx = abs(dx[j])-abs((curTaskXpos[j+1]-curTaskXpos[j]))
        tempy = abs(dy[j])-abs((curTaskYpos[j+1]-curTaskYpos[j]))
        tempt = abs(dz[j])-abs((curTaskTime[j+1]-curTaskTime[j]))
        if tempx <= 0 or tempy<=0 or tempt <=0:
            continue
        else:
            Deltax.append(tempx)
            Deltay.append(tempy)
            Deltat.append(tempt)
    Area = 0
    Area0 = 0
    for j in range(len(curTaskXpos)):
        Area = Area + curTaskXpos[j]*curTaskYpos[j]*curTaskTime[j]
    for j in range(len(Deltax)):
        Area0 = Area0 + Deltax[j]*Deltay[j]*Deltat[j]
    print(Area0/Area)
     # 指定保存的文件夹
    plt.savefig(os.path.join('SpaceTime','时空图'+str(fun1.id)+'.jpg'))
    plt.savefig(os.path.join('C:/Users/henan/Desktop/毕业设计/分类树和生成树/gc-tree/src/SpaceTime','时空图'+str(fun1.id)+'.jpg'))
    plt.clf()
    mydb = mysql.connector.connect(
       host = "localhost",
       user = "root",
       password = "Whz352904.",
       database = "graduation"
    )
    mycursor = mydb.cursor()
    sql = "INSERT INTO importance(函数, 重要性) VALUES(%s,%s)"
    val = (ff,str(Area0/Area))
    mycursor.execute(sql,val)
    mydb.commit()

# 读取输出功能文件，每三行代表一个时间段的任务
# df = pd.read_excel('输出功能.xlsx', sheet_name='Sheet1')
# taskdata=df.values[0::,0::]
# conlums = df.columns ##输出功能的目录
# taskNum = len(taskdata)/3
# f=open("重要性.txt",encoding='utf-8',mode ="w")
# for i in range(int(taskNum)):
#         # 定义坐标轴范围
#     x_min, x_max = 1, 7.5
#     y_min, y_max = 1, 7.5
#     time_min, time_max = 1, 30
#     # 创建坐标轴数据
#     x = np.linspace(x_min, x_max, 100)
#     y = np.linspace(y_min, y_max, 100)
#     time = np.linspace(time_min, time_max, 100)
#     # 创建三维坐标网格
#     X, Y, Z = np.meshgrid(x, y, time)
#     # 绘制三维图形
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')
#     ax.set_xlabel('X')
#     ax.set_ylabel('Y')
#     ax.set_zlabel('Time')
#     ax.set_xlim3d(x_min, x_max)
#     ax.set_ylim3d(y_min, y_max)
#     ax.set_zlim3d(time_min, time_max)
#     # ax.text(xpos[0], ypos[0], dz[0]+zpos[0]+1.0, "staight")
#     taskList = []
#     k = i*3
#     taskList.append(taskdata[k])
#     taskList.append(taskdata[k+1])
#     taskList.append(taskdata[k+2])
#     curTaskTime = []
#     # curTaskSpeed = []
#     # curTaskLight = []
#     # curTaskDirection = []
#     curTaskXpos = []
#     curTaskYpos = []
#     dx = []
#     dy = []
#     dz = []
#     curTaskDescribe = []
#     for temp in taskList:
#         curTaskTime.append(temp[0])
#         # curTaskSpeed.append(temp[1])
#         # curTaskLight.append(temp[2])
#         # curTaskDirection.append(temp[3])
#         curstr = temp[4].replace('(','')
#         curstr = curstr.replace(')','')
#         curstr = curstr.split(',')
#         curTaskXpos.append(int(curstr[0]))
#         curTaskYpos.append(int(curstr[1]))
#         dx.append(temp[5])
#         dy.append(temp[6])
#         dz.append(temp[7])
#         curTaskDescribe.append(temp[8])
#     for ccc in range(len(dx)):
#         ax.text(curTaskXpos[ccc], curTaskYpos[ccc], dz[ccc]+curTaskTime[ccc]+1.0, curTaskDescribe[ccc])
#     ax.bar3d(curTaskXpos, curTaskYpos, curTaskTime, dx, dy, dz, color=['red','green','blue'])
#     ## 计算重要性
#     Deltax = []
#     Deltay = []
#     Deltat = []
#     for j in range(len(curTaskXpos)-1):
#         tempx = abs(dx[j])-abs((curTaskXpos[j+1]-curTaskXpos[j]))
#         tempy = abs(dy[j])-abs((curTaskYpos[j+1]-curTaskYpos[j]))
#         tempt = abs(dz[j])-abs((curTaskTime[j+1]-curTaskTime[j]))
#         if tempx <= 0 or tempy<=0 or tempt <=0:
#             continue
#         else:
#             Deltax.append(tempx)
#             Deltay.append(tempy)
#             Deltat.append(tempt)
#     Area = 0
#     Area0 = 0
#     for j in range(len(curTaskXpos)):
#         Area = Area + curTaskXpos[j]*curTaskYpos[j]*curTaskTime[j]
#     for j in range(len(Deltax)):
#         Area0 = Area0 + Deltax[j]*Deltay[j]*Deltat[j]
#     print(Area0/Area)
    
#     # f.write('时空图'+str(i+1)+'\t'+str(Area0/Area)+'\n')
    
#     # 指定保存的文件夹
#     plt.savefig(os.path.join('SpaceTime','时空图'+str(i+1)+'.jpg'))
#     #plt.show()
#     plt.clf()
# f.truncate(f.tell()-2)
# f.close