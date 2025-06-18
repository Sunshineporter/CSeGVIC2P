import pandas as pd
from itertools import product
import xmind
# 影响因素类
class Factor:
    #name 功能名称
    #data 同一功能的不同情况,类型为list[]
    def __init__(self, name) -> None:
        self.name = name ## 速度、雨刷器、灯光、方向
        self.item = []
class Item:
    def __init__(self,name) -> None:
        self.name = name ## 时间、行为
        self.data = [] ## 时间、行为的具体数据



##生成函数
def generation(data):
    factor = [] #影响因素的列表集合
    curfactor = Factor(data[0].date) #第一个功能的名称
    curItem = Item(data[0].name)    #第一个功能的具体分类
    curItem.data.append(data[0].data)
    curfactor.item.append(curItem)
    factor.append(curfactor)
    # itemNum = [] #影响因素的具体数据的数量
    # factorName = [] #影响因素的具体名称
    # factorName.append(data[0].date)
    # for i in range(50):
    #     itemNum.append(0)
    curFactorNum = 1
    for i in range(len(data)):
        name = data[i].date
        factordata = Item(data[i].name)
        factordata.data.append(data[i].data)
        isIn,index = CompareNoCase(name,factor)
        if isIn:
            if curFactorNum != 1:
                itemIsIn,itemIndex = Compare(factordata.name,factor[index].item)
                if itemIsIn:
                    factor[index].item[itemIndex].data.append(data[i].data)
                else:
                    factor[index].item.append(factordata)
            curFactorNum = curFactorNum+1
        else:
            curFactorNum = curFactorNum+1
            aa = Factor(name)
            aa.item.append(factordata)
            factor.append(aa)
            del aa
    ##  显示分类树
    # for i in range(len(factor)):
    #     print(factor[i].name)
    #     for j in range(len(factor[i].item)):
    #         print(factor[i].item[j].name,factor[i].item[j].data)
    endData = []
    for i in factor:
        endData.append(fun_permutation(i))
    # for temp in endData:
    #     print(temp.get("name"))
    #     for i in temp.get("permutation"):
    #         print(i)
    endPer = end_permutation(endData)
    functioncsv(endPer,factor)
    # Gemeration_STree(factor)
    

##判断功能是否已经存在
def CompareNoCase(name,factor):
    index = 0
    for d in factor:
        if name == d.name:
            return True,index
        index = index + 1
    return False,index
##判断场景具体分类是否已经存在
def Compare(name,item):
    index = 0
    for d in item:
        if name == d.name:
            return True,index
        index = index + 1
    return False,index

## 动态场景(具体场景)的排列组合
def fun_permutation(secen):
    loop_val = []
    for i in secen.item:
        loop_val.append(i.data)
    return {"name":secen.name,"permutation":product(*loop_val)}

## 动态场景最终的排列组合
def end_permutation(endData):
    loop_val = []
    for i in endData:
        loop_val.append(i.get("permutation"))
    # for i in product(*loop_val):
    #     print(i)
    return product(*loop_val)
##python输出静态上下文表
def functioncsv(end_data,factor):
    dataColumns = []
    for cur in factor:
        for temp in cur.item:
            dataColumns.append((cur.name,temp.name))
    timeindex = findIndex(dataColumns)
    # print(timeindex)
    df = pd.DataFrame(columns=pd.MultiIndex.from_tuples(dataColumns) )
    
    # df = pd.DataFrame(columns=dataColumns)
    # loop_val = []
    # for i in range(len(factor)):
    #     loop_val.append(factor[i].data)
    ## 输出表格
    for i in end_data:
        temp1 = (*i[0],*i[1],*i[2],*i[3])
        ##找到不同时间的并删除
        isSame = del_differ_time(temp1,timeindex)
        if isSame:
            df.loc[len(df)]=list(temp1)
    df.to_excel('输出功能表.xlsx')

## 生成分类树
# for i in range(len(factor)):
#     print(factor[i].name)
#     for j in range(len(factor[i].item)):
#         print(factor[i].item[j].name,factor[i].item[j].data)
def Gemeration_STree(factor):
    workbook = xmind.load('功能分类树.xmind')
    sheet = workbook.getPrimarySheet()
    sheet.setTitle("功能分类树")
    # root node
    root = sheet.getRootTopic()
    root.setTitle("功能")
    for i in range(len(factor)):
        node1 = root.addSubTopic()
        node1.setTitle(factor[i].name)
        for j in range(len(factor[i].item)):
            node2 = node1.addSubTopic()
            node2.setTitle(factor[i].item[j].name)
            for k in factor[i].item[j].data:
                node3 = node2.addSubTopic()
                node3.setTitle(k)
    xmind.save(workbook)

##找到时间的列
def findIndex(dataColumns):
    index = []
    for i in range(len(dataColumns)):
        if dataColumns[i] == ('速度', '时间') or dataColumns[i] == ('灯光', '时间') or dataColumns[i] == ('方向', '时间') or dataColumns[i] == ('雨刷器', '时间'):
            index.append(i)
    return index

##找到不同时间的并删除
def del_differ_time(temp1,timeindex):
    if temp1[timeindex[0]] == temp1[timeindex[1]]== temp1[timeindex[2]]== temp1[timeindex[3]] :
        return True
    else:
        return False