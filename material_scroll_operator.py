import bpy
from bpy.types import Operator

class Ms_OT_material_scroll(bpy.types.Operator):
    bl_idname = "object.ms_ot_material_scroll"
    bl_label = "ms_OT_material_scroll"

    @classmethod
    def poll(cls, context):
        A = context.active_object
        return A is not None and A.type == 'MESH'

    def menu_func(self, context):
        self.layout.operator(Ms_OT_material_scroll.bl_idname)

    def modal(self, context: bpy.types.Context, event: bpy.types.Event):

        C, A, S, D, M = self.get_object_material_data()

        object_index = 0
        object_max = len(S) - 1

        for index, s in enumerate(S):
            if A.name == s.name:
                object_index = index

        if A.material_slots is not None:

            try:
                ms_index = A.active_material_index
                if len(A.material_slots) > 1:
                    ms_max = len(A.material_slots) - 1
                if len(M) > 1:
                    mat_max = len(M) - 1
                mat_name = A.material_slots[ms_index].name
                mat_index = self.get_mat_index(M, mat_name)

                self.set_header_text(context, A, mat_name, mat_index, ms_index)
            except IndexError:
                print("Indexes out of bounds")
            
            if event.type == 'X':

                if object_index < object_max:
                    object_index += 1
                else:
                    object_index = 0

                C.view_layer.objects.active = S[object_index]

                C, A, S, D, M = self.get_object_material_data()

                try:
                    ms_index = A.active_material_index
                    if len(A.material_slots) > 1:
                        ms_max = len(A.material_slots) - 1
                    if len(M) > 1:
                        mat_max = len(M) - 1
                    mat_name = A.material_slots[ms_index].name
                    mat_index = self.get_mat_index(M, mat_name)
                except IndexError:
                    print("Probably don't have a material or material slot on this object")
                
                if len(A.material_slots) == 0:
                    ms_index = 0
                    mat_name = "NA"
                    mat_index = 0

                self.set_header_text(context, A, mat_name, mat_index, ms_index)
            
            if event.type == 'Z':

                if object_index > 0:
                    object_index -= 1
                else:
                    object_index = object_max

                C.view_layer.objects.active = S[object_index]

                C, A, S, D, M = self.get_object_material_data()

                try:
                    ms_index = A.active_material_index
                    if len(A.material_slots) > 1:
                        ms_max = len(A.material_slots) - 1
                    if len(M) > 1:
                        mat_max = len(M) - 1
                    mat_name = A.material_slots[ms_index].name
                    mat_index = self.get_mat_index(M, mat_name)
                except IndexError:
                    print("Probably don't have a material or material slot on this object")

                if len(A.material_slots) == 0:
                    ms_index = 0
                    mat_name = "NA"
                    mat_index = 0

                self.set_header_text(context, A, mat_name, mat_index, ms_index)

            if event.type == 'WHEELUPMOUSE':
                if event.ctrl:
                    if ms_index > 0:
                        ms_index -= 1
                        A.active_material_index = ms_index
                        self.set_header_text(context, A, mat_name, mat_index, ms_index)
                    else:
                        ms_index = ms_max
                        A.active_material_index = ms_index
                        self.set_header_text(context, A, mat_name, mat_index, ms_index)
                else:
                    if mat_index > 0:
                        mat_index -= 1
                        A.material_slots[ms_index].material = D.materials[mat_index]
                        self.set_header_text(context, A, mat_name, mat_index, ms_index)
                    else:
                        mat_index = mat_max
                        A.material_slots[ms_index].material = D.materials[mat_index]
                        self.set_header_text(context, A, mat_name, mat_index, ms_index)

            if event.type == 'WHEELDOWNMOUSE':
                if event.ctrl:
                    if ms_index < ms_max:
                        ms_index += 1
                        A.active_material_index = ms_index
                        self.set_header_text(context, A, mat_name, mat_index, ms_index)
                    else:
                        ms_index = 0
                        A.active_material_index = ms_index
                        self.set_header_text(context, A, mat_name, mat_index, ms_index)
                else:
                    if mat_index < mat_max:
                        mat_index += 1
                        A.material_slots[ms_index].material = D.materials[mat_index]
                        self.set_header_text(context, A, mat_name, mat_index, ms_index)
                    else:
                        mat_index = 0
                        A.material_slots[ms_index].material = D.materials[mat_index]
                        self.set_header_text(context, A, mat_name, mat_index, ms_index)

            elif event.type == 'LEFTMOUSE':
                context.area.header_text_set(None)
                return {'FINISHED'}
            elif event.type in {'ESC', 'RIGHTMOUSE'}:
                context.area.header_text_set(None)
                return {'CANCELLED'}

        else:
            print("No material slots exist.")
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def get_mat_index(self, M, m_name):
        for index, m in enumerate(M):
            if m_name == m.name:
                mat_index = index
        return mat_index

    def get_object_material_data(self):
        C = bpy.context
        A = C.active_object
        S = C.selected_objects
        D = bpy.data
        M = D.materials

        for s in S:
            if s.type != 'MESH':
                S.remove(s)

        return C,A,S,D,M

    def set_header_text(self, context, A, m_name, mat_index, ms_index):
        context.area.header_text_set('Active Object: {}   Material Name: {}    Material Index: {}    Material Slot Index: {}'.format(A.name, m_name, mat_index, ms_index))

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}