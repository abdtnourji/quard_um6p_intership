# Autonomous Drone Engineering: 8-Day Intensive Syllabus
## Project Track 2: From Zero Knowledge to an Evidence-Based Autonomous Inspection Mission

**Project repository:** [quard_um6p_intership](https://github.com/abdtnourji/quard_um6p_intership)  
**Format:** 8 afternoon sessions, 4 hours per session  
**Total contact time:** 32 hours  
**Audience:** First-year students with no previous experience in Linux, Python, ROS 2, PX4, Gazebo, or computer vision  
**Reference platform:** Ubuntu 22.04, Python 3.10, ROS 2 Humble, PX4 `release/1.15`, matching `px4_msgs release/1.15`, Micro XRCE-DDS Agent, Gazebo, OpenCV, and YOLOv8  
**Project model:** PX4 `x500_depth` quadcopter with camera  
**Primary mode:** Simulation-first using PX4 SITL and Gazebo

---

## 1. Purpose of This Syllabus

This syllabus defines the **concepts, classroom explanations, guided exercises, and project-reading activities** required for students to understand and modify the autonomous-drone project.

It does **not** duplicate the detailed installation commands already maintained in the GitHub repository. During installation workshops, students must follow the repository guides exactly:

```text
quard_um6p_intership/installation_guide/
├── README_PHASE0_UBUNTU_ROS2_SETUP.md
├── README_PHASE1_PX4_AI_VENV_SETUP.md
└── README_PHASE_3_PIPELINE.md
```

The instructor uses classroom time to explain:

- what each installed component does;
- why a particular version or configuration is required;
- how the components connect;
- how to verify that a step worked;
- how to diagnose problems systematically;
- how to read and modify the project code safely.

The detailed terminal commands remain in the repository guides so that there is only one authoritative installation procedure.

---

## 2. Pedagogical Approach

The learning model is:

```text
Theory and intuition: 20%
Guided observation and practice: 40%
Application to the final project: 40%
```

Every session follows the same engineering cycle:

```text
Observe -> Predict -> Modify one factor -> Run -> Measure -> Explain
```

Students should never modify several variables at the same time. When a result differs from the prediction, the instructor guides the students with five questions:

1. What was expected?
2. What was observed?
3. Which system layer could cause the difference?
4. What is the smallest test that distinguishes the possible causes?
5. What evidence supports the conclusion?

The objective is not memorizing commands. The objective is understanding **which engineering question each command answers**.

---

## 3. Final Learning Outcome

By the end of Day 8, each student should be able to:

1. run the complete GitHub project on a prepared personal laptop;
2. explain the roles of Ubuntu, Python, ROS 2, PX4, Gazebo, Micro XRCE-DDS, OpenCV, and YOLOv8;
3. identify how information flows between Gazebo, PX4, ROS 2, the orbit controller, the camera bridge, and the detector;
4. use ROS 2 discovery tools to find nodes, topics, services, parameters, and message types;
5. explain the basic Python structure of the three educational scripts:
   - `trajectory.py`;
   - `mission_monitor.py`;
   - `orbit_controller.py`;
6. explain the mission state machine:

```text
WAITING -> WARMUP -> CLIMB -> APPROACH -> ORBIT
        -> HOLD -> LANDING -> FINISHED
```

7. explain the PX4 North-East-Down coordinate system;
8. explain how orbit radius and period determine trajectory geometry and speed;
9. launch the `x500_depth` drone, add inspection objects, and verify `/fmu` telemetry;
10. discover and bridge the actual camera topic instead of guessing its name;
11. run the orbit mission and YOLOv8 pipeline;
12. make one safe modification to the mission or perception parameters;
13. collect before-and-after evidence;
14. explain one limitation or failure and propose a justified next step.

---

## 4. Standard Four-Hour Session Structure

Each afternoon follows a familiar structure so beginners always know what comes next.

```text
13:00-13:15  Review, objectives, and connection to the final system
13:15-14:00  Concept lesson with visual examples
14:00-14:40  Instructor demonstration and guided code reading
14:40-14:50  Break
14:50-16:00  Guided hands-on laboratory
16:00-16:10  Break
16:10-16:40  Project application or controlled challenge
16:40-17:00  Validation, logbook, questions, and exit ticket
```

Installation days may use more workshop time, but the instructor should still reserve time to explain concepts and validate understanding.

---

    # Day 1: The Foundation - System Mission, Ubuntu, Terminal, and GitHub

## Session objective

Establish the students' mental model of the final system, remove the fear of the terminal, and begin the validated Ubuntu environment setup without turning installation into the entire learning experience.

## Expected visible result

Each student can open the repository, identify its main directories, use basic terminal navigation, explain the final autonomous inspection mission, and determine the current installation state of the laptop.

## 13:00-13:15 | Welcome and final-project demonstration

Show the completed pipeline before explaining individual components:

```text
Gazebo world
    -> x500_depth drone
    -> autonomous orbit trajectory
    -> camera stream
    -> ROS 2 image bridge
    -> YOLOv8 detections
    -> annotated image and mission evidence
```

Students should see the final destination before beginning foundational lessons.

### Instructor emphasis

Explain that the project is not simply an AI detector and not simply a flight-control exercise. It is a small autonomous system in which several specialist components must cooperate.

## 13:15-14:00 | Theory: The engineering ecosystem

### Concepts to teach

- **Operating system:** the software layer that manages the computer and applications.
- **Ubuntu:** the Linux operating system selected for the validated project environment.
- **Terminal:** a text-based method for asking the operating system to perform precise operations.
- **Shell:** the program that reads terminal commands.
- **Filesystem:** the organized hierarchy of folders and files.
- **Source code:** human-readable instructions that must be interpreted or executed.
- **Process:** a program currently running in memory.
- **Dependency:** another software component required by the project.
- **Environment variable:** a named value used by programs to find paths and configuration.
- **Simulation:** a controlled model of the physical system, not merely an animation.

### Project connection

Use the repository folders to explain separation of responsibility:

```text
config/              shared project paths and configuration
dependencies/        PX4 and DDS source repositories
gazebo/              local models and worlds
installation_guide/  authoritative setup procedures
models/               YOLO model files
perception/           camera and detection code
ros2_ws/              ROS 2 packages and build workspace
scripts/              repeatable setup and utility commands
student_logs/         individual engineering evidence
tools/                supporting control or teleoperation utilities
```

## 14:00-14:40 | Demonstration: Terminal as a precise engineering tool

Explain and demonstrate the following command categories rather than only listing commands:

### Where am I?

```bash
pwd
```

### What is here?

```bash
ls
ls -la
tree -L 2
```

### How do I move?

```bash
cd <directory>
cd ..
cd "${HOME}"
```

### How do I inspect a text file?

```bash
cat README.md
less README.md
```

### How do I create, copy, rename, and remove practice files?

```bash
mkdir practice
touch practice/notes.txt
cp practice/notes.txt practice/notes_copy.txt
mv practice/notes_copy.txt practice/renamed_notes.txt
rm practice/renamed_notes.txt
```

Explain that destructive commands such as `rm` must be used only in the instructor-created practice directory.

## 14:50-16:00 | Workshop: Repository access and Ubuntu readiness

Students open or clone the GitHub repository and inspect the top-level `README.md`.

The instructor explains these Git concepts:

- repository;
- clone;
- working copy;
- branch;
- commit;
- pull;
- local versus remote content.

Students then begin or verify Ubuntu by following:

```text
installation_guide/README_PHASE0_UBUNTU_ROS2_SETUP.md
```

Do not repeat the guide's installation commands in the lecture. Instead, explain why the guide checks:

- Ubuntu version;
- CPU architecture;
- system Python version;
- system updates;
- UTF-8 locale;
- available disk space;
- ROS 2 installation location.

## 16:10-16:40 | Project scavenger hunt

Each pair finds and explains:

1. the file that defines project environment variables;
2. the folder containing PX4 after download;
3. the ROS 2 source directory;
4. the folder containing Gazebo objects;
5. the folder containing installation guides;
6. the folder used to store student evidence;
7. the main pipeline README.

The goal is to learn the project map, not to memorize every file.

## 16:40-17:00 | Validation and exit ticket

Each student submits:

- the output of `pwd` from the project root;
- a screenshot of the repository in VS Code;
- a simple architecture sketch;
- a five-sentence explanation of the final mission;
- the first engineering logbook entry.

## Instructor checkpoint

A student is ready for Day 2 when the student can distinguish:

```text
computer -> operating system -> terminal -> repository -> file -> running process
```

---

# Day 2: The Language - Python for the Project

## Session objective

Teach only the Python concepts students need to read `trajectory.py`, `mission_monitor.py`, and `orbit_controller.py`.

## Expected visible result

Each student can execute a small Python file, explain functions and data structures, and calculate points on the orbit using the project's mathematical helper functions.

## 13:00-13:15 | Review

Ask students to explain:

- the difference between a file and a running program;
- the project root;
- why paths should use `${HOME}` instead of another student's username;
- why installation instructions are kept in one authoritative guide.

## 13:15-14:00 | Core Python concepts

Use examples from the drone mission.

### Variables and basic types

```python
altitude_m = 4.0
number_of_laps = 1.25
armed = False
state_name = "WAITING"
```

Explain:

- a variable is a meaningful name attached to a value;
- `int` represents whole numbers;
- `float` represents decimal numbers;
- `bool` represents `True` or `False`;
- `str` represents text.

### Collections used in the project

```python
position = (0.0, 0.0, -4.0)
velocity = [0.0, 0.0, 0.0]
mission = {"radius_m": 5.0, "orbit_period_s": 24.0}
```

Explain:

- **tuple:** fixed ordered group, used for a position snapshot;
- **list:** ordered collection that can be modified;
- **dictionary:** key-value storage, useful for named parameters;
- **index:** position within a collection, starting at zero.

### Conditions and loops

Teach the exact reasoning needed to read mission state checks and parameter loops.

```python
if altitude_m > 10.0:
    print("Altitude exceeds the classroom limit")
```

```python
for value in velocity:
    print(value)
```

## 14:00-14:40 | Functions, modules, and code organization

Read selected parts of `trajectory.py`.

### Function mental model

```text
inputs -> named operation -> output
```

Discuss:

- `def`;
- function parameters;
- type hints;
- return values;
- importing the `math` module;
- why pure mathematics is separated from ROS 2 code;
- why small functions are easier to test.

### Project functions

```text
smoothstep(u)
orbit_point(cx, cy, radius, angle)
inward_yaw(north, east, cx, cy)
tracking_error(desired, measured)
```

For each function, ask:

1. What enters?
2. What leaves?
3. Which units are used?
4. What physical idea does the function represent?
5. How can the function be tested independently?

## 14:50-16:00 | Guided laboratory: Trajectory mathematics in Python

Students perform small exercises using project equations.

### Circle geometry

```text
N = N_center + R cos(theta)
E = E_center + R sin(theta)
```

Students calculate and then verify the positions corresponding to:

```text
0 degrees
90 degrees
180 degrees
270 degrees
```

### Orbit timing

```text
theta(t) = 2*pi*t/T
v = 2*pi*R/T
```

Using the project defaults:

```text
radius = 5 m
period = 24 s
```

students calculate the approximate tangential speed and predict what changes when the period is reduced.

### Tracking error

```text
error = sqrt((Nd-Nm)^2 + (Ed-Em)^2 + (Dd-Dm)^2)
```

Students compare a desired position and measured position and interpret the result in metres.

## 16:10-16:40 | OOP preparation for ROS 2

Introduce only the essential object-oriented concepts:

```python
class MissionMonitor:
    def __init__(self):
        self.position = None
```

Memory model:

```text
class      = blueprint
object     = one constructed example
__init__   = setup performed at construction
self       = this particular object
attribute  = information stored by the object
method     = function belonging to the object
```

Do not teach advanced inheritance theory. Students only need enough preparation to recognize `class OrbitController(Node)` on Day 3.

## 16:40-17:00 | Exit challenge

Each student must:

- explain one function from `trajectory.py`;
- compute one orbit point by hand;
- verify it with Python;
- identify one tuple, one loop, and one dictionary in the project;
- record one confusing syntax element for review.

## Instructor checkpoint

Students are ready when they can read a small function from top to bottom and explain the sequence without executing it first.

---

# Day 3: The Middleware - ROS 2 Concepts and Python Nodes

## Session objective

Teach how independent robotics programs communicate asynchronously and connect those concepts directly to the project's monitoring and orbit nodes.

## Expected visible result

Students can inspect a ROS 2 graph, explain publishers and subscribers, and read the structure of `mission_monitor.py`.

## 13:00-14:00 | Theory: ROS 2 as a communication system

Use a radio-network analogy:

```text
Node       = one specialist with a radio
Publisher  = transmitter
Subscriber = receiver
Topic      = named radio channel
Message    = agreed information format
Service    = request followed by response
Parameter  = configurable setting
Timer      = repeating alarm clock
Callback   = function executed when an event occurs
```

### Why asynchronous communication matters

A drone camera, estimator, controller, and monitor do not all run at the same frequency. ROS 2 allows independent components to exchange data without placing all logic inside one program.

### Topic names and message types

Explain that communication requires both:

```text
same topic name + compatible message type
```

Students learn to discover interfaces using:

```bash
ros2 node list
ros2 node info <node_name>
ros2 topic list
ros2 topic info <topic_name> --verbose
ros2 interface show <message_type>
ros2 service list
ros2 service type <service_name>
ros2 param list <node_name>
```

## 14:00-14:40 | QoS, callbacks, and node lifecycle

### Quality of Service

Teach an intuitive distinction:

```text
Reliable     = make stronger efforts to deliver every message
Best effort  = prioritize fresh data; occasional loss may be acceptable
Keep last    = keep only a limited number of recent messages
Depth 1      = retain only the newest message
```

Connect this directly to PX4 odometry. A current position estimate is more useful than a queue of old estimates.

### Callback lifecycle

```text
message arrives -> ROS 2 calls callback -> callback updates node memory
```

### Node lifecycle used by the project

```text
rclpy.init()
create node
rclpy.spin(node)
callbacks and timers execute
destroy node
rclpy.shutdown()
```

## 14:50-15:35 | Guided code reading: `mission_monitor.py`

Students locate and explain:

- imports;
- inheritance from `Node`;
- `__init__`;
- node name `mission_monitor`;
- `QoSProfile`;
- `/fmu/out/vehicle_odometry` subscriber;
- `/fmu/out/vehicle_status` subscriber;
- `_odom` and `_status` callbacks;
- one-second timer;
- speed calculation;
- altitude sign conversion;
- logging and formatting;
- clean shutdown.

### Project topic naming

Explain:

```text
/fmu/out/... = data leaving the PX4 Flight Management Unit toward ROS 2
/fmu/in/...  = data entering PX4 from ROS 2
/orbit/...   = application-specific interfaces created by this project
```

Students should know that PX4 interface names are determined by the PX4 ROS 2 bridge configuration. Application-specific names are chosen by the project developer for clarity and grouping.

## 15:35-16:00 | ROS 2 practice

Use talker/listener or Turtlesim only to isolate concepts before the PX4 system is running.

Students answer:

1. Which node publishes?
2. Which node subscribes?
3. What is the topic name?
4. What is the message type?
5. What command proves each answer?

## 16:10-16:40 | Environment and workspace checkpoint

Students follow the relevant repository guides to complete or validate ROS 2 and the project workspace.

The lecture explains these concepts without repeating installation steps:

- underlay: `/opt/ros/humble`;
- overlay: project `ros2_ws/install`;
- workspace source folder;
- build, install, and log directories;
- why `colcon build --symlink-install` is useful during development;
- why `source install/setup.bash` is required;
- why unrelated workspaces must not be mixed.

## 16:40-17:00 | Exit ticket

Each student draws:

```text
PX4 publisher -> /fmu/out/vehicle_odometry -> MissionMonitor subscriber
```

and explains:

- what triggers `_odom`;
- what data are saved;
- why `depth=1` is reasonable;
- why altitude is calculated using `-position[2]`.

---

# Day 4: The Physics - Quadcopter Architecture and Gazebo Digital Twin

## Session objective

Build a correct mental model of quadcopter motion, PX4 control responsibilities, simulation, coordinate frames, and the `x500_depth` model.

## Expected visible result

Students can launch or observe the simulated drone, identify its major components, explain roll, pitch, yaw, thrust, and distinguish PX4 from Gazebo.

## 13:00-14:00 | Theory: Quadcopter mechanics and control hierarchy

### Main physical components

- frame;
- four motors and propellers;
- electronic speed controllers;
- flight controller;
- inertial measurement unit;
- position and altitude sensors;
- battery and power distribution;
- camera or payload.

### Motion intuition

- **collective thrust:** all rotor thrust changes together, mainly influencing vertical motion;
- **roll:** left-right tilt;
- **pitch:** forward-backward tilt;
- **yaw:** rotation around the vertical axis;
- **translation:** the vehicle tilts so part of its thrust acts horizontally.

### Control hierarchy in this project

```text
Orbit mission node
    -> desired position and yaw
PX4 position controller
    -> desired attitude and thrust
PX4 attitude and angular-rate controllers
    -> actuator commands
Gazebo vehicle model
    -> simulated motion
PX4 state estimator
    -> measured position and velocity
```

The mission code does not directly calculate individual motor speeds.

## 14:00-14:40 | Gazebo as a digital-twin laboratory

Explain the separation between:

- **world:** ground, lighting, gravity, and objects;
- **model:** drone or inspection object;
- **link:** rigid body;
- **joint:** relationship between bodies;
- **sensor:** simulated measurement source;
- **physics engine:** computes movement and interactions;
- **rendering:** produces the visual scene;
- **simulation time:** time used by simulated processes.

### Project-specific assets

Connect the theory to:

```text
gazebo/models/
gazebo/worlds/
PX4 x500_depth model
inspection car
inspection stop sign
inspection person marker
```

Explain that `x500_depth` includes a camera/depth-camera configuration and that camera orientation affects what YOLO can observe.

## 14:50-15:35 | Coordinate frames

Introduce PX4 NED:

```text
N = North
E = East
D = Down
```

Therefore:

```text
position z = -4 m represents an altitude of 4 m above the origin
```

Compare with RViz ENU:

```text
ENU = East, North, Up
NED -> ENU display conversion = (East, North, -Down)
```

Explain four distinct frames students may encounter:

- Gazebo world frame;
- PX4 local NED frame;
- drone body frame;
- camera optical frame.

Avoid claiming that coordinates from different frames are interchangeable.

## 15:35-16:00 | PX4 and Gazebo readiness workshop

Students use the repository guide for setup and launch. The instructor does not re-document installation commands.

Classroom emphasis:

- why PX4 and `px4_msgs` releases must match;
- what SITL means;
- why the PX4 setup script installs simulation tools;
- why submodules matter in the PX4 repository;
- why the project uses an independent PX4 checkout;
- why the empty Gazebo world may be expected before objects are spawned.

## 16:10-16:40 | Simulation observation challenge

Students observe the drone and identify:

- position in the world;
- drone heading;
- camera location and viewing direction;
- likely NED axes;
- one inspection object pose;
- the difference between changing the world and changing the drone controller.

If manual flight is used, it is an observation exercise rather than a free-flight session. One validated control method is used under instructor supervision.

## 16:40-17:00 | Exit evidence

Students submit:

- a labelled quadcopter component sketch;
- a PX4-versus-Gazebo responsibility list;
- a NED coordinate exercise;
- a screenshot of the `x500_depth` model;
- one paragraph explaining the term digital twin.

---

# Day 5: The Bridge - PX4, ROS 2, and Offboard Control

## Session objective

Explain how ROS 2 mission software reaches PX4 through uXRCE-DDS, and how PX4 telemetry returns to the ROS 2 graph.

## Expected visible result

Students can start the Agent and simulation using the project guide, observe `/fmu` topics, and explain the Offboard heartbeat and setpoint interfaces.

## 13:00-14:00 | Theory: The PX4-ROS 2 communication chain

Use the exact project architecture:

```text
ROS 2 orbit node
    -> /fmu/in/offboard_control_mode
    -> /fmu/in/trajectory_setpoint
    -> /fmu/in/vehicle_command
Micro XRCE-DDS Agent
    <-> PX4 uXRCE-DDS client
PX4
    -> /fmu/out/vehicle_odometry
    -> /fmu/out/vehicle_status
ROS 2 monitor and controller
```

### Concepts to teach

- DDS as the underlying data-distribution technology;
- resource-constrained client versus Agent;
- why PX4 simulator starts the client;
- why the Agent uses UDP port 8888 in the project;
- why only one Agent should use the connection channel;
- why matching message definitions matter;
- data entering PX4 versus data leaving PX4.

## 14:00-14:40 | Offboard-control concepts

Explain the three main project publisher interfaces.

### `/fmu/in/offboard_control_mode`

Purpose: continuously tells PX4 which external-control variables are active.

Project choice:

```text
position = true
velocity, acceleration, attitude, body rate, and actuator control = false
```

### `/fmu/in/trajectory_setpoint`

Purpose: carries desired NED position and yaw.

Explain why unused velocity, acceleration, jerk, and yaw-rate fields are assigned `NaN`: they are intentionally unspecified rather than commanded as zero.

### `/fmu/in/vehicle_command`

Purpose: sends discrete commands such as mode change, arm/disarm, and land.

Distinguish continuous setpoint streams from occasional command messages.

## 14:50-15:25 | Why warmup exists

Read the WARMUP state conceptually:

```text
publish small, valid setpoints
count approximately one second of updates
request Offboard mode
request arming
transition to CLIMB
```

Explain that Offboard is a live stream, not a single destination sent once. The heartbeat and position setpoints must continue during active external control.

## 15:25-16:00 | Guided system inspection

Students follow `README_PHASE_3_PIPELINE.md` to start the minimum communication chain.

They use discovery commands to answer:

1. Is the Agent process running?
2. Is PX4 running?
3. Which `/fmu/out` topics exist?
4. Does vehicle odometry arrive?
5. Which node subscribes to odometry?
6. Which message type defines the data?

The instructor emphasizes evidence rather than assuming that a silent terminal is broken.

## 16:10-16:40 | Applied topic-mapping exercise

Students complete an interface card for each PX4 topic used by `orbit_controller.py`:

```text
Topic name
Direction relative to PX4
Message type
Publisher
Subscriber
Purpose
Expected update pattern
Failure symptom
Verification command
```

## 16:40-17:00 | Exit ticket

Students explain, without reading notes:

- why `/fmu/in` and `/fmu/out` are different;
- why `px4_msgs` must match PX4;
- what the Agent does;
- why Offboard control requires a stream;
- why the mission node does not directly control motors.

---

# Day 6: The Project - State Machine, Orbit Physics, and Mission Execution

## Session objective

Demystify `orbit_controller.py`, connect every mission state to vehicle behavior, and perform a controlled mission-parameter experiment.

## Expected visible result

Students can run the orbit mission, use start and abort services, explain the trajectory equation, and make one safe parameter modification.

## 13:00-13:45 | State-machine theory

Draw the project state machine:

```text
WAITING
   -> WARMUP
   -> CLIMB
   -> APPROACH
   -> ORBIT
   -> HOLD
   -> LANDING
   -> FINISHED
```

For each state, students identify:

- entry condition;
- output setpoint or command;
- exit condition;
- visible Gazebo behavior;
- likely failure symptom.

Explain why a state machine prevents incompatible phases from executing simultaneously.

## 13:45-14:30 | Project parameters and validation

Read the project parameters conceptually:

```text
center_north_m
center_east_m
altitude_m
radius_m
orbit_period_s
number_of_laps
climb_time_s
approach_time_s
final_hold_s
setpoint_rate_hz
face_center
auto_start
auto_land
max_radius_m
max_altitude_m
```

Teach naming conventions:

- `_m` means metres;
- `_s` means seconds;
- `_hz` means updates per second;
- Boolean parameters represent enabled or disabled behavior.

Explain why `_validate()` rejects:

- a radius outside the classroom limits;
- an altitude outside the classroom limits;
- an orbit period below the selected limit;
- a setpoint frequency too low for reliable Offboard operation.

These are project safety and reliability constraints, not universal limits for all drones.

## 14:30-14:40 | Break

## 14:40-15:25 | Orbit equations and camera-facing yaw

### Orbit position

```text
angle = 2*pi*t/orbit_period
North = center_N + radius*cos(angle)
East = center_E + radius*sin(angle)
Down = -altitude
```

### Inward yaw

```text
yaw = atan2(center_E - East, center_N - North)
```

Explain why `atan2` preserves direction in all quadrants.

### Tangential behavior

```text
v = 2*pi*R/T
a_c = v^2/R = 4*pi^2*R/T^2
```

Students calculate values for the project defaults and predict the effect of a shorter period.

## 15:25-16:00 | Mission execution

Students follow the pipeline guide and run:

- the orbit launch file;
- `/orbit/start`;
- `/orbit/abort` when requested;
- mission monitor;
- desired and measured path outputs if visualized.

They inspect:

```text
/orbit/desired_path
/orbit/measured_path
/orbit/inspection_target
/fmu/out/vehicle_odometry
```

Explain that desired path is the command history, while measured path is evidence of actual estimated motion.

## 16:10-16:40 | Controlled modification experiment

Each pair changes exactly one of:

- `radius_m`;
- `orbit_period_s`;
- `altitude_m`;
- `number_of_laps`;
- `final_hold_s`;
- `face_center`.

Required engineering record:

```text
Original value
New value
Prediction
Equation or reasoning
Observed behavior
Measured evidence
Conclusion
```

Do not let students combine a faster orbit, larger radius, different altitude, and new camera angle in one test.

## 16:40-17:00 | Exit ticket

Each student explains one state and one equation, then identifies one difference between desired and measured motion.

---

# Day 7: The Eyes - Camera Transport, OpenCV, and YOLOv8

## Session objective

Explain how a simulated image reaches the detector and how to evaluate detection results critically.

## Expected visible result

Students discover the actual camera topic, bridge it to ROS 2, display raw images, run YOLOv8, and conduct one controlled perception experiment.

## 13:00-13:45 | From light to an image array

Explain:

- image width and height;
- pixel coordinates;
- color channels;
- OpenCV arrays;
- frame rate;
- resolution;
- camera field of view;
- object size in pixels;
- effect of altitude, distance, and viewing angle.

Pixel coordinates typically use:

```text
origin at top-left
x increases to the right
y increases downward
```

This image coordinate system is different from the drone world coordinate system.

## 13:45-14:30 | ROS 2 image transport

Explain the complete pipeline:

```text
Gazebo sensor
    -> Gazebo Transport image topic
ros_gz_image image_bridge
    -> ROS 2 sensor_msgs/Image
cv_bridge
    -> OpenCV array
YOLOv8
    -> boxes, classes, confidence
project outputs
    -> annotated image and inspection report
```

### Why topic discovery comes first

The project commonly uses `/camera`, but students must verify the running simulation because topic names come from the model configuration.

Use:

```bash
gz topic -l
ros2 topic list
ros2 topic info <topic> --verbose
ros2 topic hz <topic>
```

Explain that `image_bridge` may run silently. Topic frequency and image visualization are the real tests.

## 14:30-14:40 | Break

## 14:40-15:25 | YOLOv8 concepts

Teach only inference concepts needed by the project:

- pretrained model;
- class label;
- bounding box;
- confidence score;
- confidence threshold;
- inference time;
- frame skipping;
- CPU versus GPU inference;
- false positive;
- false negative;
- dataset bias;
- realistic object versus simple marker.

Clarify that a model called `inspection_car` in Gazebo is not guaranteed to be recognized as a car. Recognition depends on visual appearance and training data, not the Gazebo entity name.

## 15:25-16:00 | Project perception code walkthrough

Locate and explain the project perception components, such as:

```text
perception/
yolo_detector.py
inspection_reporter.py
inspection_yolo.launch.py
models/yolo/
```

Students identify:

- model path;
- image input topic;
- output detection topic;
- debug or annotated image topic;
- confidence parameter;
- report output path;
- callback receiving images;
- conversion from ROS image to OpenCV image;
- inference call;
- publication and logging.

The instructor focuses on the data path, not the internal mathematics of deep-network training.

## 16:10-16:40 | Controlled perception experiment

Each pair changes one factor:

- confidence threshold;
- object distance;
- object orientation;
- orbit altitude;
- camera pitch;
- inference-every-N-frames setting;
- realistic object versus pedagogical marker.

Required evidence:

- before image;
- after image;
- number of detections;
- confidence values;
- interpretation;
- limitation.

## 16:40-17:00 | Exit ticket

Students explain:

- why the raw image must work before debugging YOLO;
- what confidence means and does not mean;
- one cause of a missed detection;
- one cost of running inference on every frame;
- the difference between Gazebo image topics and ROS 2 image topics.

---

# Day 8: The Capstone - Independent Integration and Basic Modification

## Session objective

Require students to independently run the complete project, make a bounded modification, collect evidence, and explain the system architecture.

## Expected visible result

Each team performs a repeatable autonomous inspection demonstration and defends one modification using before-and-after evidence.

## 13:00-13:20 | Readiness briefing

Students reconstruct the startup dependency chain from memory:

```text
project environment
    -> DDS Agent
    -> PX4 and Gazebo
    -> inspection objects
    -> ROS 2 workspace
    -> camera bridge
    -> orbit mission
    -> YOLOv8
    -> visualization and evidence
```

The instructor confirms the sequence but does not provide terminal-by-terminal commands. Those remain in the project pipeline guide.

## 13:20-14:20 | Independent project launch

Each team launches the system using the GitHub documentation.

Required checks:

```text
PX4 and px4_msgs versions are coherent
DDS Agent is active
/fmu telemetry exists
x500_depth appears in Gazebo
inspection objects appear
RGB camera publishes
ROS 2 image topic has a measurable rate
orbit services exist
YOLO receives images
annotated output or report is generated
```

When a problem occurs, the team must identify the failing layer before changing configuration.

## 14:20-14:40 | Architecture explanation

Each team explains the system using one diagram. The explanation must cover:

- physical/simulation layer;
- flight-control layer;
- communication layer;
- mission layer;
- perception layer;
- evidence layer.

## 14:40-14:50 | Break

## 14:50-15:50 | Basic modification challenge

Each team selects one bounded task.

### Mission behavior options

- change orbit radius;
- change orbit period;
- change altitude;
- change number of laps;
- move the inspection center;
- change final hold time;
- change center-facing behavior.

### Simulation options

- move one inspection object;
- change one object pose;
- replace one object while preserving the spawn interface;
- adjust the validated camera view.

### Perception options

- change confidence threshold;
- change frame-processing interval;
- compare two object distances;
- compare raw and annotated output;
- improve report content without changing detector behavior.

Every team must document:

```text
Requirement
Original behavior
One selected change
Prediction
Implementation location
Validation method
Observed result
Evidence
Limitation
Next step
```

## 15:50-16:00 | Break

## 16:00-16:40 | Team demonstrations

Suggested five-minute structure:

1. mission statement;
2. system architecture;
3. assigned modification;
4. prediction;
5. live or recorded result;
6. evidence;
7. one failure or limitation;
8. next engineering step.

The explanation must remain meaningful if the live simulation fails.

## 16:40-17:00 | Individual reflection and final checkpoint

Each student submits:

- an individual logbook;
- one personally understood code block;
- one ROS 2 interface card;
- one calculation or prediction;
- one contribution to integration;
- one challenge encountered;
- one proposed improvement.

## Final acceptance statement

A student completes the core internship objective when the student can demonstrate:

> I can run the project on my laptop, explain how Gazebo, PX4, ROS 2, the mission controller, the camera bridge, and YOLOv8 work together, make one safe modification, measure its effect, and explain the result and limitations.

---

# Targeted Python Concepts Required by the Project

The lecture should teach the following concepts because students will encounter them in the project code.

## Essential syntax

- comments and docstrings;
- imports and modules;
- variables and assignment;
- `int`, `float`, `bool`, `str`, and `None`;
- lists, tuples, and dictionaries;
- indexing and negative indexing;
- arithmetic and comparison operators;
- Boolean conditions;
- `if`, `elif`, and `else`;
- `for` loops;
- functions and return values;
- type hints at a reading level;
- classes, inheritance, `self`, and `__init__`;
- attributes and methods;
- callbacks;
- `try`, `except`, and `finally`;
- formatted strings;
- `math.nan`;
- tuple unpacking with `*first`;
- comprehensions at a reading level;
- `zip`, `sum`, `getattr`, `hasattr`, and `setattr`;
- list slicing such as `path.poses[-2500:]`.

## Concepts intentionally excluded

- neural-network training from scratch;
- advanced Python decorators;
- metaclasses;
- asynchronous framework internals;
- complex package-distribution internals;
- flight-controller implementation from first principles.

---

# Targeted ROS 2 Concepts Required by the Project

Students should understand:

- ROS 2 nodes as independently executing components;
- publishers and subscribers;
- topics and message-type contracts;
- callbacks and event-driven code;
- timers and update frequency;
- services for start and abort requests;
- parameters for safe behavioral modification;
- QoS for streaming telemetry and images;
- workspace underlay and overlay;
- Colcon build process;
- launch files;
- topic frequency and publisher/subscriber counts;
- ROS 2 image messages and `cv_bridge`;
- ROS 2 bag recording as evidence;
- `rqt_graph` as an architecture observation tool;
- `rqt_image_view` as a camera-pipeline validation tool.

## Discovery commands to practice repeatedly

```bash
ros2 node list
ros2 node info <node_name>
ros2 topic list
ros2 topic info <topic_name> --verbose
ros2 topic echo <topic_name> --once
ros2 topic hz <topic_name>
ros2 interface show <message_type>
ros2 service list
ros2 service type <service_name>
ros2 param list <node_name>
ros2 pkg executables <package_name>
```

Students should not merely memorize the commands. For each command, students should state the question it answers.

---

# Project-Specific Interface Map for the Lectures

## PX4 inputs used by the mission controller

```text
/fmu/in/offboard_control_mode
/fmu/in/trajectory_setpoint
/fmu/in/vehicle_command
```

## PX4 outputs used by the project

```text
/fmu/out/vehicle_odometry
/fmu/out/vehicle_status
```

## Project-specific orbit interfaces

```text
/orbit/start
/orbit/abort
/orbit/desired_path
/orbit/measured_path
/orbit/inspection_target
```

## Camera and perception interfaces

The exact Gazebo camera topic must be discovered from the running model. The project commonly bridges the RGB stream to:

```text
/camera/image_raw
```

The perception package may publish project-specific interfaces such as:

```text
/inspection/detections
/inspection/debug_image
```

Students must verify names using the running ROS 2 graph and the project launch/configuration files.

---

# Assessment Rubric

| Criterion | Weight | Expected evidence |
|---|---:|---|
| Independent project operation | 20% | Student launches and validates the pipeline using repository guides |
| Conceptual understanding | 20% | Student explains subsystem roles, data flow, and coordinate frames |
| Code reading and modification | 20% | Student identifies the relevant code path and makes one bounded change |
| Experimental reasoning | 20% | Prediction, controlled variable, measurement, result, and interpretation |
| Documentation and teamwork | 10% | Logbook, clear contribution, interface awareness, and integration support |
| Final communication | 10% | Concise demonstration with evidence, limitations, and next step |

A perfect-looking flight without understanding should not receive the highest evaluation. A failed behavior can receive strong credit when the student isolates the cause with evidence and proposes a defensible correction.

---

# Instructor Preparation and Recovery Plan

Before Day 1, the instructor should:

- validate the complete project on a clean Ubuntu 22.04 system;
- freeze the tested software versions;
- prepare at least one complete reference laptop;
- keep a backup of the repository and large dependencies;
- prepare a restoration path for students whose installation fails;
- verify the Gazebo graphics performance of available laptops;
- confirm that CPU-based YOLO inference works;
- prepare a short video of the final pipeline;
- prepare screenshots of expected terminal outputs;
- verify that all project guides use student-independent home paths;
- confirm that no private credentials are stored in the repository.

## Recovery rule

If a student's environment remains blocked after a bounded troubleshooting period, restore or provide the validated environment so that the student continues learning the system concepts. Installation is a necessary workshop, but it is not the final educational objective.

---

# Final Definition of Success

The course is successful when beginners progress from fear of the terminal to the ability to say:

> I understand the system architecture, I can run the autonomous inspection project on my laptop, I can inspect how ROS 2 components communicate, I can locate the Python code responsible for the mission, I can safely change one behavior, and I can validate and explain the result using evidence.

```text
Observe -> Understand -> Reproduce -> Modify -> Measure -> Explain
```
