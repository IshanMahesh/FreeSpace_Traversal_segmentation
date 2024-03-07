import cv2
import numpy as np
import os
import glob


def normalize_depth_image(depth_image_path, output_image_path):

    depth_image = cv2.imread(depth_image_path, cv2.IMREAD_UNCHANGED)    
    normalized_image = cv2.normalize(depth_image, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)    
    scaled_image = (25565* normalized_image).astype(np.uint16)
    
    cv2.imwrite(output_image_path, scaled_image)

# Ruta al directorio que contiene las imágenes de profundidad
depth_images_directory = '/home/data/polytunnel_dataset/depth_images'

# Ruta al directorio donde se guardarán las imágenes de salida
output_directory = '/home/data/polytunnel_dataset/depth_images/dense_depth'
os.makedirs(output_directory, exist_ok=True)

# Obtener todos los archivos de imagen en el directorio
depth_image_paths = glob.glob(os.path.join(depth_images_directory, '*.png'))

# Procesar cada archivo de imagen de profundidad
for depth_image_path in depth_image_paths:
    filename = os.path.basename(depth_image_path)
    output_image_path = os.path.join(output_directory, filename)
    normalize_depth_image(depth_image_path, output_image_path)
    print("Procesado y guardado")


