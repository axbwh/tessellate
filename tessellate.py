bl_info = {
    "name" : "Tessellate2D",
    "author" : "Al Bannwarth",
    "version" : (1, 0),
    "blender" : (2, 83, 0),
    "location" : "View3d > Tool",
    "warning" : "",
    "wiki_url" : "bannwarth.design",
    "category" : "Automation",
}

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
    bl_category = 'Cum'
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.label(text='Tessellate', icon='LIGHTPROBE_GRID')
        row = layout.row()
        row.operator('button.tes_hex')
        
class TesHex(bpy.types.Operator):
    bl_idname = "button.tes_hex" # translates to C-name BUTTON_OT_explode
    bl_label = "Tessellate Hexagonaly"
    bl_options = {"REGISTER", "UNDO"}
    
    recursion: bpy.props.IntProperty(
        name="Recursion",
        description="Number of tile recursion from center",
        min=2, max=10,
        default=2,
    )

    size: bpy.props.FloatProperty(
        name="Size",
        description="Size ( Diameter ) of Tile",
        min=1, max=10,
        default=1,
    )

    @classmethod
    def poll(cls, context):
        return context.collection is not None and context.collection is not context.scene.collection

    def execute(self, context):
        print(context.collection)
        col_scene = context.scene.collection
        
        #create collection "tiles" if it doesn't already exists            
        if "tiles" not in bpy.data.collections:
            #print('cumming')
            col_tiles = bpy.data.collections.new("tiles")
            
        col_tiles = bpy.data.collections["tiles"]
        
        #move collection "tiles" to child of Scene
        if "tiles" not in col_scene.children :
            col_scene.children.link(col_tiles)

        
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

        
def register():
    bpy.utils.register_class(TesPanel)
    bpy.utils.register_class(TesHex)
    
def unregister():
    bpy.utils.unregister_class(TesPanel)
    bpy.utils.unregister_class(TesHex)
    
if __name__ == "__main__":
    register()
