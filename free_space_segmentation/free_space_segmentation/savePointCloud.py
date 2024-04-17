#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
import numpy as np
import os
from sensor_msgs_py import point_cloud2 

class PointCloudSaver(Node):
    def __init__(self):
        super().__init__('point_cloud_saver')
        self.subscription = self.create_subscription(PointCloud2,'/livox/lidar',self.point_cloud_callback,10)
        self.save_directory = '/home/data/unsynchronized_dataset/datasets/ORFD/testing/sequence/lidar_data'
        os.makedirs(self.save_directory, exist_ok=True)
        self.point_cloud_count = 0

    def point_cloud_callback(self, msg):
        print("Received a point cloud!")        
        points_list = list(point_cloud2.read_points(msg, field_names=("x", "y", "z"), skip_nans=True))
        if not points_list:
            self.get_logger().error('Received an empty point cloud.')
            return
        np_points = np.array(points_list, dtype=np.float32)  # use float32 for compatibility.         
        # save the point cloud as a .bin file
        file_path = os.path.join(self.save_directory, f'{self.point_cloud_count:04d}.bin')
        np_points.tofile(file_path)
        print("saved data as a .bin file...")
        
        
        self.point_cloud_count += 1

def main(args=None):
    rclpy.init(args=args)
    point_cloud_saver = PointCloudSaver()
    print("Save Point Cloud Node Running...")
    rclpy.spin(point_cloud_saver)
    
    point_cloud_saver.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
