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


def on_collision(event):
    print('发生碰撞！')
    global collision_detected
    collision_detected = True
# 连接到CARLA服务器
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
# 获取世界对象和蓝图库
world = client.get_world()
blueprint_library = world.get_blueprint_library()
# 在世界中生成三辆汽车
vehicle_bp = blueprint_library.filter('vehicle.tesla.model3')[0]
vehicle_transform = carla.Transform(carla.Location(x=10, y=208, z=0.5), carla.Rotation(yaw=0))
vehicle1 = world.spawn_actor(vehicle_bp, vehicle_transform)
transform2 = carla.Transform(carla.Location(x=20, y=208, z=0.5), carla.Rotation(yaw=0))  ## 45 130
transform3 = carla.Transform(carla.Location(x=30, y=208, z=0.5), carla.Rotation(yaw=0))  ##20 127
vehicle2 = world.spawn_actor(vehicle_bp, transform2)
vehicle3 = world.spawn_actor(vehicle_bp, transform3)
transform4 = carla.Transform(carla.Location(x=38.5, y=208, z=0.5), carla.Rotation(yaw=0))  ##20 127
vehicle4 = world.spawn_actor(vehicle_bp, transform4)
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
vehicle3.set_autopilot(True)
# vehicle3.apply_control(carla.VehicleControl(throttle=0.8, steer=0.0))
# vehicle2.set_autopilot(True)
vehicle2.apply_control(carla.VehicleControl(throttle=0.3, steer=0.0))
# vehicle4.set_autopilot(True)
vehicle4.apply_control(carla.VehicleControl(throttle=0.3, steer=0.0))
# vehicle3.set_autopilot(True)
# 创建一个行为代理对象
agent = BasicAgent(vehicle2)


destination = carla.Location(x=90,y=208,z=0.500000)
agent.set_destination(destination)

while True:

    if agent.done():
        # 获取汽车当前速度
        velocity = vehicle1.get_velocity()
        print("达到目的地，停止运行")
        print(velocity)
        break

    control = agent.run_step(debug = True)
    vehicle2.apply_control(control)
    spectator = world.get_spectator()
    transform1 = vehicle2.get_transform()
    spectator.set_transform(carla.Transform(transform1.location + carla.Location(z=23.2),
                                            carla.Rotation(pitch=-90)))  # 设置跟随汽车视角
    world.tick()
    if collision_detected:
        break

collision_sensor.destroy()
for actor in actor_list:
    actor.destroy()
print("销毁完毕")

