#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from message_filters import ApproximateTimeSynchronizer, Subscriber
from sensor_msgs.msg import Image, PointCloud2
import cv2
import numpy as np
import os
from cv_bridge import CvBridge
from sensor_msgs_py import point_cloud2

class DataSynchronizer(Node):
    def __init__(self):
        super().__init__('data_synchronizer')
        self.bridge = CvBridge()
        
        # Directorios para guardar datos sincronizados
        self.save_directory_depth = '/home/data/synchronized_dataset/datasets/ORFD/testing/sequence/dense_depth'
        self.save_directory_image = '/home/data/synchronized_dataset/datasets/ORFD/testing/sequence/image_data'
        self.save_directory_point_cloud = '/home/data/synchronized_dataset/datasets/ORFD/testing/sequence/lidar_data'
        self.save_directory_txt = '/home/data/synchronized_dataset/datasets/ORFD/testing/sequence/calib'

        for dir in [self.save_directory_depth, self.save_directory_image, self.save_directory_point_cloud,self.save_directory_txt]:
            os.makedirs(dir, exist_ok=True)

        self.depth_sub = Subscriber(self, Image, '/front_camera/depth/image_raw')
        self.image_sub = Subscriber(self, Image, '/front_camera/image_raw')
        self.point_cloud_sub = Subscriber(self, PointCloud2, '/front_camera/points')

        self.ats = ApproximateTimeSynchronizer([self.depth_sub, self.image_sub, self.point_cloud_sub], queue_size=10, slop=0.1)
        self.ats.registerCallback(self.sync_callback)

        self.data_count = 0

    def sync_callback(self, depth_msg, image_msg, point_cloud_msg):
        print("Received synchronized data")

        # Save image as a .png file 
        cv_image_r= self.bridge.imgmsg_to_cv2(image_msg, "bgr8")        
        self.save_image(cv_image_r)



        # save depth image 
        cv_image_d = self.bridge.imgmsg_to_cv2(depth_msg,desired_encoding='passthrough')
        self.save_depth_image(cv_image_d)



        # save point cloud as a .bin file 
        points_list = list(point_cloud2.read_points(point_cloud_msg, field_names=("x", "y", "z"), skip_nans=True))
        if not points_list:
            self.get_logger().error('Received an empty point cloud.')
            return
        np_points = np.array(points_list, dtype=np.float32)

        point_cloud_path = os.path.join(self.save_directory_point_cloud, f'{self.data_count:04d}.bin')
        np_points.tofile(point_cloud_path)

        self.data_count += 1

    def save_image(self, cv_image):
        image_path = os.path.join(self.save_directory_image,f'{self.data_count:04d}.png')
        cv2.imwrite(image_path,cv_image)
        self.create_txt(image_path)

    def create_txt(self,image_path):
        txt_content = '''cam_K: 528.433756558705 0.0 320.5 0.0 528.433756558705 240.5 0.0 0.0 1.0 
cam_RT: 1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 1.0 
lidar_R: 1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 1.0
lidar_T: 0 0 0'''
        base_name  = os.path.splitext(os.path.basename(image_path))[0]
        txt_file_path = os.path.join(self.save_directory_txt,f'{base_name}.txt')

        with open(txt_file_path,'w') as txt_file:
            txt_file.write(txt_content)

    def save_depth_image(self,cv_image):
        if np.nanmax(cv_image) > 0:
            
            cv_image = np.nan_to_num(cv_image, nan=0.0)    
            
            normalized_image = cv2.normalize(cv_image, None, alpha=0, beta=65535, norm_type=cv2.NORM_MINMAX)
            normalized_image = normalized_image.astype(np.uint16)

            
            scaled_image = np.interp(normalized_image, (normalized_image.min(), normalized_image.max()), (0, 255))
            display_image = scaled_image.astype(np.uint8)

            
            file_path = os.path.join(self.save_directory_depth, f'{self.data_count:04d}.png')
            cv2.imwrite(file_path, display_image)
        else:
            print("Depth image contains no valid data (max value is 0 or NaN).")



def main(args=None):
    rclpy.init(args=args)
    synchronizer = DataSynchronizer()
    print("Sync Node Running...")
    rclpy.spin(synchronizer)    
    synchronizer.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
