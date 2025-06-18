import mysql.connector
class cur(object):
    def __init__(self,scene='',fun='',importance=''):
        self.scene = scene 
        self.fun = fun
        self.importance = importance
def getSpaceAndTime():
    mydb = mysql.connector.connect(
       host = "localhost",
       user = "root",
       password = "Whz352904.",
       database = "graduation"
    )
    curList = []
    sceneList = []
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM scene")
    myresult = mycursor.fetchall()
    for x in myresult:
        cc = cur('场景'+str(x[0]))
        ss = '车道数:'+str(x[1])+'\n'+'交通标识:'+str(x[2])+'\n'+'天气:'+str(x[3])+'\n'+'路口类型:'+str(x[4])+'\n'+'道路状况:'+str(x[5])+'\n'+'UAV坐标:'+str(x[6])+'\n'+'行人1:'+str(x[7])+'\n'+'行人2:'+str(x[8])+'\n'+'机动车1:'+str(x[9])+'\n'+'机动车2:'+str(x[10])+'\n'+'红绿灯1:'+str(x[11])
        curList.append(cc)
        sceneList.append(ss)
    
    mycursor.execute("SELECT * FROM importance")
    myresult = mycursor.fetchall()
    i = 0
    for x in myresult:
        curList[i].fun = x[1]
        curList[i].importance = x[2]
        i = i+1
    i = 0
    # for x in curList:
    #     print(x.scene,' ',x.fun,' ',x.importance)
    return curList,sceneList