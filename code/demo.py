x = [1,2,3]
y = [1,3,5]
t = [1,8,10]

mt = [5,8,10]
mx = [1,3,3]
my = [1,3,3]

dx = []
dy = []
dt = []
for i in range(len(x)-1):
    tempx = mx[i]-(x[i+1]-x[i])
    tempy = my[i]-(y[i+1]-y[i])
    tempt = mt[i]-(t[i+1]-t[i])
    if tempx <= 0 or tempy<=0 or tempt <=0:
        continue
    else:
        dx.append(tempx)
        dy.append(tempy)
        dt.append(tempt)
Area = 0
Area0 = 0
for i in range(len(x)):
    Area = Area + x[i]*y[i]*t[i]
for i in range(len(dx)):
    Area0 = Area0 + dx[i]*dy[i]*dt[i]
print(Area0/Area)