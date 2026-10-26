import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

class Wave(Node):
    def __init__(self):
        super().__init__('supported_elbow_wave')
        self.pub = self.create_publisher(JointState, '/joint_targets', 1)
        self.names = None; self.home = None; self.start = None
        self.create_subscription(JointState, '/joint_states', self.receive, 10)
        self.create_timer(.02, self.tick)

    def receive(self, msg):
        if self.home is None:
            self.names = list(msg.name); self.home = list(msg.position)
            self.start = self.get_clock().now().nanoseconds*1e-9

    def tick(self):
        if self.home is None: return
        now = self.get_clock().now()
        t = now.nanoseconds*1e-9-self.start
        msg = JointState(); msg.header.stamp = now.to_msg()
        msg.name = self.names; msg.position = self.home.copy()
        j = self.names.index('left_elbow_joint')
        msg.position[j] += .05*(1-math.cos(2*math.pi*.25*t))
        self.pub.publish(msg)

def main():
    rclpy.init(); node = Wave()
    try: rclpy.spin(node)
    finally:
        node.destroy_node(); rclpy.shutdown()
