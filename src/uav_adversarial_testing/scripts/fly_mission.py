"""
Minimal mission orchestrator — arm, takeoff, fly a square, land.
Connects to PX4 SITL via MAVSDK over UDP.
"""

import asyncio
from mavsdk import System
from mavsdk.mission import MissionItem, MissionPlan
from mavsdk.telemetry import LandedState


async def run():
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone connected")
            break

    print("Waiting for global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("Global position ok")
            break

    mission_items = []
    mission_items.append(MissionItem(
        latitude_deg=47.398039859999997,
        longitude_deg=8.5455725400000002,
        relative_altitude_m=10,
        speed_m_s=5,
        is_fly_through=True,
        gimbal_pitch_deg=float("nan"),
        gimbal_yaw_deg=float("nan"),
        camera_action=MissionItem.CameraAction.NONE,
        loiter_time_s=float("nan"),
        camera_photo_interval_s=float("nan"),
        acceptance_radius_m=1.0,
        yaw_deg=float("nan"),
        camera_photo_distance_m=float("nan"),
        vehicle_action=MissionItem.VehicleAction.NONE
    ))
    mission_items.append(MissionItem(
        latitude_deg=47.398036222362471,
        longitude_deg=8.5450146439425509,
        relative_altitude_m=10,
        speed_m_s=5,
        is_fly_through=True,
        gimbal_pitch_deg=float("nan"),
        gimbal_yaw_deg=float("nan"),
        camera_action=MissionItem.CameraAction.NONE,
        loiter_time_s=float("nan"),
        camera_photo_interval_s=float("nan"),
        acceptance_radius_m=1.0,
        yaw_deg=float("nan"),
        camera_photo_distance_m=float("nan"),
        vehicle_action=MissionItem.VehicleAction.NONE
    ))

    mission_plan = MissionPlan(mission_items)

    print("Uploading mission...")
    await drone.mission.upload_mission(mission_plan)

    print("Arming...")
    await drone.action.arm()

    print("Starting mission...")
    await drone.mission.start_mission()

    async for mission_progress in drone.mission.mission_progress():
        print(f"Mission progress: {mission_progress.current}/{mission_progress.total}")
        if mission_progress.current == mission_progress.total:
            print("Mission complete")
            break

    print("Landing...")
    await drone.action.land()

    print("Waiting for landed confirmation...")
    async for landed_state in drone.telemetry.landed_state():
        if landed_state == LandedState.ON_GROUND:
            print("Landed confirmed.")
            break

    print("Done.")


if __name__ == "__main__":
    asyncio.run(run())

