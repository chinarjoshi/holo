import bpy
import sys
import os
import imp
import ray
import psutil

# HACK
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.apend(dir)

import gestures
imp.reload(gestures)


def gesture_recognition():
    for gesture in gestures.prediction_from_camera():
        print(gesture.gesture, gesture.confidence)

def update_split_view():
    pass

def open_window():
    context = bpy.context.copy()

    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            context['area'] = area
            break
    else:
        raise Exception('Blender running in headless mode. No 3D view found.')



def configure_toolbar():
    overlay['gpencil_grid_opacity'] = 0
    overlay['grid_lines'] = 0
    overlay['show_annotation'] = False
    overlay['show_floor'] = False

    for axis in 'x', 'y', 'z':
        overlay[f'show_axis_{axis}'] = False

if __name__ == '__main__':
    bpy.ops.screen.area_dupli(context, 'INVOKE_DEFAULT')
    bpy.ops.screen.area_split(context)
    overlay = bpy.types.View3DOverlay(context)

    nproc=psutil.cpu_count(logical=False)
    ray.init(num_cpu=nproc)
