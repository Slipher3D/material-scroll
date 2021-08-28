import bpy
from bpy.types import Operator

class Ms_OT_material_scroll(bpy.types.Operator):
    bl_idname = "object.ms_ot_material_scroll"
    bl_label = "ms_OT_material_scroll"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        A = context.active_object
        return A is not None and A.type == 'MESH'

    def menu_func(self):
        self.layout.operator(Ms_OT_material_scroll.bl_idname)

    def modal(self, context: bpy.types.Context, event: bpy.types.Event):

        modes = ['MATERIAL', 'MATERIAL SLOT', 'SELECTION']
        current_mode = context.scene.update_value_c_mode

        C, A, S, D, M = self.get_object_material_data()

        object_index = 0
        object_max = len(S) - 1
        ms_max = 1
        mat_max = 1

        try:
            object_index = S.index(A)
        except IndexError:
            print("Index not found for active object.")

        ms_index = self.get_ms_index(A)
        ms_max = self.get_ms_max(A, ms_max)
        mat_max = self.get_mat_max(M)
        mat_name = self.get_mat_name(A, ms_index)
        mat_index = self.get_mat_index(M, mat_name)

        self.set_header_text(context, A, mat_name, modes, current_mode, ms_index)


        if event.type == 'TAB' and event.value == 'RELEASE':

            if current_mode < len(modes) - 1:
                current_mode += 1
            else:
                current_mode = 0

            context.scene.update_value_c_mode = current_mode

            self.set_header_text(context, A, mat_name, modes, current_mode, ms_index)

        elif event.type == 'WHEELUPMOUSE' or event.type == 'LEFT_ARROW' and event.value == 'RELEASE':
            print(current_mode)
            if current_mode == modes.index('MATERIAL'):
                #change the materials
                if mat_index > 0:
                    mat_index -= 1
                    A.material_slots[ms_index].material = M[mat_index]
                    self.set_header_text(context, A, mat_name, modes, current_mode, ms_index)
                else:
                    mat_index = mat_max
                    A.material_slots[ms_index].material = M[mat_index]
                    self.set_header_text(context, A, mat_name, modes, current_mode, ms_index)
            elif current_mode == modes.index('MATERIAL SLOT'):
                #change material slot
                if ms_index > 0:
                    ms_index -= 1
                    A.active_material_index = ms_index
                    self.set_header_text(context, A, mat_name, modes, current_mode, ms_index)
                else:
                    ms_index = ms_max
                    A.active_material_index = ms_index
                    self.set_header_text(context, A, mat_name, modes, current_mode, ms_index)
            elif current_mode == modes.index('SELECTION'):
                if len(S) > 0:
                    if object_index > 0:
                        object_index -= 1
                    else:
                        object_index = object_max

                    C.view_layer.objects.active = S[object_index]

                    C, A, S, D, M = self.get_object_material_data()

                    if len(A.material_slots) < 1:
                        D.objects[object_index].data.materials.append(D.materials['MS Material'])

                    try:
                        ms_index = self.get_ms_index(A)
                        ms_max = self.get_ms_max(A, ms_max)
                        if len(M) > 1:
                            mat_max = len(M) - 1
                        mat_name = self.get_mat_name(A, ms_index)
                        mat_index = self.get_mat_index(M, mat_name)
                    except IndexError:
                        print("Probably don't have a material or material slot on this object")

                    if len(M) == 0:
                        mat_name = "NA"
                        mat_index = 0

                    self.set_header_text(context, A, mat_name, modes, current_mode, ms_index)

        elif event.type == 'WHEELDOWNMOUSE' or event.type == 'RIGHT_ARROW' and event.value == 'RELEASE':
            if current_mode == modes.index('MATERIAL'):
                if mat_index < mat_max:
                    mat_index += 1
                    A.material_slots[ms_index].material = D.materials[mat_index]
                    self.set_header_text(context, A, mat_name, modes, current_mode, ms_index)
                else:
                    mat_index = 0
                    A.material_slots[ms_index].material = D.materials[mat_index]
                    self.set_header_text(context, A, mat_name, modes, current_mode, ms_index)
            elif current_mode == modes.index('MATERIAL SLOT'):
                if ms_index < ms_max:
                    ms_index += 1
                    A.active_material_index = ms_index
                    self.set_header_text(context, A, mat_name, modes, current_mode, ms_index)
                else:
                    ms_index = 0
                    A.active_material_index = ms_index
                    self.set_header_text(context, A, mat_name, modes, current_mode, ms_index)
            elif current_mode == modes.index('SELECTION'):
                if len(S) > 0:
                    if object_index < object_max:
                        object_index += 1
                    else:
                        object_index = 0

                    C.view_layer.objects.active = S[object_index]

                    C, A, S, D, M = self.get_object_material_data()

                    if len(A.material_slots) < 1:
                        D.objects[object_index].data.materials.append(D.materials['MS Material'])

                    try:
                        ms_index = self.get_ms_index(A)
                        ms_max = self.get_ms_max(A, ms_max)
                        if len(M) > 1:
                            mat_max = len(M) - 1
                        mat_name = self.get_mat_name(A, ms_index)
                        mat_index = self.get_mat_index(M, mat_name)
                    except IndexError:
                        print("Probably don't have a material or material slot on this object")

                    if len(M) == 0:
                        mat_name = "NA"
                        mat_index = 0

                    self.set_header_text(context, A, mat_name, modes, current_mode, ms_index)


        elif event.type == 'LEFTMOUSE':
            context.area.header_text_set(None)
            return {'FINISHED'}
        elif event.type in {'ESC', 'RIGHTMOUSE'}:
            context.area.header_text_set(None)
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def get_ms_index(self, A):
        if len(A.material_slots) == 1:
            ms_index = 0
        else:
            ms_index = A.active_material_index
        return ms_index

    def get_mat_index(self, M, mat_name):
        mat_index = M.find(mat_name)
        return mat_index

    def get_mat_name(self, A, ms_index):
        mat_name = A.material_slots[ms_index].name
        return mat_name

    def get_mat_max(self, M):
        if len(M) > 1:
            mat_max = len(M) - 1
        else:
            mat_max = 0
        return mat_max

    def get_ms_max(self, A, ms_max):
        if len(A.material_slots) > 1:
            ms_max = len(A.material_slots) - 1
        else:
            ms_max = 0
        return ms_max

    def get_object_index(self, S, A, object_index):
        for index, s in enumerate(S):
            if A.name == s.name:
                object_index = index
        return object_index

    def get_object_material_data(self):
        C = bpy.context
        A = C.active_object
        S = C.selected_objects
        D = bpy.data
        M = D.materials

        return C,A,S,D,M

    def set_header_text(self, context, A, m_name, modes, current_mode, ms_index):
        context.area.header_text_set('Active Object: {}   Material Name: {}    Mode: {}    Material Slot Index: {}'.format(A.name, m_name, modes[current_mode], ms_index))

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}