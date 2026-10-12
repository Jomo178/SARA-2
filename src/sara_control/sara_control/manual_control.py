import rclpy
from rclpy.node import Node
from ackermann_msgs.msg import AckermannDrive
import tty, termios, sys, select

class ManuelControl(Node):
    def __init__(self):
        super().__init__('drive_tesla')

        # Save original terminal settings
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)

        # Allow reading individual keypresses
        tty.setcbreak(self.fd)

        # Check for keyboard input every 0.05 seconds
        self.timer = self.create_timer(0.05, self.listen_key_press)

        self.__ackermann_publicher = self.create_publisher(AckermannDrive, 'cmd_ackermann', 1)

        self.__car = AckermannDrive()

    def handle_driving(self, key:str):
        speed = self.__car.speed
        steering_angle = self.__car.steering_angle

        if(key == "y"):
            speed = 0.0
            steering_angle = 0.0

        if(key == "w"):
            speed = speed + 1

        if(key == "s"):
            speed = speed - 1

        if(key == "a"):
            steering_angle = steering_angle + 0.05

        if(key == "d"):
            steering_angle = steering_angle - 0.05

        self.__car.speed = speed
        self.__car.steering_angle = steering_angle

        self.__ackermann_publicher.publish(self.__car)

    #cehck https://github.com/ros2/teleop_twist_keyboard/blob/jazzy/teleop_twist_keyboard.py#L180 for the key
    def listen_key_press(self):
        ready, _, _ = select.select([sys.stdin], [], [], 0)
  
        if ready:
                key = sys.stdin.read(1)
                self.handle_driving(key)
                # self.get_logger().info(f"Pressed: {key}")

def main(args=None):
    rclpy.init(args=args)
    drive_tesla = ManuelControl()

    try:
        rclpy.spin(drive_tesla)
    finally:
        termios.tcsetattr(
            drive_tesla.fd,
            termios.TCSADRAIN,
            drive_tesla.old_settings
        )

    drive_tesla.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()