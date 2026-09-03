"""PX4 offboard mission: climb, approach, inspect by orbiting, hold, and land.

The code is split into a state machine so beginner students can map each block
of software to one visible phase in Gazebo. It sends PX4 NED position setpoints.
Run in SITL first. Real flight requires a separate safety review and operator.
"""
import math
from enum import Enum, auto
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from std_srvs.srv import Trigger
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path
from visualization_msgs.msg import Marker
from px4_msgs.msg import OffboardControlMode, TrajectorySetpoint, VehicleCommand, VehicleOdometry
from .trajectory import smoothstep, orbit_point, inward_yaw, tracking_error


class State(Enum):
    WAITING = auto(); WARMUP = auto(); CLIMB = auto(); APPROACH = auto()
    ORBIT = auto(); HOLD = auto(); LANDING = auto(); FINISHED = auto()


class OrbitController(Node):
    def __init__(self):
        super().__init__('orbit_controller')
        defaults = {
            'center_north_m': 0.0, 'center_east_m': 0.0, 'altitude_m': 4.0,
            'radius_m': 5.0, 'orbit_period_s': 24.0, 'number_of_laps': 1.25,
            'climb_time_s': 6.0, 'approach_time_s': 5.0, 'final_hold_s': 3.0,
            'setpoint_rate_hz': 20.0, 'face_center': True, 'auto_start': False,
            'auto_land': True, 'max_radius_m': 12.0, 'max_altitude_m': 10.0}
        for name, value in defaults.items(): self.declare_parameter(name, value)
        self.p = {name: self.get_parameter(name).value for name in defaults}
        self._validate()

        sensor_qos = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST, depth=1)
        self.heartbeat_pub = self.create_publisher(OffboardControlMode, '/fmu/in/offboard_control_mode', 10)
        self.setpoint_pub = self.create_publisher(TrajectorySetpoint, '/fmu/in/trajectory_setpoint', 10)
        self.command_pub = self.create_publisher(VehicleCommand, '/fmu/in/vehicle_command', 10)
        self.odom_sub = self.create_subscription(VehicleOdometry, '/fmu/out/vehicle_odometry', self._odom, sensor_qos)
        self.desired_path_pub = self.create_publisher(Path, '/orbit/desired_path', 10)
        self.measured_path_pub = self.create_publisher(Path, '/orbit/measured_path', 10)
        self.target_pub = self.create_publisher(Marker, '/orbit/inspection_target', 10)
        self.start_srv = self.create_service(Trigger, '/orbit/start', self._start)
        self.abort_srv = self.create_service(Trigger, '/orbit/abort', self._abort)

        self.state = State.WAITING
        self.state_t0 = self._now()
        self.warmup_ticks = 0
        self.measured = None
        self.desired = (0.0, 0.0, 0.0)
        self.desired_path = Path(); self.desired_path.header.frame_id = 'map'
        self.measured_path = Path(); self.measured_path.header.frame_id = 'map'
        self.timer = self.create_timer(1.0 / float(self.p['setpoint_rate_hz']), self._tick)
        self.get_logger().info('Mission ready. Start: ros2 service call /orbit/start std_srvs/srv/Trigger {}')

    def _validate(self):
        if not 0.5 <= float(self.p['radius_m']) <= float(self.p['max_radius_m']): raise ValueError('radius_m outside safety limits')
        if not 0.5 <= float(self.p['altitude_m']) <= float(self.p['max_altitude_m']): raise ValueError('altitude_m outside safety limits')
        if float(self.p['orbit_period_s']) < 8.0: raise ValueError('orbit_period_s must be at least 8 s')
        if float(self.p['setpoint_rate_hz']) < 10.0: raise ValueError('setpoint_rate_hz must be at least 10 Hz')

    def _now(self): return self.get_clock().now().nanoseconds / 1e9
    def _stamp_us(self): return int(self.get_clock().now().nanoseconds / 1000)
    def _elapsed(self): return self._now() - self.state_t0
    def _change(self, state):
        self.state, self.state_t0 = state, self._now()
        self.get_logger().info('STATE -> ' + state.name)

    def _start(self, request, response):
        del request
        if self.state not in (State.WAITING, State.FINISHED):
            response.success=False; response.message='Mission already active'; return response
        self.warmup_ticks=0; self._change(State.WARMUP)
        response.success=True; response.message='Orbit inspection started'; return response

    def _abort(self, request, response):
        del request; self._land(); self._change(State.LANDING)
        response.success=True; response.message='Landing requested'; return response

    def _odom(self, msg):
        self.measured = tuple(float(v) for v in msg.position)
        self._append_path(self.measured_path, self.measured)
        self.measured_path_pub.publish(self.measured_path)

    def _heartbeat(self):
        m=OffboardControlMode(); m.timestamp=self._stamp_us(); m.position=True
        for field in ('velocity','acceleration','attitude','body_rate','thrust_and_torque','direct_actuator'):
            if hasattr(m, field): setattr(m, field, False)
        self.heartbeat_pub.publish(m)

    def _setpoint(self, n, e, d, yaw):
        self.desired=(float(n),float(e),float(d))
        m=TrajectorySetpoint(); m.timestamp=self._stamp_us(); m.position=list(self.desired)
        m.velocity=[math.nan]*3; m.acceleration=[math.nan]*3; m.jerk=[math.nan]*3
        m.yaw=float(yaw); m.yawspeed=math.nan; self.setpoint_pub.publish(m)
        self._append_path(self.desired_path, self.desired); self.desired_path_pub.publish(self.desired_path)

    def _command(self, command, p1=0.0, p2=0.0):
        m=VehicleCommand(); m.timestamp=self._stamp_us(); m.command=int(command)
        m.param1=float(p1); m.param2=float(p2); m.target_system=1; m.target_component=1
        m.source_system=1; m.source_component=1; m.from_external=True; self.command_pub.publish(m)

    def _offboard_and_arm(self):
        self._command(VehicleCommand.VEHICLE_CMD_DO_SET_MODE,1.0,6.0)
        self._command(VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM,1.0,0.0)

    def _land(self): self._command(VehicleCommand.VEHICLE_CMD_NAV_LAND)

    def _append_path(self, path, ned):
        # RViz is ENU. For visualization only: ENU=(East, North, Up)=(y,x,-z).
        pose=PoseStamped(); pose.header.frame_id='map'; pose.header.stamp=self.get_clock().now().to_msg()
        pose.pose.position.x=ned[1]; pose.pose.position.y=ned[0]; pose.pose.position.z=-ned[2]
        path.header.stamp=pose.header.stamp; path.poses.append(pose)
        if len(path.poses)>2500: path.poses=path.poses[-2500:]

    def _publish_target(self):
        marker=Marker(); marker.header.frame_id='map'; marker.header.stamp=self.get_clock().now().to_msg()
        marker.ns='inspection'; marker.id=0; marker.type=Marker.CYLINDER; marker.action=Marker.ADD
        marker.pose.position.x=float(self.p['center_east_m']); marker.pose.position.y=float(self.p['center_north_m'])
        marker.pose.position.z=0.5; marker.scale.x=1.2; marker.scale.y=1.2; marker.scale.z=1.0
        marker.color.r=1.0; marker.color.g=0.25; marker.color.b=0.05; marker.color.a=0.9
        self.target_pub.publish(marker)

    def _tick(self):
        self._publish_target()
        if self.state in (State.WAITING,State.FINISHED): return
        self._heartbeat(); t=self._elapsed(); cx=float(self.p['center_north_m']); cy=float(self.p['center_east_m'])
        h=float(self.p['altitude_m']); r=float(self.p['radius_m']); first=(cx+r,cy,-h)

        if self.state==State.WARMUP:
            self._setpoint(0.0,0.0,-0.5,0.0); self.warmup_ticks+=1
            if self.warmup_ticks>=int(float(self.p['setpoint_rate_hz'])):
                self._offboard_and_arm(); self._change(State.CLIMB)
        elif self.state==State.CLIMB:
            u=smoothstep(t/float(self.p['climb_time_s'])); self._setpoint(0.0,0.0,-h*u,0.0)
            if u>=1.0: self._change(State.APPROACH)
        elif self.state==State.APPROACH:
            u=smoothstep(t/float(self.p['approach_time_s'])); n=u*first[0]; e=u*first[1]
            self._setpoint(n,e,-h,inward_yaw(n,e,cx,cy))
            if u>=1.0: self._change(State.ORBIT)
        elif self.state==State.ORBIT:
            angle=2.0*math.pi*t/float(self.p['orbit_period_s']); n,e=orbit_point(cx,cy,r,angle)
            yaw=inward_yaw(n,e,cx,cy) if bool(self.p['face_center']) else angle+math.pi/2.0
            self._setpoint(n,e,-h,yaw)
            if t>=float(self.p['orbit_period_s'])*float(self.p['number_of_laps']): self._change(State.HOLD)
        elif self.state==State.HOLD:
            self._setpoint(*first,inward_yaw(first[0],first[1],cx,cy))
            if t>=float(self.p['final_hold_s']):
                if bool(self.p['auto_land']): self._land(); self._change(State.LANDING)
                else: self._change(State.FINISHED)
        elif self.state==State.LANDING and t>=10.0: self._change(State.FINISHED)

        if self.measured and int(t*2)%2==0:
            err=tracking_error(self.desired,self.measured)
            self.get_logger().info(f'{self.state.name:8s} desired={self.desired!s} tracking_error={err:.2f} m', throttle_duration_sec=1.0)


def main(args=None):
    rclpy.init(args=args); node=OrbitController()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally: node.destroy_node(); rclpy.shutdown()
