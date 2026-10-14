import os
import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from ament_index_python import get_package_share_directory
from launch.substitutions import LaunchConfiguration
from launch.substitutions.path_join_substitution import PathJoinSubstitution
from launch_ros.actions import Node
from webots_ros2_driver.webots_launcher import WebotsLauncher
from webots_ros2_driver.webots_controller import WebotsController


def generate_launch_description():
    package_dir = get_package_share_directory('webots_ros2_tesla')
    world = LaunchConfiguration('world')

    webots = WebotsLauncher(
        world=PathJoinSubstitution(['/sara_ws/worlds', world]),
        ros2_supervisor=True
    )

    robot_description_path = os.path.join(package_dir, 'resource', 'tesla_webots.urdf')
    tesla_driver = WebotsController(
        robot_name='vehicle',
        parameters=[
            {'robot_description': robot_description_path}
        ],
        respawn=True
    )
    odometry_node = Node(
        package='sara_control',
        executable='odometry',
        #use webots time
        parameters=[{'use_sim_time': True}]
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'world',
            default_value='floor.wbt',
            description='Choose a world'
        ),
        webots,
        webots._supervisor,
        tesla_driver,
        odometry_node,        

        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=webots,
                on_exit=[
                    launch.actions.EmitEvent(event=launch.events.Shutdown())
                ]
            )
        )
    ])