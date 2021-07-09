#!/usr/bin/env bash
set -euo pipefail

blender ../objects/cube.obj --python ../holo/blender.py
