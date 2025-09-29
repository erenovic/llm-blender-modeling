import itertools
import math
from pathlib import Path
from typing import List, Tuple

from src.blender_utils.run_script import run_blender_script
from src.config import BRIGHTNESS, CAMERA_ANGLES


def parse_obj_file(file_path: Path) -> List[Tuple[float, float, float]]:
    vertices = []
    with open(file_path, "r") as file:
        for line in file:
            if line.startswith("v "):
                parts = line.split()
                vertices.append((float(parts[1]), float(parts[2]), float(parts[3])))
    return vertices


def calculate_bounding_box(file_path: Path) -> List[Tuple[float, float, float]]:
    vertices = parse_obj_file(file_path)

    min_x = min_y = min_z = float("inf")
    max_x = max_y = max_z = float("-inf")

    for x, y, z in vertices:
        min_x, max_x = min(min_x, x), max(max_x, x)
        min_y, max_y = min(min_y, y), max(max_y, y)
        min_z, max_z = min(min_z, z), max(max_z, z)

    delta_max = max(max_x - min_x, max_y - min_y, max_z - min_z)
    center = [(max_x + min_x) / 2, (max_y + min_y) / 2, (max_z + min_z) / 2]

    factor = 2.5 / math.sqrt(2)

    coords = []
    for i, j, k in itertools.product([-1, 1], repeat=3):
        x = center[0] + i * delta_max * factor
        y = center[2] + j * delta_max * factor
        z = center[1] + k * delta_max * 2.5
        coords.append((x, y, z))
    return coords


def run_script_and_render_image(
    script: str, obj_name: str, output_folder: Path, obj_path: Path, blender_executable: Path, brightness: str
) -> None:
    """Calculate bounding box and render the image using Blender script."""
    output_folder.mkdir(parents=True, exist_ok=True)

    bounding_coords = calculate_bounding_box(obj_path)
    brightness_value = BRIGHTNESS.get(brightness, BRIGHTNESS["Very Dark"])
    run_blender_script(
        script,
        obj_name,
        output_folder,
        bounding_coords,
        CAMERA_ANGLES,
        brightness_value,
        blender_executable,
        save_image=True,
    )
