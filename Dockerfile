FROM ros:jazzy-ros-base

RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-jazzy-webots-ros2-tesla \
    python3-pil \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*


# Automatically source ROS 2 in new Bash sessions
RUN echo "source /opt/ros/jazzy/setup.bash" >> /root/.bashrc

# Automatically source the SARA-2 workspace if it exists
RUN echo "[ -f /sara_ws/install/setup.bash ] && source /sara_ws/install/setup.bash" >> /root/.bashrc

WORKDIR /sara_ws

CMD ["bash"]