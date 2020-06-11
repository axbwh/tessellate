bl_info = {
    "name": "tessellate",
    "description" : "Tool to instance object into complex tessellated grids",
    "author": "Al Bannwarth <alex@bannwarth.design>",
    "version": (0, 0, 1),
    "blender" : (2, 83, 0),
    "location" : "View3d > Tes",
    "warning": "This addon is still in development.",
    "doc_url" : "bannwarth.design",
    "category": "Object" }


import bpy
import math
from mathutils import Euler

def hex_get_coord(cx, cy, cz, r):
    return {
        "x" : r * 3 / 2 * cx,
        "y" : r * math.sqrt(3) * (cz + cx / 2)
    }


class TesPanel(bpy.types.Panel):
    bl_label = 'Tessellate'
    bl_idname = 'PT_Tessellate'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tes'
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.label(text='Tessellate', icon='LIGHTPROBE_GRID')
        #dev
        row.operator('script.reload', text='', icon='FILE_REFRESH')
        #end dev
        row = layout.row()
        row.operator('button.tes_hex')
        
class TesHex(bpy.types.Operator):
    bl_idname = "button.tes_hex" # translates to C-name BUTTON_OT_explode
    bl_label = "Tessellate Hexagonaly"
    bl_options = {"REGISTER", "UNDO"}
    
    recursion: bpy.props.IntProperty(
        name="Recursion",
        description="Number of tile recursion from center",
        min=2, soft_max=12, max=20,
        default=2,
    )

    size: bpy.props.FloatProperty(
        name="Size",
        description="Size ( Diameter ) of Tile",
        min=1, soft_max=10,
        default=1,
    )

    @classmethod
    def poll(cls, context):
        return context.collection is not None and context.collection is not context.scene.collection

    def execute(self, context):
        print(context.collection)
        col_scene = context.scene.collection
        
        tiles_name = context.collection.name + '_tiles'
        print(tiles_name)
        
        #create collection "tiles" if it doesn't already exists            
        if tiles_name not in bpy.data.collections:
            col_tiles = bpy.data.collections.new(tiles_name)
            
        col_tiles = bpy.data.collections[tiles_name]
        
        #move collection tiles_name to child of Scene
        if tiles_name not in col_scene.children :
            col_scene.children.link(col_tiles)

        if len(col_tiles.objects) > 0 :
            for obj in col_tiles.objects:
                print(obj.name)
                bpy.data.objects.remove(obj, do_unlink=True)

        
        recur = self.recursion
        radius = self.size / 2

        #for loop
        for col in range(-recur, recur + 1):
            row_start = max(-recur, -col - recur)
            row_end = min(recur, -col + recur)
            for row in range(row_start, row_end + 1):
                coord = hex_get_coord(col, row, -col -row, radius) 
                orient = ( ((row % 3) * 2 + col) % 3)
                rotation = orient * ((math.pi * 2) / 3)
                tile_id = f"tile_{col}_{row}"
                
                #add instance "tile" if it doesn't already exists  
                if tile_id not in bpy.data.objects:
                    instance = bpy.data.objects.new(
                        name=tile_id, 
                        object_data= None
                    )
                    
                #set "tile" as instance of selected collection    
                instance = bpy.data.objects[tile_id]
                instance.instance_collection = context.collection
                instance.instance_type = 'COLLECTION'
                instance.location.x = coord["x"]
                instance.location.z = coord["y"]
                instance.rotation_euler = Euler((0, rotation, 0), 'XYZ')
                
                if tile_id not in col_tiles.objects :
                    col_tiles.objects.link(instance)

                if col == 0 and row == 0:
                    instance.hide_set(True)
        
        return {'FINISHED'}

        
# def register():
#     bpy.utils.register_class(TesPanel)
#     bpy.utils.register_class(TesHex)
    
# def unregister():
#     bpy.utils.unregister_class(TesPanel)
#     bpy.utils.unregister_class(TesHex)
    
# if __name__ == "__main__":
#     register()
