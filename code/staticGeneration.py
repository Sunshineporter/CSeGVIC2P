import pandas as pd
from itertools import product
import xmind
# 影响因素类
class Factor:
    #name 影响因素名称
    #data 同一影响因素的不同情况,类型为list[]
    def __init__(self, name) -> None:
        self.name = name
        self.data = []



##生成函数
def generation(data):
    factor = [] #影响因素的列表集合
    curfactor = Factor(data[0].date)
    curfactor.data.append(data[0].name)
    factor.append(curfactor)
    itemNum = [] #影响因素的具体数据的数量
    factorName = [] #影响因素的具体名称
    factorName.append(data[0].date)
    for i in range(50):
        itemNum.append(0)
    curFactorNum = 1
    for i in range(len(data)):
        name = data[i].date
        factordata = data[i].name
        isIn,index = CompareNoCase(name,factorName)
        if isIn:
            itemNum[index] = itemNum[index] +1
            if curFactorNum != 1:
                factor[index].data.append(factordata)
        else:
            curFactorNum = curFactorNum+1
            factorName.append(name)
            aa = Factor(name)
            aa.data.append(factordata)
            factor.append(aa)
            del aa
            itemNum[curFactorNum-1] =itemNum[curFactorNum-1] + 1

    # for i in range(len(factor)):
    #     print(factor[i].name,factor[i].data)
    sum = cal_sum(itemNum)
    Staticcsv(sum,factorName,factor)
    Gemeration_STree(factor)
    return 0



##判断因素是否已经存在
def CompareNoCase(d1,d2):
    index = 0
    for d in d2:
        if d == d1:
            return True,index
        index = index + 1
    return False,index
## 判断条件的总和
def cal_sum(a):
    sum = 1
    for x in a:
        if x==0:
            return sum
        sum = sum * x
    return sum

##python输出静态上下文表
def Staticcsv(sum,factorName,factor):

    # print(factorName)
    df = pd.DataFrame(columns=factorName)

    loop_val = []
    for i in range(len(factor)):
        loop_val.append(factor[i].data)
    for i in product(*loop_val):
        #print(list(i))
        #append rows of df2 to end of existing DataFrame

        # df_temp = pd.DataFrame(list(i))
        #print(df_temp)
        df.loc[len(df)]=list(i)
    df.to_csv('静态上下文表.csv',index=False)

## 生成分类树
# for i in range(len(factor)):
#     print(factor[i].name,factor[i].data)
def Gemeration_STree(factor):
    workbook = xmind.load('静态分类树.xmind')
    sheet = workbook.getPrimarySheet()
    sheet.setTitle("静态分类树")
    # root node
    root = sheet.getRootTopic()
    root.setTitle("静态场景")
    for i in factor:
        node1 = root.addSubTopic()
        node1.setTitle(i.name)
        for temp in i.data:
            node2 = node1.addSubTopic()
            node2.setTitle(temp)
    xmind.save(workbook)
