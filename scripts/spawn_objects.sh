#!/usr/bin/env bash


# =============================================================================
# Project   : Quadcopter Autonomous Inspection (UM6P Internship)
# Author    : Dr. Abdellah TNOURJI
# Website   : https://www.abdellahtnourji.com/
# Date      : [Date, Aug 2026]

# License   : UM6P
# =============================================================================



PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

WORLD_NAME="default"


spawn()
{
    local NAME=$1
    local MODEL=$2
    local X=$3
    local Y=$4
    local Z=$5

    MODEL_SDF="${PROJECT_ROOT}/gazebo/models/${MODEL}/model.sdf"

    echo
    echo "Spawning ${NAME}"

    gz service \
      -s "/world/${WORLD_NAME}/create" \
      --reqtype gz.msgs.EntityFactory \
      --reptype gz.msgs.Boolean \
      --timeout 3000 \
      --req "
        name: '${NAME}',
        sdf_filename: '${MODEL_SDF}',
        pose: {
          position: {
            x: ${X},
            y: ${Y},
            z: ${Z}
          }
        }
      "
}


spawn inspection_car \
      inspection_hatchback \
      6.0 \
      0.0 \
      0.0

spawn inspection_pickup \
      inspection_pickup \
      -5.0 \
      2.0 \
      0.0

spawn inspection_person \
      inspection_person \
      0.0 \
      6.0 \
      0.0

echo
echo "Done."
