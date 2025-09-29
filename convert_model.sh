#!/bin/bash
QBITS=8

mlx_lm.convert \
    --hf-path FreedomIntelligence/BlenderLLM \
    -q \
    --mlx-path ./assets/models/blender-net-${QBITS} \
    --q-bits ${QBITS}
