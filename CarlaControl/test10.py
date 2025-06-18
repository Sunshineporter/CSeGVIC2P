import carla
import random
import time
import glob
import os
import sys
actor_list=[]


try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass



sys.path.append('D:\CARLA_0.9.10.1\WindowsNoEditor\PythonAPI\carla')
from agents.navigation.basic_agent import BasicAgent
from agents.navigation.behavior_agent import BehaviorAgent
import math
def has_obstacle_ahead(vehicle, distance_threshold=10):
    """
    判断车辆前方是否有障碍物
    Args:
        vehicle: Carla车辆对象
        distance_threshold: 距离阈值，小于该值则认为有障碍物
    Returns:
        True or False
    """
    # 获取当前世界中的所有车辆
    vehicle_list = vehicle.get_world().get_actors().filter('vehicle.*')
    # 获取当前车辆的位置和朝向
    location = vehicle.get_location()
    forward_vector = vehicle.get_transform().get_forward_vector()
    # 计算前方距离
    forward_distance = 10  # 假设前方10米
    forward_location = location + forward_distance * forward_vector
    # 判断前方是否有车辆
    for other_vehicle in vehicle_list:
        if other_vehicle.id != vehicle.id:
            other_location = other_vehicle.get_location()
            distance = math.sqrt((other_location.x - forward_location.x)**2
                                 + (other_location.y - forward_location.y)**2
                                 + (other_location.z - forward_location.z)**2)
            if distance < distance_threshold:
                return True
    return False
def on_collision(event):
    print('发生碰撞！')
    global collision_detected
    collision_detected = True
def turn_on_fog_lights(vehicle):
    """
    打开车辆雾灯
    Args:
        vehicle: Carla车辆对象
    """
    light_state = carla.VehicleLightState(carla.VehicleLightState.Position | carla.VehicleLightState.LowBeam | carla.VehicleLightState.Fog)
    vehicle.set_light_state(light_state)
# 连接到CARLA服务器
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
# 获取世界对象和蓝图库
world = client.get_world()
# 设置天气参数
weather = carla.WeatherParameters(
    cloudiness=80,
    precipitation=0.0,
    fog_density=70.0,
    fog_distance=25,
    sun_altitude_angle=80.0)
world.set_weather(weather)
map = world.get_map()
blueprint_library = world.get_blueprint_library()
# 在世界中生成三辆汽车
vehicle_bp = blueprint_library.filter('vehicle.tesla.model3')[0]
vehicle_transform = carla.Transform(carla.Location(x=10, y=208, z=0.5), carla.Rotation(yaw=0))
vehicle1 = world.spawn_actor(vehicle_bp, vehicle_transform)
transform2 = carla.Transform(carla.Location(x=20, y=208, z=0.5), carla.Rotation(yaw=0))  ## 45 130
transform3 = carla.Transform(carla.Location(x=30, y=208, z=0.5), carla.Rotation(yaw=0))  ##20 127
vehicle2 = world.spawn_actor(vehicle_bp, transform2)
vehicle3 = world.spawn_actor(vehicle_bp, transform3)
# transform4 = carla.Transform(carla.Location(x=38.5, y=208, z=0.5), carla.Rotation(yaw=0))  ##20 127
# vehicle4 = world.spawn_actor(vehicle_bp, transform4)
turn_on_fog_lights(vehicle1)
turn_on_fog_lights(vehicle2)
turn_on_fog_lights(vehicle3)
##待测车辆为中间车辆vehicle2

actor_list.append(vehicle1)
actor_list.append(vehicle2)
actor_list.append(vehicle3)
# 在世界中一个碰撞传感器
collision_sensor_bp = world.get_blueprint_library().find('sensor.other.collision')
collision_sensor_transform = carla.Transform(carla.Location(x=1.0, z=1.0))
collision_sensor = world.spawn_actor(collision_sensor_bp, collision_sensor_transform, attach_to=vehicle2)
# 注册碰撞回调函数
collision_detected = False
collision_sensor.listen(lambda event: on_collision(event))
# 激活汽车的自动驾驶模式
vehicle1.set_autopilot(True)
# vehicle3.set_autopilot(True)
vehicle3.apply_control(carla.VehicleControl(throttle=0.5, steer=0.0))
# vehicle2.set_autopilot(True)
vehicle2.apply_control(carla.VehicleControl(throttle=0.8, steer=0.0))
# vehicle4.set_autopilot(True)

# vehicle3.set_autopilot(True)
# 创建一个行为代理对象
agent = BehaviorAgent(vehicle2,behavior='normal')

destination = carla.Location(x=60,y=208,z=0.500000)
agent.set_destination(carla.Location(x=20, y=208, z=0.5),destination)

while True:
    spectator = world.get_spectator()
    transform1 = vehicle2.get_transform()
    spectator.set_transform(carla.Transform(transform1.location + carla.Location(z=20),
                                            carla.Rotation(pitch=-90)))  # 设置跟随汽车视角
    vehicle_location = vehicle2.get_location()
    distance = vehicle_location.distance(destination)
    print(distance)
    if distance < 10.0:

        # 获取汽车当前速度
        velocity = vehicle2.get_velocity()
        print("达到目的地，停止运行")
        print(velocity)
        break

    waypoint = map.get_waypoint(vehicle_location)
    # 获取路径上的车辆列表
    vehicle_list = world.get_actors().filter('vehicle.*')
    # 超车
    if has_obstacle_ahead(vehicle2):
        agent._overtake(vehicle_location, waypoint, vehicle_list)
        # 暂停一段时间
        time.sleep(3)


    # control = agent.run_step(debug = True)
    # vehicle2.apply_control(control)

    world.tick()
    if collision_detected:
        break

collision_sensor.destroy()
for actor in actor_list:
    actor.destroy()
print("销毁完毕")

