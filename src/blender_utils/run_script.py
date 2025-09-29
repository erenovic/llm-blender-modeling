import logging
import os
import subprocess
import tempfile
from pathlib import Path
from typing import List, Tuple

# Set up logging
logger = logging.getLogger(__name__)


def run_script_and_save_obj(
    script: str, obj_name: str, output_folder: Path, blender_executable: Path
) -> Path:
    """Run Blender script to save the generated .obj file.

    Args:
        script: Blender Python script content
        obj_name: Name for the output object file
        output_folder: Directory to save the output file
        blender_executable: Path to Blender executable

    Returns:
        Path to the generated .obj file

    Raises:
        subprocess.CalledProcessError: If Blender execution fails
        FileNotFoundError: If the OBJ file is not created
    """
    output_folder.mkdir(parents=True, exist_ok=True)

    run_blender_script(
        script_content=script,
        name=obj_name,
        output_folder=output_folder,
        camera_locations=[],
        camera_rotations=[],
        brightness=(),
        blender_executable=blender_executable,
        save_obj=True,
    )

    obj_path = output_folder / f"{obj_name}.obj"
    if not obj_path.exists():
        raise FileNotFoundError(f"OBJ file was not created at expected path: {obj_path}")

    return obj_path


def run_blender_script(
    script_content: str,
    name: str,
    output_folder: Path,
    camera_locations: List[Tuple[float, float, float]],
    camera_rotations: List[Tuple[float, float, float]],
    brightness: Tuple[List[float], ...],
    blender_executable: Path,
    save_obj: bool = False,
    save_image: bool = False,
) -> None:
    """Run a Blender script with optional object export and image rendering.

    Args:
        script_content: Blender Python script content
        name: Base name for output files
        output_folder: Directory to save output files
        camera_locations: List of camera position tuples (x, y, z)
        camera_rotations: List of camera rotation tuples (x, y, z)
        brightness: Tuple containing brightness values for each camera view
        blender_executable: Path to Blender executable
        save_obj: Whether to export object as .obj file
        save_image: Whether to render and save images

    Raises:
        subprocess.CalledProcessError: If Blender execution fails
    """
    script_path = None
    try:
        script_path = _create_temp_script(
            script_content,
            output_folder,
            name,
            save_obj,
            save_image,
            camera_locations,
            camera_rotations,
            brightness,
        )
        logger.info(f"Created temporary script at: {script_path}")
        _execute_blender_script(blender_executable, script_path)
    finally:
        # Keep script for debugging if OBJ export was requested
        if script_path and os.path.exists(script_path) and not save_obj:
            os.remove(script_path)
        elif script_path and save_obj:
            logger.info(f"Keeping temporary script for debugging at: {script_path}")


def _create_temp_script(
    script_content: str,
    output_folder: Path,
    name: str,
    save_obj: bool,
    save_image: bool,
    camera_locations: List[Tuple[float, float, float]],
    camera_rotations: List[Tuple[float, float, float]],
    brightness: Tuple[List[float], ...],
) -> str:
    """Create a temporary Blender script file.

    Returns:
        Path to the created temporary script file
    """
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as temp_script:
        # Write initial setup
        temp_script.write("""import bpy
import os
import math

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

""")

        # Write main script content
        temp_script.write(script_content)
        temp_script.write("\n")  # Ensure there's a newline after the script content

        # Validate the script has no obvious syntax issues
        _validate_script_content(script_content)

        # Add object export if requested
        if save_obj:
            obj_export_path = output_folder / f"{name}.obj"
            temp_script.write(f"""
# Export the objects as OBJ
print("Exporting OBJ to: {obj_export_path}")
try:
    bpy.ops.export_scene.obj(filepath=r'{obj_export_path}')
    print("OBJ export completed successfully")
except Exception as e:
    print(f"Error exporting OBJ: {{e}}")
    raise e
""")

        # Add image rendering if requested
        if save_image:
            temp_script.write(
                _generate_rendering_script(
                    output_folder, name, camera_locations, camera_rotations, brightness
                )
            )

        # Log the script path for debugging
        logger.debug(f"Created temporary script at: {temp_script.name}")
        return temp_script.name


def _validate_script_content(script_content: str) -> None:
    """Validate that the script content appears to be complete Python code.

    Args:
        script_content: The generated script content to validate

    Raises:
        ValueError: If the script appears to be incomplete or invalid
    """
    lines = script_content.strip().split('\n')
    if not lines:
        raise ValueError("Script content is empty")

    last_line = lines[-1].strip()

    # Check for common signs of incomplete generation
    if (last_line.endswith('.') and not last_line.endswith('..') and
        not any(last_line.endswith(suffix) for suffix in ['.py', '.obj', '.png'])):
        raise ValueError(f"Script appears to be incomplete - ends with: '{last_line}'")

    # Try to compile the script to check for syntax errors
    try:
        compile(script_content, '<generated_script>', 'exec')
    except SyntaxError as e:
        raise ValueError(f"Generated script has syntax error: {e}")

    logger.info("Script validation passed")


def _generate_rendering_script(
    output_folder: Path,
    name: str,
    camera_locations: List[Tuple[float, float, float]],
    camera_rotations: List[Tuple[float, float, float]],
    brightness: Tuple[List[float], ...],
) -> str:
    """Generate the rendering portion of the Blender script.

    Returns:
        String containing the rendering script
    """
    script_parts = []

    for i, (camera_location, camera_rotation) in enumerate(zip(camera_locations, camera_rotations), 1):
        light_location = (camera_location[0] * 1.2, camera_location[1] * 1.2, camera_location[2] * 1.2)
        render_path = output_folder / f"{name}_view{i}.png"

        script_parts.append(f"""
# Camera and lighting setup for view {i}
camera = bpy.data.cameras.new('Camera_{i}')
cam_obj = bpy.data.objects.new('Camera_{i}', camera)
bpy.context.scene.collection.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj
cam_obj.location = {camera_location}
cam_obj.rotation_euler = {camera_rotation}

# Key light setup
key_light_data = bpy.data.lights.new(name='Key_Light_{i}', type='POINT')
key_light_object = bpy.data.objects.new(name='Key_Light_{i}', object_data=key_light_data)
bpy.context.collection.objects.link(key_light_object)
key_light_object.location = {light_location}
key_light_data.energy = {brightness[0][i - 1]}

# Render settings and execution
bpy.context.scene.render.film_transparent = True
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.filepath = r'{render_path}'
bpy.ops.render.render(write_still=True)
""")

    return "\n".join(script_parts)


def _execute_blender_script(blender_executable: Path, script_path: str) -> None:
    """Execute a Blender script using subprocess.

    Args:
        blender_executable: Path to Blender executable
        script_path: Path to the script file to execute

    Raises:
        subprocess.CalledProcessError: If Blender execution fails
    """
    command = [str(blender_executable), "--background", "--factory-startup", "--python", script_path]

    logger.info(f"Executing Blender command: {' '.join(command)}")

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logger.info("Blender script executed successfully")
        if result.stdout:
            logger.debug(f"Blender stdout: {result.stdout}")
        if result.stderr:
            logger.warning(f"Blender stderr: {result.stderr}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Blender execution failed with return code {e.returncode}")
        if e.stdout:
            logger.error(f"Blender stdout: {e.stdout}")
        if e.stderr:
            logger.error(f"Blender stderr: {e.stderr}")
        raise
