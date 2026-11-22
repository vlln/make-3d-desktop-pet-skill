"""Inspect a local asset in a disposable Blender process; never save the scene."""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import addon_utils
import bpy


def enable_vrm():
    matches = [m.__name__ for m in addon_utils.modules()
               if m.__name__ == "io_scene_vrm" or (m.__name__.startswith("bl_ext.")
                                                     and m.__name__.endswith(".vrm"))]
    if len(matches) != 1:
        raise RuntimeError(f"Install or keep one enabled VRM add-on: {matches}")
    name = matches[0]
    if not addon_utils.check(name)[1]:
        if bpy.ops.preferences.addon_enable(module=name) != {"FINISHED"}:
            raise RuntimeError(f"Cannot enable {name}")
    if not hasattr(bpy.types.Armature, "vrm_addon_extension"):
        raise RuntimeError(f"VRM properties did not register: {name}")
    return name


def inspect_mesh(obj):
    mesh = obj.data
    polygons = Counter(len(face.vertices) for face in mesh.polygons)
    mesh.calc_loop_triangles()
    rigs = [m.object for m in obj.modifiers if m.type == "ARMATURE" and m.object]
    deform = {b.name for rig in rigs for b in rig.data.bones if b.use_deform}
    groups = {g.index for g in obj.vertex_groups if g.name in deform}
    totals = [sum(g.weight for g in v.groups if g.group in groups) for v in mesh.vertices] if rigs else []
    return {
        "name": obj.name,
        "location_world": list(obj.matrix_world.translation),
        "dimensions_blender_units": list(obj.dimensions),
        "vertices": len(mesh.vertices),
        "faces": sum(polygons.values()),
        "faces_by_sides": dict(sorted(polygons.items())),
        "triangles": len(mesh.loop_triangles),
        "uv_layers": [layer.name for layer in mesh.uv_layers],
        "materials": [slot.name for slot in obj.material_slots],
        "shape_keys": [key.name for key in mesh.shape_keys.key_blocks] if mesh.shape_keys else [],
        "armature_modifiers": [rig.name for rig in rigs],
        "vertices_without_deform_weight": sum(t <= 1e-6 for t in totals) if rigs else None,
        "weighted_vertices_not_normalized": sum(t > 1e-6 and abs(t - 1) > 1e-3 for t in totals) if rigs else None,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("asset", type=Path, help=".blend, .glb, .gltf, .fbx or .vrm")
    parser.add_argument("report", type=Path, help="new JSON report path")
    parser.add_argument("--vrm", action="store_true", help="enable the installed VRM add-on in this process")
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
    asset, report = args.asset.resolve(strict=True), args.report.resolve()
    if not asset.is_file() or report.suffix.lower() != ".json" or report.exists():
        raise ValueError("Use a regular asset file and a new .json report path")
    suffix = asset.suffix.lower()
    if suffix not in {".blend", ".glb", ".gltf", ".fbx", ".vrm"}:
        raise ValueError(f"Unsupported format: {suffix}")
    mod = enable_vrm() if args.vrm or suffix == ".vrm" else None
    if suffix == ".blend":
        result = bpy.ops.wm.open_mainfile(filepath=str(asset), use_scripts=False)
    else:
        for obj in list(bpy.context.scene.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        if suffix == ".vrm":
            result = bpy.ops.import_scene.vrm(filepath=str(asset))
        elif suffix == ".fbx":
            result = bpy.ops.import_scene.fbx(filepath=str(asset))
        else:
            result = bpy.ops.import_scene.gltf(filepath=str(asset))
    if result != {"FINISHED"}:
        raise RuntimeError(f"Blender import did not finish: {result}")
    bpy.context.view_layer.update()
    scene = bpy.context.scene
    meshes = [inspect_mesh(o) for o in scene.objects if o.type == "MESH"]
    if not meshes:
        raise RuntimeError("No mesh objects in the active scene")
    armatures = []
    for obj in scene.objects:
        if obj.type == "ARMATURE":
            ext = getattr(obj.data, "vrm_addon_extension", None)
            armatures.append({"name": obj.name, "bones": len(obj.data.bones),
                              "vrm_spec": ext.spec_version if mod and ext else None})
    images = [{"name": i.name, "source": i.source, "path": i.filepath, "packed": bool(i.packed_file),
               "file_exists": Path(bpy.path.abspath(i.filepath, library=i.library)).is_file()
               if i.source == "FILE" and i.filepath and not i.packed_file else None}
              for i in bpy.data.images if i.users and i.source in {"FILE", "TILED", "GENERATED"}]
    report.parent.mkdir(parents=True, exist_ok=True)
    with report.open("x", encoding="utf-8") as handle:
        json.dump({"blender": bpy.app.version_string, "asset": asset.name, "vrm_addon": mod,
                   "scene": scene.name, "unit_scale": scene.unit_settings.scale_length,
                   "meshes": meshes, "armatures": armatures, "images": images}, handle, indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()
