import bpy
import os
import re
def extract_text_between_markers(filename):
        extracted_blocks = []

        with open(filename, 'r') as file:
            start_marker = "<Object"
            end_marker = "</Object>"
            is_inside_block = False
            current_block = ""
            index = 0

            for line in file:
                if start_marker in line:
                    is_inside_block = True
                    current_block = line
                elif is_inside_block:
                    current_block += line

                if end_marker in line:
                    is_inside_block = False
                    extracted_blocks.append((index, current_block.strip()))
                    index += 1
                    current_block = ""

        return extracted_blocks
def rearrange(filename, selected_collections, operator, context):
    path = filename
    blocks = extract_text_between_markers(path)
    current_block = ['', '', '', '', '']
    for b in blocks:
        next_block = ['', '', '', '', '']
        keywords = operator.as_keywords(ignore=("filter_glob", "directory", "ui_tab", "filepath", "files", "collections"))
        try:
            tstr = ''.join(b[1])
            #res = re.search(r"\\([^\\]+)\." , tstr)
            res = re.search(r"Prefab=([^.]+)" , tstr)
            name_proxy = res.group(1)
            next_block[0] = name_proxy.replace('"', '')
            #name_proxy.replace('"', '')
            res = re.search(r'Name="([^"]+)"' , tstr)
            next_block[1] = res.group(1)
            res = re.search(r'Pos="([^"]+)"' , tstr)
            next_block[2] = res.group(1)
            res = re.search(r'Scale="([^"]+)"' , tstr)
            next_block[3] = res.group(1)
            res = re.search(r'Rotate="([^"]+)"' , tstr)
            next_block[4] = res.group(1)
    
            current_block = next_block
            from . import import_fbx
            original_extension = "grp"
            file_name = current_block[0]
            fbxfile_name = '\\' + file_name + "." + "fbx" #FBX BLOCK
            dirname = os.path.dirname(operator.filepath)
            fbxfilepath = dirname + fbxfile_name
            try:
                if import_fbx.load(operator, context, filepath = fbxfilepath, **keywords) == {'FINISHED'}:
                    for duplicated_obj in bpy.context.selected_objects:
                        if duplicated_obj.type == 'MESH':
                            bpy.context.view_layer.objects.active = duplicated_obj
                            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                            duplicated_obj.name = current_block[1]
                            loc = current_block[2].split(",", 2)
                            duplicated_obj.location = (float(loc[0]), float(loc[1]), float(loc[2]))
                            sca = current_block[3].split(",", 2)
                            duplicated_obj.scale = (float(sca[0]), float(sca[1]), float(sca[2]))
                            duplicated_obj.rotation_mode = 'QUATERNION'
                            rot = current_block[4].split(",", 3)
                            duplicated_obj.rotation_quaternion = (float(rot[0]), float(rot[1]), float(rot[2]), float(rot[3]))
                            scene = bpy.context.scene
                            scene.collection.objects.link(duplicated_obj)
                            collection = bpy.data.collections.get(selected_collections)
                            current_collections = duplicated_obj.users_collection[:] #currentcollectionchecker
                            for current_collection in current_collections:
                                current_collection.objects.unlink(duplicated_obj)
                            scene.collection.objects.link(duplicated_obj)
                            if collection is None:
                                collection = bpy.data.collections.new(selected_collections)
                                if collection.name not in scene.collection.children:
                                    scene.collection.children.link(collection)
                            collection.objects.link(duplicated_obj)
                        else:
                            objs = bpy.data.objects
                            objs.remove(objs[duplicated_obj.name], do_unlink=True)
            except:
                operator.report({'ERROR'}, "FBX IMPORT FAILED")
        except:
            operator.report({'ERROR'}, "BLOCK READING FAILED")
            print("invalid type")
