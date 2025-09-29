#!/bin/bash

PROMPT="Write Blender Python to create a rustic chair with a wooden texture and green upholstery..."
OBJ_NAME="rustic_chair"
BRIGHTNESS="Medium Bright"

echo "Starting BlenderNet generation..."

source .venv/bin/activate

# Run with default config (prompt is now in the YAML file)
python -m src.main prompt="$PROMPT" obj_name="$OBJ_NAME" brightness="$BRIGHTNESS"

# Or override specific values if needed:
# python -m src.main model_path="path/to/other/model"
