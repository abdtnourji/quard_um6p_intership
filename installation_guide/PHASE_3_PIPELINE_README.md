# Phase 3 - Run the Autonomous AI Drone Inspection Pipeline

This guide explains how to run the complete internship demonstration in separate Terminator terminals:

1. verify the fixed software versions;
2. start the Micro XRCE-DDS Agent;
3. start PX4 v1.15 with the `x500_depth` model in Gazebo;
4. add inspection objects to the empty world;
5. discover and bridge the RGB camera into ROS 2;
6. run the `px4_orbit_inspection` package or fly manually;
7. run YOLO on the camera stream;
8. visualize and record the results.

The tutorial assumes that Phase 1 and Phase 2 are complete. Do not reinstall the complete platform if the checks below succeed.

---

## 1. Expected environment

| Component            | Required version or location             |
| -------------------- | ---------------------------------------- |
| Operating system     | Ubuntu 22.04                             |
| ROS 2                | Humble, `/opt/ros/humble`                |
| Python               | Python 3.10                              |
| Python environment   | `/home/<user_name>/px4-venv`             |
| NumPy                | 1.26.4                                   |
| PX4                  | `release/1.15`                           |
| `px4_msgs`           | `release/1.15`                           |
| Micro XRCE-DDS Agent | `master`, using the already tested build |
| PX4 model            | `x500_depth`, airframe ID `4002`         |
| ROS 2 workspace      | `${ROS2_WS}` from `config/project.env`   |

The matching PX4 and `px4_msgs` branches are important because ROS 2 applications must use message definitions compatible with the uXRCE-DDS client built into PX4.

---

## 2. Project layout

The important project structure is:

```text
quard_um6p_intership/
├── config/
│   ├── project.env
│   ├── DDS_AGENT_COMMIT.txt
│   ├── PX4_COMMIT.txt
│   └── PX4_MSGS_COMMIT.txt
├── data/
├── dependencies/
│   ├── Micro-XRCE-DDS-Agent/
│   └── PX4-Autopilot/
├── gazebo/
│   ├── models/
│   │   ├── inspection_car/
│   │   ├── inspection_person_marker/
│   │   └── inspection_stop_sign/
│   └── worlds/
├── logs/
├── ros2_ws/
│   └── src/
│       ├── px4_msgs/
│       ├── px4_orbit_inspection/
├── scripts/
│   ├── 00_check_ubuntu.sh
│   ├── 01_install_system_dependencies.sh
│   └── 02_download_sources.sh
└── student_logs/
```

The scripts are for initial setup only. Students run the actual simulation and experiments with normal PX4, Gazebo and ROS 2 commands.

---

Source and test ROS 2:

```bash
source /opt/ros/humble/setup.bash
ros2 doctor --report
```

Open `~/.bashrc` and add:

```bash
export INTERNSHIP_ROOT="$HOME/quard_um6p_intership"
export GZ_SIM_RESOURCE_PATH="$HOME/quard_um6p_intership/gazebo/models:$HOME/.gz/models${GZ_SIM_RESOURCE_PATH:+:$GZ_SIM_RESOURCE_PATH}"
```

# 3. Download the source stack

The project uses:

```text
PX4-Autopilot release/1.15
px4_msgs       release/1.15
```

Run once:

```bash
cd ~/quard_um6p_intership
chmod +x scripts/02_download_sources.sh
./scripts/02_download_sources.sh
```

---

## 4. Shell environment

Open a new terminal and inspect the project environment:

```bash
cd ~/quard_um6p_intership
source config/project.env

printf "INTERNSHIP_ROOT=%s\n" "${INTERNSHIP_ROOT}"
printf "PX4_DIR=%s\n" "${PX4_DIR}"
printf "ROS2_WS=%s\n" "${ROS2_WS}"
printf "DDS_AGENT_DIR=%s\n" "${DDS_AGENT_DIR}"
```

ROS 2 must be sourced in every terminal that runs a ROS 2 command:

```bash
source /opt/ros/humble/setup.bash
```

Activate the Python environment in terminals that run Python or the educational ROS 2 Python packages:

```bash
source /home/<user_name>/px4-venv/bin/activate
```

Verify it:

```bash
python -c "import sys, numpy; print(sys.executable); print(numpy.__version__)"
```

Expected:

```text
/home/<user_name>/px4-venv/bin/python
1.26.4
```

### Optional `.bashrc` convenience

These lines may be added once to `~/.bashrc`:

```bash
# ROS 2 base environment
source /opt/ros/humble/setup.bash

# Internship project root
export INTERNSHIP_ROOT="$HOME/quard_um6p_intership"

# Custom Gazebo models. Keep any existing resource path.
export GZ_SIM_RESOURCE_PATH="$HOME/.gz/models${GZ_SIM_RESOURCE_PATH:+:$GZ_SIM_RESOURCE_PATH}"
```

Use the same uppercase variable name, `INTERNSHIP_ROOT`, everywhere. Linux environment-variable names are case-sensitive.

Reload the shell only after editing:

```bash
source ~/.bashrc
```

---

## 5. Verify the downloaded branches

Because scripts 00, 01 and 02 have already run, verify instead of restarting from zero:

```bash
cd ~/quard_um6p_intership
source config/project.env

git -C "${PX4_DIR}" branch --show-current
git -C "${ROS2_WS}/src/px4_msgs" branch --show-current
git -C "${DDS_AGENT_DIR}" branch --show-current
```

Expected:

```text
release/1.15
release/1.15
master
```

Record exact commits for reproducibility:

```bash
git -C "${PX4_DIR}" rev-parse HEAD
git -C "${ROS2_WS}/src/px4_msgs" rev-parse HEAD
git -C "${DDS_AGENT_DIR}" rev-parse HEAD
```

Compare them with the commit files under `config/`.

---

## 6. Verify Python, ROS 2, YOLO and CUDA

Activate both ROS 2 and the Python environment:

```bash
source /opt/ros/humble/setup.bash
source /home/<user_name>/px4-venv/bin/activate
```

Run:

```bash
python -c "import rclpy; print('rclpy OK')"
python -c "from sensor_msgs.msg import Image; print('sensor_msgs OK')"
python -c "from cv_bridge import CvBridge; print('cv_bridge OK')"
python -c "from ultralytics import YOLO; print('Ultralytics YOLO OK')"
python -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('Device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

CUDA is optional. If it is unavailable, use CPU inference and reduce the model or image size.

---

## 7. Build only the educational ROS 2 packages

Do this when a package was added or its Python/launch/configuration files changed:

```bash
cd ~/quard_um6p_intership
source config/project.env
source /opt/ros/humble/setup.bash
source /home/<user_name>/px4-venv/bin/activate
cd "${ROS2_WS}"

colcon build \
  --symlink-install \
  --packages-select px4_orbit_inspection

source install/setup.bash
```

If `inspection_yolo` is present as a ROS 2 package, build both:

```bash
colcon build \
  --symlink-install \
  --packages-select px4_orbit_inspection inspection_yolo

source install/setup.bash
```

Verify package discovery:

```bash
ros2 pkg executables px4_orbit_inspection
ros2 pkg executables inspection_yolo 2>/dev/null || true
```

---

# 8. Run the full pipeline in Terminator

Open a Terminator window and split it into at least six terminals. Run the terminals in the order below.

---

## Terminal 1 - Micro XRCE-DDS Agent

```bash
cd ~/quard_um6p_intership
source config/project.env
cd "${DDS_AGENT_DIR}"

MicroXRCEAgent udp4 -p 8888
```

Keep this terminal running. The agent connects PX4's uXRCE-DDS client to ROS 2 over UDP.

---

## Terminal 2 - PX4 v1.15 and Gazebo with `x500_depth`

```bash
cd ~/quard_um6p_intership
source config/project.env
cd "${PX4_DIR}"

PX4_SYS_AUTOSTART=4002 \
PX4_GZ_MODEL=x500_depth \
./build/px4_sitl_default/bin/px4
```

The empty world is expected. It confirms that PX4 and the `x500_depth` model started before the inspection objects are added.

### Optional custom Gazebo spawn pose

Use this only if the matching object coordinates and orbit center were designed around that pose:

```bash
PX4_SYS_AUTOSTART=4002 \
PX4_GZ_MODEL_POSE="283.08,-136.22,3.86,0.00,0,-0.7" \
PX4_GZ_MODEL=x500_depth \
./build/px4_sitl_default/bin/px4
```

For the first student demonstration, spawning near the Gazebo origin is easier because Gazebo global coordinates and PX4 local coordinates are less confusing.

### Verify the ROS 2 connection

In a separate ROS 2 terminal after the Agent and PX4 are running:

```bash
source /opt/ros/humble/setup.bash
ros2 topic echo /fmu/out/vehicle_status --once
ros2 topic echo /fmu/out/vehicle_odometry --once
```

Do not begin autonomous flight if these topics are unavailable.

---

## Terminal 3 - Add inspection objects

First discover the running world name:

```bash
cd ~/quard_um6p_intership
source config/project.env

gz service -l | grep '/world/.*/create'
```

Normally:

```text
/world/default/create
```

The local demonstration layout is:

```text
                         Person marker
                            (0, 6)
                               ●

                               ↑ Gazebo +X or chosen map direction

       Stop-sign marker       DRONE/HOME          Car marker
          (-5, 2.5)             (0, 0)              (8, 0)
               ●                   ✈                   ●
```

The comments above are a conceptual plan. Use the Gazebo axis indicator to verify the actual world axes.

Set shared variables:

```bash
cd ~/quard_um6p_intership
source config/project.env

WORLD_NAME="default"
MODEL_DIR="$(pwd)/gazebo/models"
```

### Spawn the car marker

```bash
OBJECT_SDF="${MODEL_DIR}/inspection_car/model.sdf"

gz service \
  -s "/world/${WORLD_NAME}/create" \
  --reqtype gz.msgs.EntityFactory \
  --reptype gz.msgs.Boolean \
  --timeout 3000 \
  --req "
    name: 'inspection_car_instance',
    sdf_filename: '${OBJECT_SDF}',
    pose: {
      position: {x: 8.0, y: 0.0, z: 0.0},
      orientation: {w: 1.0, x: 0.0, y: 0.0, z: 0.0}
    }
  "
```

### Spawn the stop-sign marker

```bash
OBJECT_SDF="${MODEL_DIR}/inspection_stop_sign/model.sdf"

gz service \
  -s "/world/${WORLD_NAME}/create" \
  --reqtype gz.msgs.EntityFactory \
  --reptype gz.msgs.Boolean \
  --timeout 3000 \
  --req "
    name: 'inspection_stop_sign_instance',
    sdf_filename: '${OBJECT_SDF}',
    pose: {
      position: {x: -5.0, y: 2.5, z: 0.0},
      orientation: {w: 1.0, x: 0.0, y: 0.0, z: 0.0}
    }
  "
```

### Spawn the person marker

```bash
OBJECT_SDF="${MODEL_DIR}/inspection_person_marker/model.sdf"

gz service \
  -s "/world/${WORLD_NAME}/create" \
  --reqtype gz.msgs.EntityFactory \
  --reptype gz.msgs.Boolean \
  --timeout 3000 \
  --req "
    name: 'inspection_person_marker_instance',
    sdf_filename: '${OBJECT_SDF}',
    pose: {
      position: {x: 0.0, y: 6.0, z: 0.0},
      orientation: {w: 1.0, x: 0.0, y: 0.0, z: 0.0}
    }
  "
```

A successful response should include:

```text
data: true
```

If the world name differs, replace `default`. If a model already exists, use a new entity name or remove the old entity before spawning it again.

> The supplied geometric markers are pedagogical objects. A pretrained COCO YOLO model is not guaranteed to recognize them reliably as a car, person, or stop sign. Reliable pretrained-YOLO demonstrations require realistic, correctly textured objects, suitable camera distance, and appropriate lighting.

---

## Terminal 4 - Discover and bridge the RGB camera

Do not guess the camera topic. Discover it:

```bash
gz topic -l | grep -Ei 'camera|image|rgb|depth|points'
```

For the standard `x500_depth` model, the RGB image is commonly `/camera` and depth data is commonly `/depth_camera`, but use the names printed by the running simulation.

Inspect the candidate RGB topic:

```bash
gz topic -i -t /camera
```

Confirm that Gazebo is publishing messages:

```bash
gz topic -e -t /camera
```

Stop the binary-looking image output with `Ctrl+C`.

Now bridge the RGB topic to ROS 2:

```bash
source /opt/ros/humble/setup.bash

ros2 run ros_gz_image image_bridge /camera \
  --ros-args \
  -r /camera:=/camera/image_raw \
  -p qos:=sensor_data
```

An apparently silent bridge terminal is normal. Leave it running and verify from another terminal:

```bash
source /opt/ros/humble/setup.bash
ros2 topic list | grep camera
ros2 topic info /camera/image_raw --verbose
ros2 topic hz /camera/image_raw
```

Display the raw camera image before starting YOLO:

```bash
ros2 run rqt_image_view rqt_image_view /camera/image_raw
```

Do not proceed until an image is visible. If the camera sees only sky, ground, or empty space, change drone pose, camera angle, or object placement.

---

## Terminal 5 - Run the orbit mission

```bash
cd ~/quard_um6p_intership
source config/project.env
source /opt/ros/humble/setup.bash
source /home/<user_name>/px4-venv/bin/activate
source "${ROS2_WS}/install/setup.bash"

ros2 launch px4_orbit_inspection orbit_demo.launch.py
```

Start explicitly from another sourced ROS 2 terminal:

```bash
ros2 service call /orbit/start std_srvs/srv/Trigger "{}"
```

Abort and request landing:

```bash
ros2 service call /orbit/abort std_srvs/srv/Trigger "{}"
```

Inspect the package while it runs:

```bash
ros2 node info /orbit_controller
ros2 topic hz /fmu/in/trajectory_setpoint
ros2 topic echo /fmu/out/vehicle_odometry --once
```

### Orbit physics

For radius `R` and period `T`:

```text
angle(t) = 2*pi*t/T
North(t) = center_N + R*cos(angle)
East(t)  = center_E + R*sin(angle)
Down(t)  = -altitude
```

Tangential speed:

```text
v = 2*pi*R/T
```

Centripetal acceleration:

```text
a_c = v^2/R = 4*pi^2*R/T^2
```

Students should predict how reducing `T` changes tracking error and image quality before running the experiment.

---

## Terminal 6 - Run YOLO

### Preferred method: ROS 2 YOLO package

If `inspection_yolo` is present:

```bash
cd ~/quard_um6p_intership
source config/project.env
source /opt/ros/humble/setup.bash
source /home/<user_name>/px4-venv/bin/activate
source "${ROS2_WS}/install/setup.bash"

ros2 launch inspection_yolo inspection_yolo.launch.py \
  model_path:=/home/<user_name>/dev/yolov8m.pt \
  image_topic:=/camera/image_raw \
  output_csv:="$(pwd)/data/inspection_report.csv"
```

Inspect detections:

```bash
ros2 topic echo /inspection/detections
```

Display annotated images:

```bash
ros2 run rqt_image_view rqt_image_view /inspection/debug_image
```

### Compatibility method: existing standalone detector

Before running the existing script, verify which ROS topic it subscribes to:

```bash
cd ~/PX4-ROS2-Gazebo-YOLOv8

grep -nE 'create_subscription|image_raw|/camera|VideoCapture|CvBridge' uav_camera_det.py
```

If it subscribes to `/camera/image_raw`, run:

```bash
source /opt/ros/humble/setup.bash
source /home/<user_name>/px4-venv/bin/activate
source ~/quard_um6p_intership/ros2_ws/install/setup.bash
cd ~/PX4-ROS2-Gazebo-YOLOv8

python -u uav_camera_det.py
```

Use `python -u` so terminal output is not buffered.

Do not start a second `ros_gz_image` bridge in Terminal 6. Terminal 4 already owns the bridge. Multiple bridges make topic graphs and debugging unnecessarily confusing.

Check publisher/subscriber matching:

```bash
ros2 topic info /camera/image_raw --verbose
```

A working chain should show at least one publisher, the image bridge, and at least one subscriber, the YOLO node.

---

## Terminal 7 - Visualization and evidence

Raw image:

```bash
ros2 run rqt_image_view rqt_image_view /camera/image_raw
```

Annotated YOLO image:

```bash
ros2 run rqt_image_view rqt_image_view /inspection/debug_image
```

Node graph:

```bash
rqt_graph
```

Record a complete experiment:

```bash
cd ~/quard_um6p_intership
mkdir -p data/bags

ros2 bag record \
  -o data/bags/orbit_inspection_run_01 \
  /camera/image_raw \
  /inspection/debug_image \
  /inspection/detections \
  /fmu/out/vehicle_odometry \
  /fmu/out/vehicle_status \
  /fmu/in/trajectory_setpoint
```

Stop recording with `Ctrl+C` and confirm that the bag closes successfully.

---

# 9. Manual keyboard flight before autonomous flight

Keyboard flight is useful for camera exploration, but the exact command depends on the teleoperation package already installed in the project. Do not run an unknown keyboard node against PX4.

First inspect available executables:

```bash
ros2 pkg executables | grep -Ei 'teleop|keyboard|offboard'
```

Inspect the selected node and its expected message type before running it:

```bash
ros2 pkg executables <package_name>
ros2 interface show <message_type>
```

Recommended student sequence:

1. keep the DDS Agent, PX4, camera bridge and YOLO running;
2. use the already validated keyboard controller to take off and hover;
3. rotate slowly until a target becomes visible;
4. move toward and away from it;
5. observe detection confidence and bounding-box size;
6. land;
7. then repeat using `px4_orbit_inspection` for a reproducible trajectory.

Do not run manual keyboard control and autonomous orbit control simultaneously. Both may publish conflicting PX4 setpoints.

---

# 10. Camera orientation: recommended safe method

The PX4 v1.15 `x500_depth` model is documented as having a front-facing depth camera. Editing the model inside `dependencies/PX4-Autopilot` directly makes updates and reproducibility harder. Prefer a project-owned custom model, for example `x500_depth_down`, that includes the standard model and changes only the camera pose.

Before changing anything, locate the actual model used by your checkout:

```bash
cd ~/quard_um6p_intership
source config/project.env

find "${PX4_DIR}" "$HOME/.gz/models" \
  -path '*x500_depth*/model.sdf' \
  -o -path '*OakD-Lite*/model.sdf'
```

Inspect all relevant poses, not a hard-coded line number:

```bash
grep -n -B 3 -A 6 '<pose>' /path/to/x500_depth/model.sdf
```

The suggested change:

```xml
<pose>.12 .03 .242 0 0 0</pose>
```

to:

```xml
<pose>.15 .029 .21 0 0.7854 0</pose>
```

adds a pitch of `0.7854 rad`, approximately 45 degrees. Whether positive pitch points the optical axis down or up depends on the included camera model's frame convention. Therefore:

1. make a backup or custom model;
2. change the pose;
3. restart PX4/Gazebo;
4. bridge and display `/camera/image_raw`;
5. verify the direction visually;
6. if it points upward, test `-0.7854` instead;
7. document the final working sign and file path.

For a true nadir-looking camera, a pitch near 90 degrees may be appropriate, but verify frame conventions and avoid guessing. A 45-degree oblique view is usually more engaging for inspection because it can include both the ground target and surrounding context.

After modifying a cached model, fully restart the simulation. Do not modify the model while Gazebo is running and expect an already spawned entity to update.

---

# 11. Student experiments

## Experiment A - Confidence threshold

```bash
ros2 param get /yolo_detector confidence_threshold
ros2 param set /yolo_detector confidence_threshold 0.25
ros2 param set /yolo_detector confidence_threshold 0.70
```

Question: how do false detections and missed detections change?

## Experiment B - Process fewer frames

```bash
ros2 param set /yolo_detector inference_every_n_frames 1
ros2 param set /yolo_detector inference_every_n_frames 3
```

Question: what changes in inference load, output frequency and responsiveness?

## Experiment C - Orbit speed

Change the orbit period in the package YAML, rebuild only if required, restart the orbit node, and test 30 s, 24 s and 12 s.

Question: does faster motion increase trajectory error or reduce detection stability?

## Experiment D - Camera viewing angle

Compare forward-facing, 45-degree oblique and validated downward-facing camera orientations.

Question: which view produces the most continuous evidence during the selected inspection mission?

## Experiment E - Distance

Use keyboard control or change the orbit radius. Compare bounding-box area and confidence at multiple distances.

Question: is the closest view always the best view?

For every experiment, record:

```text
Prediction
One variable changed
Fixed conditions
Measured result
Failure or anomaly
Interpretation
Next experiment
```

---

# 12. Troubleshooting

## The image bridge terminal is silent

This is normally expected. Test the result from another terminal:

```bash
ros2 topic hz /camera/image_raw
ros2 topic info /camera/image_raw --verbose
```

## `/camera/image_raw` does not exist

Check the Gazebo topic first:

```bash
gz topic -l | grep -Ei 'camera|image|rgb|depth'
gz topic -i -t /camera
```

Then check that ROS 2 was sourced before running `image_bridge`.

## ROS topic exists but has no image frequency

Confirm Gazebo itself is publishing:

```bash
gz topic -e -t /camera
```

If Gazebo has no messages, the issue is before ROS 2: model, sensor, simulation pause state, or topic selection.

## YOLO runs but reports no detections

First display `/camera/image_raw`. Confirm that a realistic target is visible. Then test a lower threshold:

```bash
ros2 param set /yolo_detector confidence_threshold 0.25
```

A visible geometric shape is not automatically a valid pretrained-YOLO object.

## The standalone Python script prints nothing

Run unbuffered and verify its subscription:

```bash
python -u uav_camera_det.py
ros2 node list
ros2 topic info /camera/image_raw --verbose
```

## PX4 topics are missing

Verify:

```bash
pgrep -af MicroXRCEAgent
pgrep -af px4
ros2 topic list | grep '^/fmu/'
```

Confirm Agent port `8888`, matching PX4/`px4_msgs` branches, and the same ROS environment.

## PX4 will not enter Offboard mode

Confirm that `OffboardControlMode` and `TrajectorySetpoint` are continuously published before requesting Offboard mode:

```bash
ros2 topic hz /fmu/in/offboard_control_mode
ros2 topic hz /fmu/in/trajectory_setpoint
```

Inspect vehicle status and QGroundControl/preflight conditions.

## Object spawn returns false

Check:

```bash
test -f "${OBJECT_SDF}" && echo "SDF exists"
gz service -l | grep '/world/.*/create'
```

Use a unique entity name and the correct world name.

---

# 13. Clean shutdown

Preferred shutdown:

1. abort or land the drone;
2. stop YOLO with `Ctrl+C`;
3. stop rosbag cleanly with `Ctrl+C`;
4. stop the camera bridge;
5. stop PX4/Gazebo;
6. stop the DDS Agent.

Use normal signals before force-killing:

```bash
pkill -INT -x px4 || true
pkill -INT -f 'gz sim' || true
pkill -INT -x MicroXRCEAgent || true
```

Check remaining processes:

```bash
pgrep -af 'px4|gz sim|MicroXRCEAgent|image_bridge|uav_camera_det'
```

Use `pkill -9` only as a last resort because it prevents processes from cleaning up files and shared resources.

---

# 14. Final video plan

Record the final tutorial after the pipeline works without manual correction.

## Video chapter 1 - Installation and versions

Show:

```bash
lsb_release -a
ros2 --help
git -C "${PX4_DIR}" branch --show-current
git -C "${ROS2_WS}/src/px4_msgs" branch --show-current
git -C "${DDS_AGENT_DIR}" branch --show-current
python -c "import sys, numpy; print(sys.executable, numpy.__version__)"
```

Explain that Phase 3 does not reinstall validated dependencies.

## Video chapter 2 - Terminator layout

Show the six or seven terminals and name their responsibilities:

```text
1 DDS Agent
2 PX4 + Gazebo
3 Gazebo objects
4 Camera bridge
5 Orbit controller
6 YOLO
7 Visualization and recording
```

## Video chapter 3 - Data flow

Show:

```bash
rqt_graph
ros2 node list
ros2 topic list | grep -E 'fmu|camera|inspection'
```

## Video chapter 4 - Manual inspection

Use the validated keyboard controller to explore object distance and camera perspective. Do not run the orbit controller simultaneously.

## Video chapter 5 - Autonomous inspection

Start:

```bash
ros2 service call /orbit/start std_srvs/srv/Trigger "{}"
```

Show Gazebo, the raw image, the YOLO image and the detection topic.

## Video chapter 6 - Experiment

Change exactly one parameter, predict the effect, run the mission, and compare the evidence.

## Video chapter 7 - Results

Show:

```bash
head -n 10 data/inspection_report.csv
ros2 bag info data/bags/orbit_inspection_run_01
```

End with the engineering chain:

```text
Mission > Requirements > Architecture > Simulation > Programming
> Integration > Testing > Evidence > Demonstration
```

---

# 15. Definition of a successful Phase 3

Phase 3 is complete when:

- PX4 `release/1.15` and `px4_msgs release/1.15` are verified;
- DDS connects PX4 to ROS 2;
- the `x500_depth` drone appears and can fly;
- inspection objects appear in Gazebo;
- `/camera/image_raw` has a measurable frequency;
- the raw camera image is visible;
- YOLO publishes annotated images and detections;
- manual keyboard inspection works independently;
- autonomous orbit inspection works independently;
- no two controllers publish competing setpoints;
- a rosbag and inspection report are produced;
- students can explain coordinate frames, orbit speed, camera perspective, confidence threshold, false detections and system integration.
