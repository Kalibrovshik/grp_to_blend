bl_info = {
    "name": "GRP Import",
    "author": "Kalibrovshik",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "File > Import",
    "description": "Import GRP files",
    "category": "Import-Export",
}

if "bpy" in locals():
    import importlib
    if "import_grp" in locals():
        importlib.reload(import_grp)

import bpy
from . import import_grp


def register():
    import_grp.register()


def unregister():
    import_grp.unregister()


if __name__ == "__main__":
    register()
