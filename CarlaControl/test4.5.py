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
def turn_on_fog_lights(vehicle):
    """
    打开车辆雾灯
    Args:
        vehicle: Carla车辆对象
    """
    light_state = carla.VehicleLightState(carla.VehicleLightState.Position | carla.VehicleLightState.LowBeam | carla.VehicleLightState.Fog)
    vehicle.set_light_state(light_state)
def set_traffic_light_color(traffic_light, color):
    """
    修改交通信号灯的颜色
    Args:
        traffic_light: Carla交通信号灯对象
        color: 要设置的颜色，可以是"Red"、"Yellow"或"Green"
    """
    if color == "Red":
        traffic_light.set_state(carla.TrafficLightState.Red)
    elif color == "Yellow":
        traffic_light.set_state(carla.TrafficLightState.Yellow)
    elif color == "Green":
        traffic_light.set_state(carla.TrafficLightState.Green)
def get_traffic_light_color(vehicle):
    """
    获取待测车辆前方的红绿灯颜色
    Args:
        vehicle: Carla车辆对象
    Returns:
        color: 红绿灯颜色，可以是"Red"、"Yellow"或"Green"
    """
    traffic_light = vehicle.get_traffic_light()
    if traffic_light is not None:
        state = traffic_light.get_state()
        if state == carla.TrafficLightState.Red:
            color = "Red"
        elif state == carla.TrafficLightState.Yellow:
            color = "Yellow"
        elif state == carla.TrafficLightState.Green:
            color = "Green"
        else:
            color = "Unknown"
    else:
        color = "None"
    return color
# 连接到CARLA服务器
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
# 获取世界对象和蓝图库
world = client.get_world()
# 设置天气参数
weather = carla.WeatherParameters(
    cloudiness=80,
    precipitation=0.0,
    fog_density=0.0,
    fog_distance=0,
    sun_altitude_angle=80.0)
world.set_weather(weather)
blueprint_library = world.get_blueprint_library()
# 筛选出一辆小型汽车蓝图
blueprint = blueprint_library.filter('vehicle.tesla.model3')[0]
blueprint2 = blueprint_library.filter('model3')[0]
# 筛选出一个行人蓝图
walker_blueprint = blueprint_library.filter('walker.pedestrian.0001')[0]
# 设置汽车的初始位置和朝向
transform1 = carla.Transform(carla.Location(x=43, y=130, z=0.5), carla.Rotation(yaw=-180))
transform2 = carla.Transform(carla.Location(x=20, y=130, z=0.5), carla.Rotation(yaw=-180))## 45 130
transform3 = carla.Transform(carla.Location(x=20, y=127, z=0.5), carla.Rotation(yaw=-180))  ##20 127
# 设置行人的初始位置和朝向
walker_transform1 = carla.Transform(carla.Location(x=-5, y=125, z=0.5), carla.Rotation(yaw=-90))
walker_transform2 = carla.Transform(carla.Location(x=-5, y=140, z=0.5), carla.Rotation(yaw=-90))
# 在世界中生成三辆汽车
vehicle1 = world.spawn_actor(blueprint, transform1)
vehicle2 = world.spawn_actor(blueprint2, transform2)
vehicle3 = world.spawn_actor(blueprint2, transform3)
# 在世界中生成两个行人
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
walker_controller1.set_max_speed(1.1)  # Between 1 and 2 m/s (default is 1.4 m/s).
# 开启控制
walker_controller2.start()
walker_controller2.go_to_location(carla.Location(x=12, y=98, z=0.500000))  # 设置行人目的地
walker_controller2.set_max_speed(1.1)  # Between 1 and 2 m/s (default is 1.4 m/s).

# 激活汽车的自动驾驶模式
vehicle1.set_autopilot(True)
vehicle2.set_autopilot(True)
vehicle3.set_autopilot(True)



actor_list.append(vehicle1)
actor_list.append(vehicle2)
actor_list.append(vehicle3)
actor_list.append(walker1)
actor_list.append(walker2)
# 创建一个行为代理对象
agent = BasicAgent(vehicle1)

agent.set_destination(carla.Location(x=-5,y=160,z=0.500000))





while True:

    if agent.done():
        print("The target has been reached, stopping the simulation")
        break
    control = agent.run_step(debug = True)
    vehicle1.apply_control(control)
    spectator = world.get_spectator()
    transform1 = vehicle1.get_transform()
    spectator.set_transform(carla.Transform(transform1.location + carla.Location(z=23.565),
                                            carla.Rotation(pitch=-90)))  # 设置跟随汽车视角
    # if get_traffic_light_color(vehicle2) == "Green":
    #     set_traffic_light_color(vehicle2.get_traffic_light(),"Red")
# actor_list = world.get_actors().filter('vehicle*') + world.get_actors().filter('walker*')


for actor in actor_list:
    actor.destroy()
print("销毁完毕")