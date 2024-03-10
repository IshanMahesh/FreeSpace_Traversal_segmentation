from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()

    rgb_subscriber_node = Node(
        package= "my_py_pkg",
        executable="save_rgb_image"
    )
    pointCloud_subscriber_node = Node(
        package="my_py_pkg",
        executable="save_point_Cloud"
    )
    depthImage_subscriber_node = Node(
        package="my_py_pkg",
        executable="save_depth_image"
    )
    ld.add_action(rgb_subscriber_node)
    ld.add_action(pointCloud_subscriber_node)
    ld.add_action(depthImage_subscriber_node)
    
    return ld