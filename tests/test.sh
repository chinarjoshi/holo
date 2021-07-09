#!/usr/bin/env bash
set -euo pipefail

blender ../objects/cube.blend --python ../holo/blender.py
