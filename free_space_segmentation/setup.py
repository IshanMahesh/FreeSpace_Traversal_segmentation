from setuptools import setup

package_name = 'free_space_segmentation'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='aldoadrian050301@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "save_rgb_image    = free_space_segmentation.saveImage:main",
            "save_point_Cloud  = free_space_segmentation.savePointCloud:main",
            "save_depth_image  = free_space_segmentation.save_depth_image:main",
            "sync_node         = free_space_segmentation.synchronizer_node:main"
        ],
    },
)
