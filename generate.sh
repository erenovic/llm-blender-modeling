#!/bin/bash

DEFAULT_PROMPT="Write Blender Python to create a rustic chair with a wooden texture and dark green upholstery. The object should be realistic and many-polygon."
DEFAULT_OBJ_NAME="rustic_chair"

export PROMPT=${1:-$DEFAULT_PROMPT}
OBJ_NAME=${2:-$DEFAULT_OBJ_NAME}


BRIGHTNESS="Dark"

echo "Starting BlenderNet generation..."

source .venv/bin/activate

# Run with default config (prompt is now in the YAML file)
python -m src.main obj_name="$OBJ_NAME" brightness="$BRIGHTNESS"

# Or override specific values if needed:
# python -m src.main model_path="path/to/other/model"
