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


try:
    # 连接到CARLA服务器
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    # 获取世界对象和蓝图库
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()
    # 筛选出一辆小型汽车蓝图
    blueprint = blueprint_library.filter('vehicle.tesla.model3')[0]
    # 筛选出一个行人蓝图
    walker_blueprint = blueprint_library.filter('walker.pedestrian.0001')[0]
    # 设置汽车的初始位置和朝向
    transform1 = carla.Transform(carla.Location(x=20, y=130, z=0.5), carla.Rotation(yaw=-180))
    transform2 = carla.Transform(carla.Location(x=5, y=110, z=0.5), carla.Rotation(yaw=-90))## 45 130
    transform3 = carla.Transform(carla.Location(x=20, y=126, z=0.5), carla.Rotation(yaw=-180))  ##20 127
    # 设置行人的初始位置和朝向
    walker_transform1 = carla.Transform(carla.Location(x=12, y=111, z=0.5), carla.Rotation(yaw=-90))
    walker_transform2 = carla.Transform(carla.Location(x=12, y=120, z=0.5), carla.Rotation(yaw=-90))
    # 在世界中生成三辆汽车
    vehicle1 = world.spawn_actor(blueprint, transform1)
    vehicle2 = world.spawn_actor(blueprint, transform2)
    vehicle3 = world.spawn_actor(blueprint, transform3)
    # 在世界中生成两个行人
    walker1 = world.spawn_actor(walker_blueprint, walker_transform1)
    walker2 = world.spawn_actor(walker_blueprint, walker_transform2)

    # 创建用于控制行人的Ai
    walker_controller_bp = world.get_blueprint_library().find('controller.ai.walker')
    walker_controller1 = world.spawn_actor(walker_controller_bp, walker_transform1, walker1)
    walker_controller2 = world.spawn_actor(walker_controller_bp, walker_transform2, walker2)
    # 开启控制
    walker_controller1.start()
    walker_controller1.go_to_location(carla.Location(x=12, y=100, z=0.500000))  # 设置行人目的地
    walker_controller1.set_max_speed(1 + random.random())  # Between 1 and 2 m/s (default is 1.4 m/s).
    # 开启控制
    walker_controller2.start()
    walker_controller2.go_to_location(carla.Location(x=12, y=98, z=0.500000))  # 设置行人目的地
    walker_controller2.set_max_speed(1 + random.random())  # Between 1 and 2 m/s (default is 1.4 m/s).
    # 激活汽车的自动驾驶模式
    vehicle1.set_autopilot(True)
    vehicle2.set_autopilot(True)
    vehicle3.set_autopilot(True)

    actor_list.append(vehicle1)
    actor_list.append(vehicle2)
    actor_list.append(vehicle3)
    actor_list.append(walker1)
    actor_list.append(walker2)
    ##为汽车设置目的地
    destination = carla.Location(x=-5, y=170, z=0.5)
    agent = BasicAgent(vehicle1)
    agent.set_destination(destination)
    destination2 = carla.Location(x=5, y=110, z=0.5)
    agent2 = BasicAgent(vehicle3)
    agent2.set_destination(destination2)
    # 等待汽车到达目的地
    while True:
        vehicle_location = vehicle1.get_location()
        distance = vehicle_location.distance(destination)
        print('distance:',distance)
        vehicle_location2 = vehicle3.get_location()
        distance2 = vehicle_location2.distance(destination2)
        print('distance2:', distance2)
        if distance<1.5 or distance2 < 1.5:
            print(distance)
            print(distance2)
            break
        time.sleep(0.1)

    # 让汽车行驶一段时间
    # time.sleep(30)
    # actor_list.append(vehicle3)
    # 等待汽车行驶一段时间后结束程序

# except:
#     # 销毁所有生成的汽车
#     print('出现错误')
#     # 销毁所有生成的汽车
#     for actor in actor_list:
#         actor.destroy()
finally:
    # 销毁所有生成的汽车
    for actor in actor_list:
        actor.destroy()