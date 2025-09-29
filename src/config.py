import math
from typing import List, Tuple

CAMERA_ANGLES = [
    (math.radians(315), math.radians(180), math.radians(135)),
    (math.radians(45), 0, math.radians(315)),
    (math.radians(315), math.radians(180), math.radians(45)),
    (math.radians(45), 0, math.radians(225)),
    (math.radians(315), math.radians(180), math.radians(225)),
    (math.radians(45), 0, math.radians(45)),
    (math.radians(315), math.radians(180), math.radians(315)),
    (math.radians(45), 0, math.radians(135))
]


BRIGHTNESS = {
    "Very Bright": (
        (125, 100.0, 75, 100.0, 125, 100.0, 75, 100.0),
        (80, 65.0, 50, 65.0, 80, 65.0, 50, 65.0),
        (80, 65.0, 50, 65.0, 80, 65.0, 50, 65.0)
    ),
    "Bright": (
        (175, 150.0, 125, 150.0, 175, 150.0, 125, 150.0),
        (125, 112.5, 100, 112.5, 125, 112.5, 100, 112.5),
        (125, 112.5, 100, 112.5, 125, 112.5, 100, 112.5)
    ),
    "Medium Bright": (
        (250, 212.5, 175, 212.5, 250, 212.5, 175, 212.5),
        (200, 160.0, 120, 160.0, 200, 160.0, 120, 160.0),
        (200, 162.5, 125, 162.5, 200, 162.5, 125, 162.5)
    ),
    "Dark": (
        (450, 350.0, 250, 350.0, 450, 350.0, 250, 350.0),
        (400, 275.0, 150, 275.0, 400, 275.0, 150, 275.0),
        (400, 275.0, 150, 275.0, 400, 275.0, 150, 275.0)
    ),
    "Very Dark": (
        (600, 500.0, 400, 500.0, 600, 500.0, 400, 500.0),
        (500, 400.0, 300, 400.0, 500, 400.0, 300, 400.0),
        (500, 400.0, 300, 400.0, 500, 400.0, 300, 400.0)
    )
}


def get_brightness(brightness: str) -> Tuple[List[float], ...]:
    assert brightness in BRIGHTNESS, f"Invalid brightness: {brightness}"
    return BRIGHTNESS[brightness]
