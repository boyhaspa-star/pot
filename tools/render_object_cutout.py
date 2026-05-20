from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path("/home/uwase/Downloads/plant/hero")


def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


mesh_objs = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
coords = []
for obj in mesh_objs:
    coords.extend([obj.matrix_world @ Vector(corner) for corner in obj.bound_box])

min_v = Vector((min(c.x for c in coords), min(c.y for c in coords), min(c.z for c in coords)))
max_v = Vector((max(c.x for c in coords), max(c.y for c in coords), max(c.z for c in coords)))
center = (min_v + max_v) * 0.5
height = max_v.z - min_v.z
width = max_v.x - min_v.x

cam_data = bpy.data.cameras.new("TEMP_hero_cutout_camera")
cam = bpy.data.objects.new("TEMP_hero_cutout_camera", cam_data)
bpy.context.collection.objects.link(cam)
cam.location = (center.x + width * 0.08, center.y - 4.9, center.z + height * 0.15)
look_at(cam, (center.x - width * 0.04, center.y, center.z - height * 0.03))
cam.data.type = "ORTHO"
cam.data.ortho_scale = height * 1.03
bpy.context.scene.camera = cam

key_data = bpy.data.lights.new("TEMP_hero_cutout_key", "AREA")
key = bpy.data.objects.new("TEMP_hero_cutout_key", key_data)
bpy.context.collection.objects.link(key)
key.location = (center.x + width * 1.2, center.y - 2.2, max_v.z + height * 0.45)
look_at(key, center)
key.data.energy = 980
key.data.size = 3.1

fill_data = bpy.data.lights.new("TEMP_hero_cutout_fill", "AREA")
fill = bpy.data.objects.new("TEMP_hero_cutout_fill", fill_data)
bpy.context.collection.objects.link(fill)
fill.location = (center.x - width * 1.8, center.y - 2.8, center.z + height * 0.08)
look_at(fill, center)
fill.data.energy = 16
fill.data.size = 6.0

top_data = bpy.data.lights.new("TEMP_hero_cutout_top", "AREA")
top = bpy.data.objects.new("TEMP_hero_cutout_top", top_data)
bpy.context.collection.objects.link(top)
top.location = (center.x + width * 0.12, center.y - 1.1, max_v.z + height * 0.72)
look_at(top, center)
top.data.energy = 34
top.data.size = 5.8

scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
if hasattr(scene, "eevee"):
    scene.eevee.taa_render_samples = 64
scene.view_settings.view_transform = "Filmic"
scene.view_settings.look = "Medium High Contrast"
scene.view_settings.exposure = 0
scene.view_settings.gamma = 1
scene.render.resolution_x = 900
scene.render.resolution_y = 1100
scene.render.film_transparent = True
scene.render.filepath = str(ROOT / "outputs" / "hero_object_cutout.png")
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"

bpy.ops.render.render(write_still=True)
print(f"Rendered {scene.render.filepath}")
