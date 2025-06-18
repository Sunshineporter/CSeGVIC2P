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
actor_list=[]

# 连接到CARLA服务器
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
# 获取世界对象和蓝图库
world = client.get_world()
blueprint_library = world.get_blueprint_library()
# 在世界中生成一辆汽车
blueprint = blueprint_library.filter('vehicle.tesla.model3')[0]

# 设置汽车的初始位置和朝向
transform1 = carla.Transform(carla.Location(x=20, y=130, z=0.5), carla.Rotation(yaw=-180))
transform2 = carla.Transform(carla.Location(x=45, y=130, z=0.5), carla.Rotation(yaw=-180))## 45 130
transform3 = carla.Transform(carla.Location(x=60, y=130, z=0.5), carla.Rotation(yaw=-180))  ##20 127
# 在世界中生成三辆汽车
vehicle1 = world.spawn_actor(blueprint, transform1)
vehicle2 = world.spawn_actor(blueprint, transform2)
vehicle3 = world.spawn_actor(blueprint, transform3)
# 激活汽车的自动驾驶模式
vehicle1.set_autopilot(True)
vehicle2.set_autopilot(True)
vehicle3.set_autopilot(True)

actor_list.append(vehicle1)
actor_list.append(vehicle2)
actor_list.append(vehicle3)


# 创建一个行为代理对象
agent = BehaviorAgent(vehicle3, behavior='normal')
# agent.set_destination((100, 100, 0))
agent.set_destination(agent.vehicle.get_location(),carla.Location(x=-5,y=150,z=0.500000))
# 让汽车行驶一段时间
while True:
    vehicle_location = vehicle3.get_location()
    distance = vehicle_location.distance(carla.Location(x=-5, y=150, z=0.500000))
    # print(distance)
    if distance < 6:
        break
    # 获取车辆的位置和waypoint
    # location = vehicle3.get_location()
    # waypoint = world.get_map().get_waypoint(location)
    # # 获取车辆周围的其他车辆列表
    # # vehicle_list=[]
    # vehicle_list = world.get_actors().filter('*vehicle*')
    # vehicle_list = [v for v in vehicle_list if v.id != vehicle3.id]
    # # 使用_overtake()方法进行超车
    # print(len(vehicle_list))
    #
    # agent._overtake(location, waypoint, vehicle_list)
    # 应用控制命令
    # vehicle.apply_control(control)
    # 等待一段时间，模拟汽车行驶的过程
    # time.sleep(0.1)
    time.sleep(0.1)
    spectator = world.get_spectator()
    transform5 = vehicle3.get_transform()
    spectator.set_transform(carla.Transform(transform5.location + carla.Location(z=40),
                                            carla.Rotation(pitch=-90)))  # 设置跟随汽车视角
# 销毁所有生成的对象
for actor in actor_list:
    actor.destroy()
print("销毁完毕")