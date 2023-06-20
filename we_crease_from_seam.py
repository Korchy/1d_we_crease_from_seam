# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/1d_we_crease_from_seam

import bmesh
import bpy
from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class

bl_info = {
    "name": "WE Crease from seam",
    "description": "Sets edges marked as UV-Seams with Mean Crease = 1.0 value",
    "author": "Nikita Akimov, Paul Kotelevets",
    "version": (1, 0, 0),
    "blender": (2, 79, 0),
    "location": "View3D > Tool panel > 1D > WE Crease from seam",
    "doc_url": "https://github.com/Korchy/1d_we_crease_from_seam",
    "tracker_url": "https://github.com/Korchy/1d_we_crease_from_seam",
    "category": "All"
}


# MAIN CLASS

class WECFS:

    @classmethod
    def set_crease(cls, context):
        # set Mean Crease to 1.0 for UVSeam edges
        # current mode
        mode = context.active_object.mode
        # switch to Edit mode
        if context.active_object.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='EDIT')
        # switch to edges mode
        context.tool_settings.mesh_select_mode = (False, True, False)
        # switch to Object mode
        bpy.ops.object.mode_set(mode='OBJECT')
        # deselect all data
        cls._deselect_all(obj_data=context.object.data)
        # select UV-Seam edges and set crease by them
        bm = bmesh.new()
        bm.from_mesh(context.object.data)
        bm.edges.ensure_lookup_table()
        # select seam edges
        seam_edges = [e for e in bm.edges if e.seam]
        for edge in seam_edges:
            edge.select = True
        # set crease
        crease_layer = bm.edges.layers.crease.verify()
        for edge in bm.edges:
            if edge.select:
                edge[crease_layer] = 1.0
        # save changed data to mesh
        bm.to_mesh(context.object.data)
        # return mode back
        bpy.ops.object.mode_set(mode=mode)

    @staticmethod
    def _deselect_all(obj_data):
        for polygon in obj_data.polygons:
            polygon.select = False
        for edge in obj_data.edges:
            edge.select = False
        for vertex in obj_data.vertices:
            vertex.select = False


# OPERATORS

class WECFS_OT_set_crease(Operator):
    bl_idname = 'wecfs.set_crease'
    bl_label = 'Set Crease'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        WECFS.set_crease(
            context=context
        )
        return {'FINISHED'}


# PANELS

class WECFS_PT_panel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "WE Crease from seam"
    bl_category = '1D'

    def draw(self, context):
        layout = self.layout
        layout.operator(
            operator='wecfs.set_crease',
            icon='BRUSH_CREASE'
        )


# REGISTER

def register():
    register_class(WECFS_OT_set_crease)
    register_class(WECFS_PT_panel)


def unregister():
    unregister_class(WECFS_PT_panel)
    unregister_class(WECFS_OT_set_crease)


if __name__ == "__main__":
    register()
