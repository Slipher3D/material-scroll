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

def register():
    from bpy.utils import register_class
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    from  bpy.utils import unregister_class
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
