import bpy
import json
from bpy.types import SpaceView3D, Quaternion, Matrix
from bpy.app.handlers import persistent


"""
 2. offset each camera rotation view to make it square
 3. change initial view_distance to match maximum view potential
 4. rotate each camera view with view_rotation.rotate() to make it 90 degree offsets with 45 degree offsets
with respect to the y axis
 5. From there each rotation from the view rotation changes objects[].rotation_euler
"""

def duplicate_window(window_type: str = 'INVOKE_DEFAULT') -> None:
    """Duplicates a new window into bpy.data.screens from current active window."""
    context_window = bpy.context.copy()
    context_window['area'] = [area for area in bpy.context.screen.areas if area.type == 'VIEW_3D'][0]
    bpy.ops.screen.area_dupli(context_window, window_type)


def convert_quadview(area: SpaceView3D) -> None:
    """Converts a given window into quad-view."""
    region = [region for region in RENDER_AREA.regions if region.type == 'WINDOW'][0]
    override = {'area': RENDER_AREA, 'region': region, 'edit_object': bpy.context.edit_object}
    bpy.ops.screen.region_quadview(override)


def configure_scene(screen_data: SpaceView3D) -> None:
    """Removes all overlay elements from the 3D viewport."""
    screen_data.shading.background_type = 'VIEWPORT'
    screen_data.shading.background_color = (0, 0, 0)
    screen_data.overlay.show_overlays = False
    for attribute in 'show_gizmo', 'show_region_toolbar', 'show_region_tool_header':
        setattr(screen_data, attribute, False)

# if __name__ == '__main__':
duplicate_window()
RENDER_AREA = bpy.data.window_managers[0].windows[-1].screen.areas[0]
QUAD_VIEWS = RENDER_AREA.spaces[0].region_quadviews
convert_quadview(area=RENDER_AREA)
configure_scene(screen_data=RENDER_AREA.spaces[0])

def initial_config(values: json):
    with open('config/init.json') as file:
        config = json.load(file)
    for index, window in enumerate(config):
        for key, attribute in window.values():
            setattr(QUAD_VIEWS[index], key, attribute)


# bpy.data.window_managers[0].windows[1].screen.areas[0].spaces[0].region_3d.view_rotation.rotate(Euler((1, 10, .1)))

for window in bpy.data.window_managers[0].windows: # let's find what's what
    for area in window.screen.areas:
        if area.type == 'VIEW_3D':
            if len(area.spaces[0].region_quadviews) > 0: #if quadviews are active
                quad_views = area.spaces[0].region_quadviews
            else:
                main_view = area.spaces[0].region_3d

@persistent # This makes it stay if another file is opened
def update_handler(dummy):
    for every_view in quad_views:
        every_view.view_location = main_view.view_location
        every_view.view_distance = main_view.view_distance

    [area for area in bpy.data.window_managers[0].windows[0].screen.areas if area.type == 'VIEW_3D'][0]



bpy.app.handlers.frame_change_post.append(update_handler)
#bpy.app.handlers.scene_update_post.remove(update_handler)
