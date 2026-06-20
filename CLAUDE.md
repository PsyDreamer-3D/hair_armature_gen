# Hair Armature Generator

Blender 5.0.1 add-on. All source code lives in `hair_armature_gen/`.

See `../AGENTS.md` for project-wide development guidelines (hot-reload pattern, bpy.ops rules, structure conventions).
See `../hair-rig-scope.md` for the intended scope of this add-on and how it fits into the larger project.

## Key design decisions

- Boundary detection: dihedral angle threshold via bmesh (no sharp-edge markers)
- Centerline: PCA major axis (numpy SVD) per segment
- Root direction: segment endpoint closest to mesh bounding-box centroid
- Bone creation requires armature Edit Mode — wrapped in `context.temp_override`

## Testing

Install via Blender Preferences → Extensions → Install from Disk, pointing at the `hair_armature_gen/` folder.
In the 3D viewport N-panel, open "Hair Rig", pick a mesh with angular card geometry, and click "Generate Structural Rig".
