# Changelog

All notable changes to Hair Armature Generator will be documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [Unreleased]

---

## [0.1.0] — 2026-06-19

Initial release.

### Added

- **Segmentation** — dihedral-angle flood-fill via BMesh groups mesh faces into connected card sections. Boundary sensitivity is controlled by the **Angle Threshold** parameter.
- **PCA centerline** — per-segment principal component analysis (NumPy SVD) extracts the dominant axis of elongation, giving a clean centerline through each card regardless of orientation.
- **Vertex snapping** — sampled bone positions are snapped to the nearest vertex within the same segment using `mathutils.kdtree.KDTree`. Consecutive duplicates are removed to prevent zero-length bones.
- **Top-to-bottom orientation** — each bone chain runs from the highest Z endpoint (root/scalp end) to the lowest (tip), so bone tails consistently face downward.
- **`Bone_ROOT`** — a single root bone placed at the mesh bounding-box centre; all chains are parented to it.
- **Chain density controls** — **Max Chains** caps the total number of chains (largest segments kept first); **Min Separation** culls chains whose midpoints are closer together than the specified distance, eliminating stacked duplicates on layered card meshes.
- **Bones Per Chain** — sets the number of bones in each chain as a direct count (replaces a distance-based spacing approach).
- **Clear operator** — removes previously generated `Hair_Armature` objects to support re-running with adjusted settings.
- **N-panel UI** — "Hair Rig" tab in the 3D Viewport sidebar, with parameters grouped under Segmentation, Chain Density, and Bones sections.
- **Hot-reload support** — the standard `_needs_reload` guard in `__init__.py` enables Blender's Reload Scripts workflow during development.
