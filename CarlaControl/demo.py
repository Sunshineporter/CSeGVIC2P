import time

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
    client = carla.Client('localhost',2000)
    client.set_timeout(10)
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()
    ego_bp = blueprint_library.filter("model3")[0]  #创建汽车
    blueprintsWalkers = blueprint_library.filter("walker.pedestrian.*")
    # 创建行人
    walker_bp = random.choice(blueprintsWalkers)
    weather = carla.WeatherParameters(
        cloudiness=60,
        precipitation=100.0,
        precipitation_deposits=70.0,
        sun_altitude_angle=20.0)
    world.set_weather(weather)  #设置天气
    location2 = carla.Location(x=98, y=40, z=0.600000)
    rotation2 = carla.Rotation(pitch=0.000000, yaw=-179.840790, roll=0.000000)
    transform2 = carla.Transform(location2,rotation2)       #位置参数
    spawn_point = world.get_map().get_spawn_points()
    walker = world.spawn_actor(walker_bp, transform2)       #行人的位置
    # 创建用于控制行人的Ai
    walker_controller_bp = world.get_blueprint_library().find('controller.ai.walker')
    walker_controller = world.spawn_actor(walker_controller_bp, transform2, walker)
    # 开启控制
    walker_controller.start()
    walker_controller.go_to_location(carla.Location(x=120, y=40, z=0.600000))   #设置行人目的地
    walker_controller.set_max_speed(1 + random.random())  # Between 1 and 2 m/s (default is 1.4 m/s).
    # random.choice(spawn_point)
    # traffic_light = world.get_map().get_traffic()
    # f1 = open("traffic_light.txt", "w")
    # for line in traffic_light:
    #     f1.write(str(line) + '\n')
    # f1.close()

    # ego_bp2 = blueprint_library.filter("vehicle")[0]  # 创建汽车2
    # location3 = carla.Location(x=130, y=67, z=0.600000)
    # rotation3 = carla.Rotation(pitch=0.000000, yaw=0, roll=0.000000)
    # transform3 = carla.Transform(location3, rotation3)
    # vehicle2 = world.spawn_actor(ego_bp2, transform3)
    # agent2 = BasicAgent(vehicle2)
    # agent2.set_destination(carla.Location(x=60, y=16.905891, z=0.600000))


    # location2 = carla.Location(x=62.025547, y=16.905891, z=0.600000)
    # rotation2 = carla.Rotation(pitch=0.000000, yaw=-179.840790, roll=0.000000)
    location = carla.Location(x=106, y=67, z=0.600000)
    rotation = carla.Rotation(pitch=0.000000, yaw=0, roll=0.000000)
    # transform2 = carla.Transform(location2,rotation2)
    transform = carla.Transform(location, rotation)
    vehicle = world.spawn_actor(ego_bp,transform)
    # ego_vehicle.set_autopilot(True)
    # 当有仿真世界有actor产生或者有改变是需要及时的更新，此时tick()就是这个作用。
    world.tick()
    # 使用agent里面的BehaviorAgent类，该类主要是设置自己控制的agent的行为模式，主要有三种
    agent = BasicAgent(vehicle)             #开启自动驾驶
    # 路径规划的核心代码
    # print(123)
    # aa=carla.Location(x=62.025547,y=16.905891,z=0.600000)
    # print(aa.x)
    agent.set_destination(carla.Location(x=62.025547,y=16.905891,z=0.600000))

    # vehicle.apply_control(carla.VehicleControl(throttle=0.0, steer=0.0))
    actor_list.append(walker)
    actor_list.append(vehicle)
    # actor_list.append(vehicle2)
    # actor_list1 = world.get_actors()
    # for traffic_light in actor_list1.filter('traffic.traffic_light'):
    #     print("actor_id",traffic_light.id,"{}".format(traffic_light.get_transform()))
    # while True:
    # spectator = world.get_spectator()
    # transform = vehicle.get_transform()
    # spectator.set_transform(carla.Transform(transform.location + carla.Location(z=50),
    #                                         carla.Rotation(pitch=-90)))
    if vehicle.is_at_traffic_light():       #如果是红灯就设置为绿灯
        traffic_light = vehicle.get_traffic_light()
        if traffic_light.get_state() == carla.TrafficLightState.Red:
            # world.hud.notification("Traffic light changed! Good to go!")
            traffic_light.set_state(carla.TrafficLightState.Green)
        print(traffic_light)
        print(123456)

    # time.sleep(10)

    while True:
        spectator = world.get_spectator()
        transform1 = vehicle.get_transform()
        spectator.set_transform(carla.Transform(transform1.location + carla.Location(z=40),
                                                carla.Rotation(pitch=-90))) #设置跟随汽车视角
        if agent.done():            #判断是否到终点
            print("The target has been reached, stopping the simulation")
            break
        control = agent.run_step()
        vehicle.apply_control(control)


finally:
    walker_controller.stop()
    for actor in actor_list:
        actor.destroy()
    print("ALL clean up!")



