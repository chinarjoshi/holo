import bpy


context = bpy.context.copy()

for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        context['area'] = area
        bpy.ops.screen.area_dupli(context, 'INVOKE_DEFAULT')
        bpy.ops.screen.region_quadview()
        break
else:
    raise Exception('Blender running in headless mode. No 3D view found.')
