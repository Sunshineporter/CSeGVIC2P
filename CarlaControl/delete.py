import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla
import random
import time

sys.path.append('D:\CARLA_0.9.10.1\WindowsNoEditor\PythonAPI\carla')
from agents.navigation.basic_agent import BasicAgent
from agents.navigation.behavior_agent import BehaviorAgent
# TOWN = 'Town03'




# 连接到CARLA服务器
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
# 获取世界对象和蓝图库
world = client.get_world()
blueprint_library = world.get_blueprint_library()
# 筛选出一辆小型汽车蓝图


actor_list = world.get_actors().filter('vehicle*')
# 销毁所有生成的汽车
for actor in actor_list:
    actor.destroy()
print("销毁完毕")
actor_list = world.get_actors().filter('walker*')
for actor in actor_list:
    actor.destroy()
print("销毁完毕")

actor_list = world.get_actors().filter('collision*')
for actor in actor_list:
    actor.destroy()
print("销毁完毕")