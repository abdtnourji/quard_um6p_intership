# QUARD UM6P Internship: Orbit Inspection with YOLO

This folder adds the student-facing ROS 2 work to the already working infrastructure. It does **not** reinstall PX4, Gazebo, DDS, ROS 2, CUDA, or YOLO.

## Existing infrastructure, unchanged

```text
dependencies/PX4-Autopilot       release/1.15
dependencies/Micro-XRCE-DDS-Agent master
ros2_ws/src/px4_msgs             release/1.15
```

## What students create and run

```text
Gazebo RGB camera
       |
       | direct command: ros_gz_image image_bridge
       v
/camera/image_raw
       |
       v
inspection_yolo/yolo_detector
       |                    |
       v                    v
/inspection/detections   /inspection/debug_image
       |
       v
inspection_reporter + PX4 odometry
       |
       v
data/inspection_report.csv

px4_orbit_inspection --> PX4 offboard setpoints --> orbit around inspection site
```

## Final repository structure

Copy the supplied directories into the project so the important tree becomes:

```text
quard_um6p_intership/
├── config/
│   └── project.env
├── data/
├── dependencies/
│   ├── Micro-XRCE-DDS-Agent/
│   └── PX4-Autopilot/
├── gazebo/
│   └── models/
│       ├── inspection_car/
│       ├── inspection_person_marker/
│       └── inspection_stop_sign/
├── logs/
├── ros2_ws/
│   └── src/
│       ├── px4_msgs/
│       ├── px4_orbit_inspection/
│       └── inspection_yolo/
├── student_guides/
│   ├── 01_discover_the_system.md
│   ├── 02_orbit_physics.md
│   ├── 03_camera_and_yolo.md
│   └── 04_inspection_experiments.md
└── student_logs/
```

## First check

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

## Build only the educational packages

```bash
cd ~/quard_um6p_intership
source config/project.env
source /opt/ros/humble/setup.bash
source /home/tnourji/px4-venv/bin/activate
cd "${ROS2_WS}"
colcon build --symlink-install --packages-select px4_orbit_inspection
source install/setup.bash
```

## Terminal 1: DDS Agent

Students type the actual command:

```bash
cd ~/quard_um6p_intership
source config/project.env
cd "${DDS_AGENT_DIR}"
MicroXRCEAgent udp4 -p 8888
```

## Terminal 2: PX4 and Gazebo

```bash
cd ~/quard_um6p_intership
source config/project.env
cd ./dependencies/PX4-Autopilot
PX4_GZ_MODEL=x500_depth \
./build/px4_sitl_default/bin/px4
```

pkill -9 px4
pkill -9 gzserver
pkill -9 gzclient
pkill -9 ignition
pkill -9 ruby
pkill -9 gazebo

The empty world is expected. The inspection objects are spawned next.

## Terminal 3: add objects to the running empty world

First discover the actual world name:

```bash
source config/project.env
gz service -l | grep '/world/.*/create'
```

Normally it is `/world/default/create`. Spawn three objects with direct Gazebo commands:

```text
                         Person
                       (0.0, 6.0)
                           ●

                           ↑ North

          Stop sign       DRONE           Car
          (-5.0, 2.5)     (0, 0)        (6.0, 0.0)
              ●              ✈               ●
```

```bash
cd ~/quard_um6p_intership
source config/project.env


WORLD_NAME="default"
MODEL_DIR="$(pwd)/gazebo/models"


OBJECT_SDF="${MODEL_DIR}/inspection_car/model.sdf"
```

```bash
gz service \
  -s "/world/${WORLD_NAME}/create" \
  --reqtype gz.msgs.EntityFactory \
  --reptype gz.msgs.Boolean \
  --timeout 3000 \
  --req "
    name: 'inspection_car_instance',
    sdf_filename: '${OBJECT_SDF}',
    pose: {
      position: {
        x: 8.0,
        y: 0.0,
        z: 0.0
      },
      orientation: {
        w: 1.0,
        x: 0.0,
        y: 0.0,
        z: 0.0
      }
    }
  "

```

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
      position: {
        x: -5.0,
        y: 7.5,
        z: 0.0
      },
      orientation: {
        w: 1.0,
        x: 0.0,
        y: 0.0,
        z: 0.0
      }
    }
  "
```

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
      position: {
        x: 0.0,
        y: 2.0,
        z: 0.0
      },
      orientation: {
        w: 1.0,
        x: 0.0,
        y: 0.0,
        z: 0.0
      }
    }
  "
```

````

If the world is not named `default`, replace `/world/default/create` with the service name printed by the discovery command.

## Terminal 4: discover and bridge the RGB camera

Do not guess the Gazebo topic:

```bash
gz topic -l | grep -E 'camera|image'
````

Display topic details:

```bash
gz topic -i -t /camera
```

For the PX4 v1.15 `x500_depth` model, the RGB topic is commonly `/camera`. Bridge the discovered RGB topic:

```bash
source /opt/ros/humble/setup.bash
ros2 run ros_gz_image image_bridge /camera \
  --ros-args -r /camera:=/camera/image_raw
```

Verify:

```bash
ros2 topic hz /camera/image_raw
ros2 topic info /camera/image_raw
```

## Terminal 5: start the orbit data aquisition

```bash
cd ~/quard_um6p_intership
source config/project.env
source /opt/ros/humble/setup.bash
source /home/tnourji/px4-venv/bin/activate
source "${ROS2_WS}/install/setup.bash"
ros2 launch px4_orbit_inspection orbit_demo.launch.py
```

## Terminal 6: start the orbit
Start the mission explicitly:

```bash
ros2 service call /orbit/start std_srvs/srv/Trigger "{}"
```



## Terminal 7: start camera bridge

```bash
ros2 run ros_gz_image image_bridge /camera --ros-args -p qos:=sensor_data
```

## Terminal 7: start YOLO

```bash
source ~/px4-venv/bin/activate
python uav_camera_det.py
```

Abort and request landing:

```bash
ros2 service call /orbit/abort std_srvs/srv/Trigger "{}"
```

---

make the drone camera look down
source /opt/ros/humble/setup.bash
export GZ_SIM_RESOURCE_PATH=~/.gz/models

Additional Configs
Put below lines in your bashrc:
source /opt/ros/humble/setup.bash
export GZ_SIM_RESOURCE_PATH=~/.gz/models
Copy the content of models from main repo to ~/.gz/models
Copy default.sdf from worlds folder in the main repo to ~/PX4-Autopilot/Tools/simulation/gz/worlds/
Change the angle of Drone's camera for better visual:

# Go to ~/PX4-Autopilot/Tools/simulation/gz/models/x500_depth/model.sdf then change <pose> tag in line 9 from:

<pose>.12 .03 .242 0 0 0</pose>
to:
<pose>.15 .029 .21 0 0.7854 0</pose>
