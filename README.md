# free_space_segmentation
The project is founded on the precedent set by the following project ["ORFD: Off-Road-Freespace-Detection
"](https://github.com/chaytonmin/Off-Road-Freespace-Detection/tree/main).











## Introduction

The ORFD project is resumed para probar its implementation in the detection of paths in polytunnels de dicados a la cosecha de fresa. The repository with modifications to the original code is located at: [Off-road-detection](https://github.com/adri-gth/Off-road-detection/tree/main), el dataset generado cuenta con un total de 34,684 datos y se ncuentra disponible en (polytunnel_dataset)[https://drive.google.com/file/d/1egS08WVoOzbN0vwSiknT8DT6aaipX_3V/view?usp=sharing]

El proyecto se divide en 3 secciones:

Colectar datos 

generacion de un politunel_dataset 

prueba del modelo OFF-Net entrenado con el dataset de ORFD



the 'Free space segmentation' folder es el paquete genrado para la extraccion de infromacion de los bagfiles,  The 'docker' folder contains a shell file el cual se explica su uso mas adelante y en 
el folder 'python_code' se encuentra el codigo para extraer el gt_image. 




### Preparacion del entrono de trabajo 

#### Instruction for running the docker image

 The 'docker' folder contains a shell file. This file must be downloaded to the host and executed using the following commands:
 
 To start the container for the first time, execute the following command:
 
     cd <the directory where the 'obs_detect.sh' file is located>
     ./obs_detect.sh run
     
This command sets up and runs a new container using the 'adriavdocker/obsdetection:v2' image 

To start the container that has already been created: 

    ./obs_detect.sh start
    
To enter the container after it has been started

    ./obs_detect.sh enter
    
To stop the container 

    ./obs_detect.sh stop
    
Additional Notes: Ensure that the 'obs_detect.sh' script has execute permissions. If it does not, you can grant execute permissions using the following command:

    chmod +x obs_detect.sh







## Colectando datos  

### indicaciones fisicas de como se colocaro los sensores en el robot para colectar los datos 

para colectar datos se fijan dos sensores a una estructura ubicada sobre un [Hunter 2.0](https://docs.trossenrobotics.com/agilex_hunter_20_docs/), el primer es
un LiDAR [LIVOX-MID360](https://www.livoxtech.com/mid-360) y [ZED 2 Stereo Camera](https://store.stereolabs.com/en-gb/products/zed-2), estos sensores ubicados uno sobre el otro, como se muestra en el diagrama sigueinte: 

```
                                                                    _____LiDAR______
2.25 ft----------------- Camera height------------------------------__depth_camera__
  |                                                                        |         
  |                                                                        |
  |                                                                        |
1.2 ft----------------- Hunter's max height--------------------------------|
  |                                                                        |
  |                                                                        |
  |                                                                        |
  |                                                                        |
Floor______________________________________________________________________|____________________________________________
```


### Extracting Depth images, RGB images and point clouds from a ROS2 topic in a synchronized manner.

To obtain information in a synchronized manner (for the ORFD project, this is mandatory), the data_synchronizer node should be executed:
 
    ros2 run free_space_segmentation sync_node 

The root path where the information is stored is:

- '/home/data/synchronized_dataset/datasets/ORFD/testing/sequence/****'

The folders created to store the information are:

    rgb_image: image_data 
    point Cloud: lidar_data 
    calib: calib 
    depth_image: dense_depth 

    
si no se re quiere extraer la infromacion de una manera sincronizada, entonces: 


para extraer unicamente rgb_image se debe ejecutar el sigueinte comando 

    ros2 run free_space_segmentation save_rgb_image

este comando almacena las imagenes rgb y los datos de calibracion de la capara y sensor lidar

The root path where the information is stored is:
    /home/data/unsynchronized_dataset/datasets/ORFD/testing/image_data
    /home/data/unsynchronized_dataset/datasets/ORFD/testing/calib'




para extraer unicamente nueve de putos se debe ejecutar el sigueinte comando

     ros2 run free_space_segmentation save_point_Cloud 

este comando almecena la nueve de puntos generada por el sensor lidar como un archivo .bin 

The root path where the information is stored is:

'/home/data/unsynchronized_dataset/datasets/ORFD/testing/sequence/lidar_data'





para estraer unicamente las imagens de profundidad se debe ejecutar el sigueinte comando

      ros2 run free_space_segmentation save_depth_image 


The root path where the information is stored is:
     '/home/data/unsynchronized_dataset/datasets/ORFD/testing/sequence/dense_depth'









### Instructions for creating a training dataset

With the folders generated previously, the only thing left to do is to generate gt_image. To accomplish this, the [Supervisely](https://supervisely.com/) platform is used.

To generate the ground truth image data:

1. The 'image_data' folder, generated by the sync_node , is uploaded to it.

2. In the platform Supervisely, the 'road' class is created, applicable to 'any shape', which enables the segmentation of paths.

3. After the segmentation is applied to the data, the project is downloaded and exported using the 'Export to Supervisely Format' option, retaining only the .json annotations.
    
4. Subsequently, in the 'python_code' folder, there is an 'extract_mask.py' script. In this script, the path to the file downloaded from Supervisely, the name of that file, and the folder in which the mask will be extracted need to be updated. The script creates the 'gt_image' folder.


The folders 'lidar_data', 'dense_depth', 'image_data', 'calib', and 'gt_image' are already available. They should be organized in the following manner:

```
|-- datasets
 |  |-- ORFD
 |  |  |-- training
 |  |  |  |-- sequence   |-- calib
 |  |  |                 |-- sparse_depth
 |  |  |                 |-- dense_depth
 |  |  |                 |-- lidar_data
 |  |  |                 |-- image_data
 |  |  |                 |-- gt_image
 ......
 |  |  |-- validation
 ......
 |  |  |-- testing
 ......
```
The location of 'datasets', which is the folder containing all the information, must be the same as the path for 'test.sh' and 'train.sh' so that the program can access the information.




























