from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    usb_cam_dir      = get_package_share_directory('usb_cam')
    velodyne_driver_dir  = get_package_share_directory('velodyne_driver')
    velodyne_pointcloud_dir  = get_package_share_directory('velodyne_pointcloud')
    sensor_init_dir = get_package_share_directory('sensor_initialize')
    fusion_pkg_dir = get_package_share_directory('sensor_fusion_pkg')
    info_pkg_dir = get_package_share_directory('info_publisher_pkg')

    return LaunchDescription([
        # 1) 다중 카메라 센서 초기화.
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(usb_cam_dir, 'launch', 'multiple_camera.launch.py')
            )
        ),
        # 2) 벨로다인 드라이버 런치.
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(velodyne_driver_dir, 'launch', 'velodyne_driver_node-VLP16-launch.py')
            )
        ),
        # 3) 벨로다인 데이터 변환.
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(velodyne_pointcloud_dir, 'launch', 'velodyne_transform_node-VLP16-launch.py')
            )
        ),
        # 4) UM7 센서 초기화.
        Node(
            package='umx_driver',
            executable='um7_driver',
            name='um7_driver',
            output='screen',
        ),
        # 5) TF 브로드캐스트 (카메라 ⇆ LiDAR)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(sensor_init_dir, 'launch', 'sensor_tf.launch.py')
            )
        ),
        # 6) LiDAR 전처리
        Node(
            package='sensor_initialize',
            executable='lidar_preprocessing_node',
            name='lidar_preprocessor',
            output='screen',
            parameters=[{
                # 필요하면 파라미터 여기
            }]
        ),
        # 7) LiDAR-카메라 Fusion (멀티 실행)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(fusion_pkg_dir, 'launch', 'fusion_multi.launch.py')
            )
        ),
        # 8) info 퍼블리셔 런치
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(info_pkg_dir, 'launch', 'info_publisher.launch.py')
            )
        ),
        # 9) 라바콘 경로 생성기
        Node(
            package="track_driving_pkg",
            executable="waypoint_extractor_node",
            name="waypoint_extractor_node",
            output="screen"
        ),
        # 10) erp 42 제어 로직 관련 코드
        Node(
            package="track_driving_pkg",
            executable="erp42_control_node",
            name="erp42_control_node",
            output="screen"
        ),
        # N) ERP42 제어 관련 노드 실행.
        Node(
            package='erp42_control',
            executable='ErpSerialHandler_node',
            name='ErpSerialHandler_node',
            output='screen',
        ),
    ])