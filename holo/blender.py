import bpy
from gestures import prediction_from_camera


context = bpy.context.copy()

for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        context['area'] = area
        break
else:
    raise Exception('Blender running in headless mode. No 3D view found.')


for gesture in prediction_from_camera():
    print(gesture.gesture, gesture.confidence)

bpy.ops.screen.area_dupli(context, 'INVOKE_DEFAULT')

bpy.ops.screen.area_split(context)

overlay = bpy.types.View3DOverlay(context)

overlay['gpencil_grid_opacity'] = 0
overlay['grid_lines'] = 0
overlay['show_annotation'] = False
overlay['show_floor'] = False

for axis in 'x', 'y', 'z':
    overlay[f'show_axis_{axis}'] = False
