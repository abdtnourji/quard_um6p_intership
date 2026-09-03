"""Small terminal monitor. It makes the classroom demo easier to follow."""
import math
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from px4_msgs.msg import VehicleOdometry, VehicleStatus


class MissionMonitor(Node):
    def __init__(self):
        super().__init__('mission_monitor')
        qos=QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST, depth=1)
        self.position=None; self.velocity=None; self.status=None
        self.create_subscription(VehicleOdometry,'/fmu/out/vehicle_odometry',self._odom,qos)
        self.create_subscription(VehicleStatus,'/fmu/out/vehicle_status',self._status,qos)
        self.create_timer(1.0,self._print)
    def _odom(self,m): self.position=tuple(m.position); self.velocity=tuple(m.velocity)
    def _status(self,m): self.status=m
    def _print(self):
        if not self.position: self.get_logger().info('Waiting for PX4 odometry...'); return
        speed=math.sqrt(sum(float(v)**2 for v in self.velocity))
        altitude=-float(self.position[2])
        nav=getattr(self.status,'nav_state','?') if self.status else '?'
        arm=getattr(self.status,'arming_state','?') if self.status else '?'
        self.get_logger().info(f'LIVE | altitude={altitude:5.2f} m | speed={speed:4.2f} m/s | nav={nav} | arm={arm}')


def main(args=None):
    rclpy.init(args=args); n=MissionMonitor()
    try: rclpy.spin(n)
    except KeyboardInterrupt: pass
    finally: n.destroy_node(); rclpy.shutdown()
