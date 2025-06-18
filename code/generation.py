import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# 创建一个3D坐标系
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# 生成数据
xpos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
ypos = [2, 3, 4, 5, 1, 6, 2, 1, 7, 2]
zpos = np.zeros(10)
dx = np.ones(10)
dy = np.ones(10)
dz = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# 绘制3D立体柱状图
ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='b')
# 设置图像标题和轴标签
ax.set_title('3D Bar Chart')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
# 显示图像
plt.show()