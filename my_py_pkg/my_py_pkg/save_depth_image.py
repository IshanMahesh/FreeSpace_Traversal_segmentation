#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import numpy as np
import os
import cv2
from cv_bridge import CvBridge

class DepthImageSaver(Node):
    def __init__(self):
        super().__init__('depth_image_saver')
        self.subscription = self.create_subscription(Image,'/front_camera/depth/image_raw',self.image_callback,10)
        self.save_directory = '/home/data/unsynchronized_dataset/datasets/ORFD/testing/dense_depth'
        os.makedirs(self.save_directory, exist_ok=True)
        self.bridge = CvBridge()
        self.image_count = 0

    def image_callback(self, msg):
        print("Received a depth image!")




        #change the image from ROS to NumPy using CvBridge         
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
        if np.nanmax(cv_image) > 0:
            
            cv_image = np.nan_to_num(cv_image, nan=0.0)    
            
            normalized_image = cv2.normalize(cv_image, None, alpha=0, beta=65535, norm_type=cv2.NORM_MINMAX)
            normalized_image = normalized_image.astype(np.uint16)

            
            scaled_image = np.interp(normalized_image, (normalized_image.min(), normalized_image.max()), (0, 255))
            display_image = scaled_image.astype(np.uint8)

            
            file_path = os.path.join(self.save_directory, f'{self.image_count:04d}.png')
            cv2.imwrite(file_path, display_image)
            print("Saved depth image")

            self.image_count += 1
        else:
            print("Depth image contains no valid data (max value is 0 or NaN).")


        '''   
        np_image = np.array(cv_image, dtype=np.float32)

        normalized_image = cv2.normalize(np_image, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        scaled_image = (25565 * normalized_image).astype(np.uint16)




        #save the depth image as a .png file 
        file_path = os.path.join(self.save_directory, f'{self.image_count:04d}.png')

        cv2.imwrite(file_path, scaled_image)
        print("Saved depth image")        
        self.image_count += 1
        '''

def main(args=None):
    rclpy.init(args=args)
    depth_image_saver = DepthImageSaver()
    print("Save Depth Image Node Running...")
    rclpy.spin(depth_image_saver)
    
    depth_image_saver.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
