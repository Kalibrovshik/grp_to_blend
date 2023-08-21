import bpy
import os
from bpy_extras.io_utils import ImportHelper

def menu_func(self, context):
    self.layout.operator("import.grp", text="GRP (.grp)")

def register():
    bpy.utils.register_class(ImportGRPOperator)
    bpy.types.TOPBAR_MT_file_import.append(menu_func)

def unregister():
    bpy.utils.unregister_class(ImportGRPOperator)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func)

class ImportGRPOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "import.grp"
    bl_label = "Import GRP"
    bl_options = {'REGISTER', 'UNDO'}
    
    filename_ext = "*.grp;*.fbx"
    filter_glob: bpy.props.StringProperty(
        default="*.grp;*.fbx",
        options={'HIDDEN'},
    )
    
    collections: bpy.props.StringProperty(name="Collections")
    filepath: bpy.props.StringProperty(name="File Path", subtype='FILE_PATH')
    files: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)
    @classmethod
    def poll(cls, context):
        return True
    
    def invoke(self, context, event):
        # Open the file selection window
        context.window_manager.fileselect_add(self)
        
        return {'RUNNING_MODAL'}
    
    def draw(self, context):
        layout = self.layout
        layout.template_list("UI_UL_list", "", self, "files", self, "file_index")
        layout.prop(self, "collections", text="Collections")
    
    def execute(self, context):
        print("Importing GRP:", self.filepath)
        selected_collections = ''
        selected_collections = selected_collections + self.collections
        print("Selected collections:", selected_collections)
        import os

        if self.files:
            ret = {'CANCELLED'}
            dirname = os.path.dirname(self.filepath)
            for file in self.files:
                path = os.path.join(dirname, file.name)
                from . import parse_grp
                file_name = bpy.path.display_name_from_filepath(self.filepath)
                original_extension = os.path.splitext(self.filepath)[1]
                grpfile_name = file_name + "." + "grp"
                grpfilepath = bpy.path.abspath(self.filepath)
                grpfilepath = grpfilepath.replace(file_name + original_extension, grpfile_name)
                parse_grp.rearrange(grpfilepath, selected_collections, self, context)
                ret = {'FINISHED'}
            return ret
        else:
            return {'FINISHED'}
                
        return {'FINISHED'}
        

if __name__ == "__main__":
    register()
