import rclpy 
from rclpy.node import Node
from ackermann_msgs.msg import AckermannDrive
from nav_msgs.msg import Odometry as OdometryMsg
import numpy as np 
import math

class Odometry(Node):
    def __init__(self):
        super().__init__("odometry")

        self.declare_parameter('wheel_base', 2.94)
        self.velocity = 0
        self.delta = 0.0
        self.q = np.array([-11.9883,-12.1427,0.0]) 
        
        self.subscription = self.create_subscription(AckermannDrive, 'cmd_ackermann', self.ackermann_callback, 1)
        self.odom_publisher = self.create_publisher(OdometryMsg, '/odom', 10)

        self.last_update_time = None

        self.timer = self.create_timer(0.1, self.timer_callback)


    def timer_callback(self):
        now = self.get_clock().now()
        if self.last_update_time is None:
            self.last_update_time = now
            return

        dt = (now - self.last_update_time).nanoseconds / 1e9

        self.last_update_time = now
        
        wheel_base = self.get_parameter('wheel_base').value
        self.q = self.update_state(self.q, self.velocity, self.delta, wheel_base, dt)

        self.get_logger().info(f"Estimated position: {self.q}")

    def ackermann_callback(self, msg:AckermannDrive):
        # TODO: need to change because webot uses km/h and not m/s
        self.velocity = msg.speed / 3.6
        self.delta = msg.steering_angle
            

    def update_state(self, q, v, delta, L, dt):
        x, y, theta = q

        return np.array([
            x + v * math.cos(theta) * dt,
            y + v * math.sin(theta) * dt,
            theta + (v / L) * math.tan(delta) * dt
        ])


def main(args=None):
    rclpy.init(args=args)
    odometry = Odometry()
    rclpy.spin(odometry)

    odometry.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
