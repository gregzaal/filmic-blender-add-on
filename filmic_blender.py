bl_info = {
    "name": "Install Filmic Blender",
    "description": "A simple add-on that can download and install Filmic Blender",
    "author": "Greg Zaal",
    "version": (0, 1),
    "blender": (2, 78, 0),
    "location": "Properties Editor > Scene > Color Management",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Render"}

import bpy
import os

url = "https://github.com/sobotka/filmic-blender/archive/master.zip"
cpath = os.path.join(os.path.dirname(bpy.app.binary_path), "2.78", "datafiles")
cmpath = os.path.join(cpath, "colormanagement")

def filmic_is_installed():
    # For now just check if readme from github exists. Probably a better way to do this.
    check_path = os.path.join(cmpath, 'README.md')
    return os.path.exists(check_path)

class FBDownloadFilmic(bpy.types.Operator):
    "Download and install Filmic Blender. Restart Blender when it's done"
    bl_idname='filmic_blender.get'
    bl_label='Get Filmic Blender'
    
    def execute(self,context):        
        td = bpy.app.tempdir
        if not os.path.exists(td):
            os.makedirs(td)

        from urllib.request import urlretrieve
        dfile = os.path.join(td, 'filmic_blender.zip')
        try:
            urlretrieve(url, dfile)
        except:
            self.report({'ERROR'}, "Failed to download Filmic Blender, maybe check your internet connection?")
            print ("URL:", url, "\nDownload Path:", dfile)
            return {'CANCELLED'}
        else:
            if os.path.exists(cmpath):
                opath = os.path.join(cpath, 'colormanagement_old')
                i = 1
                while os.path.exists(opath):
                    opath = os.path.join(cpath, 'colormanagement'+'_old'*i)
                    i += 1
                os.rename(cmpath, opath)

            import zipfile
            zfile = zipfile.ZipFile(dfile)
            zfile.extractall(os.path.join(cpath))
            zfile.close()
            os.rename(os.path.join(cpath, 'filmic-blender-master'), cmpath)

            self.report({'INFO'}, "Filmic Blender successfully installed! Now restart Blender")

        return {'FINISHED'}

def ui(self, context):
    if not filmic_is_installed():
        layout = self.layout
        box = layout.box()
        col = box.column(align=True)
        row = col.row()
        row.scale_y=1.5
        row.alignment = 'CENTER'
        row.operator('filmic_blender.get', icon='SEQ_CHROMA_SCOPE')
        row = col.row()
        row.alignment = 'CENTER'
        row.label("Please restart Blender when it's done")

def register():
    bpy.utils.register_module(__name__)
    bpy.types.SCENE_PT_color_management.prepend(ui)

def unregister():    
    bpy.utils.unregister_module(__name__)
    bpy.types.SCENE_PT_color_management.remove(ui)
    
if __name__ == "__main__":
    register()
