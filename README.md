# tessellate

Blender Tessellation Util

Still under development

Right now only handles rotational hexagonal tessellations, in the style of Escher's Reptiles (1943)

How to use :
  1. Install tessellate.py (Edit > Preferences > Add-ons > Install)
  2. In the 3D viewport, you'll get a 'Tes' tab, with a panel 'Tessellate' and a button 'Hexagonal'
  3. Create a grease pencil object at 0,0,0 coordinates, and put it in a collection
  4. Select the collection (not the object) and click 'Hexagonal'
      
      A new collection (named 'yourcollectionname_tiles') will be created with instances of your current collection, tiled across the ZX plane. 
      
      Use the redo panel to adjust the recursion (how many time to reapeat the pattern outwards) and size (how large each tile is)
      
      The more Instances (higher recursion) the slower the software will become.
      
  5. Start drawing
  6. If you want to change the recursion, delete the '_tiles" hierarchy ( right click > Delete Hierarchy) before re-clicking Hexagonal
  
