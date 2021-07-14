import bpy
import json
from bpy.types import SpaceView3D
from bpy.app.handlers import persistent
from mathutils import Quaternion, Matrix, Vector
from holo.gestures import prediction_from_camera


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


def initial_config(values: list) -> None:
    """Sets the camera position and rotation values during initialization of new frame."""
    for index, window in enumerate(values):
        for key, attribute in window.items():
            if key not in {'perspective_matrix', 'window_matrix'}: # BUG These values are read only and need a setter
                setattr(QUAD_VIEWS[index], key, attribute)

def transform_rotate(direction: 'str', confidence: int) -> None:
    """Given a direction and confidence value (Out of 100%), rotate the object by its corresponding vector."""
    magnitude = confidence / 100
    if direction not in {'retract', 'expand'}:
        bpy.ops.transform.rotate(
            value=magnitude,
            orient_axis='Z',
            orient_type='VIEW',
            orient_matrix=((0.85153, 0.277963, -0.44456),
                        (0.15535, 0.676067, 0.720278),
                        (0.500763, -0.6824, 0.53251)),
            orient_matrix_type='VIEW',
            mirror=True, use_proportional_edit=False,
            proportional_edit_falloff='SMOOTH',
            proportional_size=1,
            use_proportional_connected=False,
            use_proportional_projected=False)
    else:
        for window in QUAD_VIEWS:
            window.view_distance += magnitude if direction == 'expand' else magnitude * -1


def get_gestures() -> None:
    """Retrieves gestures from camera and applies the corresponding tranformation to the object."""
    rotation_mapping = {
        'Fist' : 'X',
        'L'    : 'Y',
        'Okay' : 'Z',
    }

    for gesture in prediction_from_camera():
        transform_rotate(direction=rotation_mapping(gesture.gesture), magnitude=gesture.confidence)


def initial_config_values() -> list:
    """Returns initial config values as a convenience utility."""
    return [
        {
            "view_distance": 4.183098793029785,
            "view_location": Vector((-0.8385156989097595, 0.05902576446533203, 0.48941677808761597)),
            "view_perspective": "PERSP",
            "view_rotation": Quaternion((0.6414357423782349, -0.6326250433921814, 0.3170725703239441, 0.2963286340236664))
        },
        {
            "view_distance": 4.183099269866943,
            "view_location": Vector((-0.4491613209247589, 1.5609432458877563, 0.014791678637266159)),
            "view_perspective": "PERSP",
            "view_rotation": Quaternion((0.4915403723716736, 0.6154682636260986, -0.25714513659477234, -0.559877872467041)),
        },
        {
            "view_distance": 5.019718647003174,
            "view_location": Vector((-0.9179283380508423, -0.46830159425735474, 0.334771990776062)),
            "view_perspective": "PERSP",
            "view_rotation": Quaternion((-0.22622741758823395, 0.6814441084861755, -0.1789524108171463, 0.6726300716400146))
        },
        {
            "view_distance": 5.019718647003174,
            "view_location": Vector((0.797123372554779, 0.7804675102233887, 0.635741114616394)),
            "view_perspective": "PERSP",
            "view_rotation": Quaternion((0.687656581401825, 0.6367506384849548, -0.2974682152271271, 0.1821804791688919))
        }
    ]


if __name__ == '__main__':
    duplicate_window()
    RENDER_AREA = bpy.data.window_managers[0].windows[-1].screen.areas[0]
    MAIN_VIEW = [area for area in bpy.data.window_managers[0].windows[0].screen.areas if area.type == 'VIEW_3D'][0].spaces[0].region_3d
    QUAD_VIEWS = RENDER_AREA.spaces[0].region_quadviews
    convert_quadview(area=RENDER_AREA)
    configure_scene(screen_data=RENDER_AREA.spaces[0])
    initial_config(initial_config_values())
    get_gestures()


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
    for every_view in QUAD_VIEWS:
        every_view.view_location = MAIN_VIEW.view_location
        every_view.view_distance = MAIN_VIEW.view_distance

bpy.app.handlers.frame_change_post.append(update_handler)
