#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv_bridge
import cv2
import numpy as np
import os
import time

class RgbImageSaver(Node):
    def __init__(self):
        super().__init__('rgb_image_saver')
        self.bridge = cv_bridge.CvBridge()
        self.subscription = self.create_subscription(Image, '/front_camera/image_raw', self.image_callback, 10)
        #create directories
        self.save_directory_video = '/home/data/polytunnel_dataset/video_data'
        os.makedirs(self.save_directory_video, exist_ok=True)
        self.save_directory_image = '/home/data/polytunnel_dataset/image_data'
        os.makedirs(self.save_directory_image, exist_ok=True)
        self.save_directory_txt = '/home/data/polytunnel_dataset/calib'
        os.makedirs(self.save_directory_txt, exist_ok=True)

        self.video_writer = None    
        self.image_count = 0  

    def image_callback(self, msg):
        print("Received an image!")
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            
            if self.video_writer is None:
                self.init_video_writer(cv_image)
            self.video_writer.write(cv_image)
            
            # save image as a file 
            self.save_image(cv_image)
        except Exception as e:
            self.get_logger().error('Error processing image: %s' % str(e))

    def init_video_writer(self, image):
        try:
            height, width, _ = image.shape
            video_format = 'mp4'
            
            video_filename = self.save_directory_video +'/output_video.' + video_format
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            
            fps = 30  # Frames per second
            self.video_writer = cv2.VideoWriter(video_filename, fourcc, fps, (width, height))
        except Exception as e:
            self.get_logger().error('Error initializing video writer: %s' % str(e))

     

    def save_image(self, cv_image):
        image_path = os.path.join(self.save_directory_image, f'image_{self.image_count:04d}.png')
        cv2.imwrite(image_path, cv_image)
        self.image_count += 1
        self.create_txt_for_png(image_path)        
    
    def create_txt_for_png(self, image_path):
        txt_content = '''cam_K: 528.433756558705 0.0 320.5 0.0 528.433756558705 240.5 0.0 0.0 1.0 
cam_RT: 1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 1.0 
lidar_R: 1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 1.0
lidar_T: 0 0 0'''

        base_name = os.path.splitext(os.path.basename(image_path))[0]
        txt_file_path = os.path.join( self.save_directory_txt, f'{base_name}.txt')

        with open(txt_file_path, 'w') as txt_file:
            txt_file.write(txt_content)
        print(f'Archivo creado: {txt_file_path}')

        

    def destroy_node(self):
        print("Releasing VideoWrite")
        if self.video_writer is not None:
            self.video_writer.release()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    image_to_video_converter = RgbImageSaver()
    print("Save Rgb Image Rode Running...")
    
    rclpy.spin(image_to_video_converter)
    image_to_video_converter.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()