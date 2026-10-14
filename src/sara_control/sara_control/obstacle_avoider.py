import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from rclpy.qos import qos_profile_sensor_data

class ObstacleAvoider(Node):
    def __init__(self):
        super().__init__("obstacle_avoider")

        self.create_subscription = self.create_subscription(LaserScan, 'vehicle/lidar', self.lidar_callback, qos_profile_sensor_data)

    def lidar_callback(self, msg: LaserScan):
        self.get_logger().info("recieved")


def main(args=None):
    rclpy.init(args=args)
    obstacle_avoider = ObstacleAvoider()

    rclpy.spin(obstacle_avoider)

    obstacle_avoider.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()