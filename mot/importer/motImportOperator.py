import bpy
from bpy.props import StringProperty, PointerProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper
import os

from .motImporter import importMot
from ..common.motUtils import getArmatureObject


collItems = []

def _coll_items(self, context):
    return collItems

def _update_coll_items():
    collItems.clear()

    collItems.append(("__auto__", "AUTO", ""))
    for coll in bpy.data.collections:
        collItems.append((coll.name, coll.name, ""))

class ImportNierMot(bpy.types.Operator, ImportHelper):
    """Import a Nier Animation mot file"""
    bl_idname = "import_scene.mot"
    bl_label = "Import Nier Animation Data"
    bl_options = {'UNDO'}

    filename_ext = ".mot"
    filter_glob: bpy.props.StringProperty(default="*.mot", options={'HIDDEN'})

    bulkImport: bpy.props.BoolProperty(name="Bulk Import", description="Import all mot files in the folder", default=False)
    targetCollection: bpy.props.EnumProperty(items=_coll_items, default=0, name="", description="")

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        col = layout.column()

        row = col.row(align=True)
        row.prop(self, "bulkImport")

        row = col.row(align=True)
        row.label(text="Target Collection")
        row = col.row(align=True)
        row.prop(self, "targetCollection", text="")

    def invoke(self, context, event):
        _update_coll_items()

        wm = context.window_manager
        wm.fileselect_add(self)

        return {'RUNNING_MODAL'}

    def execute(self, context):
        from .motImporter import importMot

        armarture = getArmatureObject(self.targetCollection)
        if armarture == None:
            self.report({'ERROR'}, "No valid armature found")
            return {'CANCELLED'}

        if not self.bulkImport:
            importMot(self.filepath, armarture, printProgress=not self.bulkImport)
        else:
            path = self.filepath if os.path.isdir(self.filepath) else os.path.dirname(self.filepath)
            allMotFiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith(".mot")]
            for i, file in enumerate(allMotFiles):
                print(f"Importing {file} ({i+1}/{len(allMotFiles)})")
                importMot(os.path.join(path, file), armarture, printProgress=not self.bulkImport)

        if self.bulkImport:
            print(f"Imported {len(allMotFiles)} mot files from {path}")
            self.report({'INFO'}, f"Imported {len(allMotFiles)} mot files")
        else:
            self.report({'INFO'}, "Imported mot file")

        return {'FINISHED'}
