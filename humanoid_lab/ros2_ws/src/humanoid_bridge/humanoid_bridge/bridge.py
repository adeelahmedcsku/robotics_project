import os
import sys
import time
sys.path.insert(0, os.environ['HUMANOID_LAB_ROOT'])
import mujoco as mj
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from model import load, addresses, names, command

class Bridge(Node):
    def __init__(self):
        super().__init__('asimov_simulation')
        self.m, self.d = load()
        _, self.qi, self.vi = addresses(self.m)
        self.joints = names(self.m)
        self.home = self.d.qpos[self.qi].copy()
        self.target = self.home.copy()
        self.last = -np.inf
        self.pub = self.create_publisher(JointState, '/joint_states', 10)
        self.create_subscription(JointState, '/joint_targets', self.receive, 10)
        self.viewer = None
        if self.declare_parameter('viewer', False).value:
            import mujoco.viewer
            self.viewer = mujoco.viewer.launch_passive(self.m, self.d)
            self.viewer.cam.distance = 2.2
            self.viewer.cam.lookat[:] = [0, 0, .65]
        self.create_timer(.01, self.tick)

    def receive(self, msg):
        stamp = msg.header.stamp.sec+msg.header.stamp.nanosec*1e-9
        age = self.get_clock().now().nanoseconds*1e-9-stamp
        if msg.name != self.joints or len(msg.position) != self.m.nu:
            self.get_logger().warning('Rejected names or shape'); return
        if not 0 <= age <= .1 or not np.isfinite(msg.position).all():
            self.get_logger().warning('Rejected stale/nonfinite command'); return
        self.target = np.array(msg.position)
        self.last = time.monotonic()

    def tick(self):
        # Simulation fallback only. A physical machine needs a rig-specific stop.
        target = self.target if time.monotonic()-self.last < .1 else self.home
        for _ in range(5):
            command(self.m, self.d, target); mj.mj_step(self.m, self.d)
        msg = JointState(); msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joints
        msg.position = self.d.qpos[self.qi].tolist()
        msg.velocity = self.d.qvel[self.vi].tolist()
        msg.effort = self.d.actuator_force.tolist()
        self.pub.publish(msg)
        if self.viewer:
            self.viewer.sync()


def main():
    rclpy.init(); node = Bridge()
    try:
        rclpy.spin(node)
    finally:
        if node.viewer: node.viewer.close()
        node.destroy_node(); rclpy.shutdown()
