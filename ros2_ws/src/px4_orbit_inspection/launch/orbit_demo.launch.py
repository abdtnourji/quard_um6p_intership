from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    share = get_package_share_directory('px4_orbit_inspection')
    parameters = os.path.join(share, 'config', 'mission.yaml')
    return LaunchDescription([
        Node(package='px4_orbit_inspection', executable='orbit_controller',
             name='orbit_controller', parameters=[parameters], output='screen'),
        Node(package='px4_orbit_inspection', executable='mission_monitor',
             name='mission_monitor', output='screen'),
    ])
