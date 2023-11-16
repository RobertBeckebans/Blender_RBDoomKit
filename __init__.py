
bl_info = {
	'name': "RBDoomKit",
	'description': "RBDOOM-3-BFG Mapping Toolkit",
	'author': "Robert Beckebans",
	'blender': (3, 4, 0),
	'category': "Game Engine",
	'tracker_url': "https://github.com/RobertBeckebans/Blender_RBDoomKit"
	}
	

#import typing
import os
import bpy
import json
import time

from bpy.props import (
        BoolProperty,
        FloatProperty,
        StringProperty,
        IntProperty,
        CollectionProperty)
from bpy.types import Context


tbpath = "C:\\Projects\\RBDOOM-3-BFG\\base\\_tb\\"

class RBDoomKitPreferences(bpy.types.AddonPreferences):
	bl_idname = __name__

	game_path = StringProperty(
        name='C:\\Projects\\RBDOOM-3-BFG\\',
        description='',
        default='',
        maxlen=1024,
        subtype='DIR_PATH')

	base_path = StringProperty(
        name='base',
        description='',
        default='',
        maxlen=1024,
        subtype='DIR_PATH')
	
	mod_path = StringProperty(
        name='base',
        description='',
        default='',
        maxlen=1024,
        subtype='DIR_PATH')


def prefs():
    return bpy.context.preferences.addons[__name__].preferences

class RBDoomKit_PT_UI(bpy.types.Panel):	
	"""RBDoomKit Panel Test!"""
	bl_label = "RBDoomKit"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_category = 'RBDoomKit'

	def draw(self, context):
		#addon_prefs = prefs()
		layout = self.layout
		box = layout.box()

		col = box.column(align=True)
		col.label(text="Material Tools:")
		row = col.row(align=True)
		op = col.operator("view3d.rbdoomkit_reloadmats", text="Reload Materials", icon="MOD_TRIANGULATE")
		#row = col.row(align=True)
		#row.prop(addon_prefs, 'set_base', text="")
		
		col.separator()
		col = self.layout.column(align = True)
		col2= self.layout.column(align = True)
		col2.label(text="RBDoomKit Beta")
		col2.enabled = False
		col2.label(text="send feedback to @RobertBeckebans!")



class RBDoomKit_ReloadMaterials(bpy.types.Operator):
	'''Reload Doom Materials'''
	bl_idname = "view3d.rbdoomkit_reloadmats"
	bl_label = "Reload Doom Materials"

	def execute(self, context: Context):
		print( 'Reloading Doom Materials' )

		jsonfilename = "C:\\Projects\\RBDOOM-3-BFG\\base\\_bl\\materials.json"

		start = time.time() 
		data = json.loads( open( jsonfilename ).read() )
		end = time.time()
		print( "loading {0} took {1} seconds".format( jsonfilename, ( end - start ) ) )

		doomMaterials = data["materials"]

		for mat in bpy.data.materials:
			if mat.name in doomMaterials:
				print( "updating material: ", mat.name )
				#mat.user_clear()
				#bpy.data.materials.remove( mat )

				mat.use_nodes = True
				matNodes = mat.node_tree.nodes
				matLinks = mat.node_tree.links

				matDisney = matNodes.get( "Principled BSDF" )

				doomMat = doomMaterials[mat.name]
				editorImage = doomMat["editorImage"]
				imgfilename = os.path.normpath( tbpath + editorImage + ".png" )

				if os.path.exists( imgfilename ):
					print( "found " + imgfilename )

					# create image and assign to material
					image = None
					if editorImage in bpy.data.images:
						image = bpy.data.images[ editorImage ]
					else:
						image = bpy.data.images.load( imgfilename )

					# create image node
					nodeTex = matNodes.new( "ShaderNodeTexImage" )
					nodeTex.image = image

					# create the texture coordinate
					nodeUV = matNodes.new( "ShaderNodeTexCoord" )

					matLinks.new( nodeTex.inputs["Vector"], nodeUV.outputs["UV"] )
					matLinks.new( matDisney.inputs["Base Color"], nodeTex.outputs["Color"] )
					matLinks.new( matDisney.inputs["Alpha"], nodeTex.outputs["Alpha"] )

		return {'FINISHED'}

classes = (
    RBDoomKitPreferences,
	RBDoomKit_PT_UI,
	RBDoomKit_ReloadMaterials
)


def register():
	for cls in classes:
	    bpy.utils.register_class(cls)

def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)

if __name__ == "__main__":
	register()
