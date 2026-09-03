"""Pure mathematical functions used by the mission node and unit tests."""
import math


def smoothstep(u: float) -> float:
    """Smoothly move from 0 to 1 with zero slope at both ends."""
    u = max(0.0, min(1.0, u))
    return u * u * (3.0 - 2.0 * u)


def orbit_point(cx: float, cy: float, radius: float, angle: float):
    """Return North and East coordinates on a horizontal circle."""
    return cx + radius * math.cos(angle), cy + radius * math.sin(angle)


def inward_yaw(north: float, east: float, cx: float, cy: float) -> float:
    """Return NED yaw that points from the drone toward the circle center."""
    return math.atan2(cy - east, cx - north)


def tracking_error(desired, measured) -> float:
    """Return 3D Euclidean distance between two NED points."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(desired, measured)))
