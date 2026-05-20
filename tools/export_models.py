from pathlib import Path

import bpy


ROOT = Path("/home/uwase/Downloads/plant/hero")
MODELS = ROOT / "models"


def export_selected(object_names, output_name):
    bpy.ops.object.select_all(action="DESELECT")
    for name in object_names:
        obj = bpy.data.objects.get(name)
        if obj is None:
            raise SystemExit(f"Missing object: {name}")
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

    bpy.ops.export_scene.gltf(
        filepath=str(MODELS / output_name),
        export_format="GLB",
        use_selection=True,
        export_apply=True,
        export_materials="EXPORT",
        export_yup=True,
    )


export_selected(["Meshy_Mesh1.0"], "pot_vase_model.glb")
export_selected(["Rough_Clay_Rectangular_Base"], "base_stone_model.glb")
export_selected(["Meshy_Mesh1.0", "Rough_Clay_Rectangular_Base"], "pot_vase_and_base.glb")
print("Exported hero GLB models")
