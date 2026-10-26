from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='humanoid_bridge', executable='bridge',
             parameters=[{'viewer': True}]),
        Node(package='humanoid_bridge', executable='wave')])
