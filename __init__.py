bl_info = {
    "name" : "MaterialScroll",
    "author" : "Slipher3D",
    "description" : "Change material and material slot by keyboard and mouse scroll.",
    "blender" : (2, 93, 1),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Object"
}

import bpy
from . material_scroll_operator import Ms_OT_material_scroll

classes = (Ms_OT_material_scroll,)

ms_keymaps = []

def register():
    from bpy.utils import register_class
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.update_value_c_mode = bpy.props.IntProperty(name='cmode', description='Current mode', default=0, min=0, max=2)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("object.ms_ot_material_scroll", type='C', value='PRESS', ctrl=True)
        ms_keymaps.append((km, kmi))

def unregister():

    for km, kmi in ms_keymaps:
        km.keymap_items.remove(kmi)
    ms_keymaps.clear()

    del bpy.types.Scene.update_value_modes
    del bpy.types.Scene.update_value_c_mode
    from  bpy.utils import unregister_class
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
