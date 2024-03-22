import bpy
from math import radians

def objRotationWrapper(obj: bpy.types.Object):
	if obj.parent is not None \
		and abs(obj.parent.rotation_euler[0] - radians(90)) < 0.001 \
		and obj.rotation_euler[0] == 0:
		return

	# make invisible parent and inherit armature's transform
	# and rotate with 90° on x axis
	parentObj = bpy.data.objects.new("RotationWrapper", None)
	parentObj.hide_viewport = True
	parentObj.location = obj.location
	parentObj.rotation_mode = obj.rotation_mode
	parentObj.rotation_euler = (obj.rotation_euler[0] + radians(90), obj.rotation_euler[1], obj.rotation_euler[2])
	parentObj.scale = obj.scale

	# revert armature to default transform
	obj.location = (0, 0, 0)
	obj.rotation_mode = "XYZ"
	obj.rotation_euler = (0, 0, 0)
	obj.scale = (1, 1, 1)

	# Revert rotation if Z-up (rotation is made by GBFRBlenderTool)
	rootBone = obj.data.bones["_900"]
	if abs(rootBone.tail[2] - 0.05) < 0.001:
		obj.select_set(True)
		bpy.context.view_layer.objects.active = obj
		obj.rotation_euler[0] = radians(-90)
		bpy.ops.object.transform_apply(location=False, rotation=True, scale=False, properties=False, isolate_users=False)
		bpy.context.view_layer.objects.active = None
		obj.select_set(False)

	# link armature with new parent
	obj.users_collection[0].objects.link(parentObj)
	obj.parent = parentObj