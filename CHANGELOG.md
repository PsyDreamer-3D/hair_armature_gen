# Changelog

All notable changes to Hair Armature Generator will be documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [Unreleased]

### Added

- **Generate Chain from Selection** — new operator that creates bone chains from manually selected vertices. Select vertices in Edit Mode, return to Object Mode, and click the button. Each separate group of selected vertices becomes its own chain; vertices are ordered by following connected edges from root to tip (falling back to longest-axis ordering for closed loops or branching shapes) and resampled evenly to **Bones Per Chain** bones.
- **Merge into Active Armature** — new toggle in the Output section. When enabled, both generation operators add their chains to the currently active armature object instead of creating a new one. An existing `Bone_ROOT` is reused if present; a new one is created otherwise. New bones are named to avoid conflicts with any bones already in the armature.

---

## [0.1.0] — 2026-06-19

Initial release.

### Added

- **Segmentation** — detects hard-angle boundaries between adjacent faces and groups them into individual card sections. Boundary sensitivity is controlled by the **Angle Threshold** parameter.
- **Centerline extraction** — finds the dominant length-wise axis through each card section and places a clean centerline through it, regardless of card orientation.
- **Vertex snapping** — sampled bone positions are snapped to the nearest mesh vertex within the same card section. Duplicate positions are removed to prevent zero-length bones.
- **Top-to-bottom orientation** — each bone chain runs from the highest Z endpoint (root/scalp end) to the lowest (tip), so bone tails consistently face downward.
- **`Bone_ROOT`** — a single root bone placed at the mesh bounding-box center; all chains are parented to it.
- **Chain density controls** — **Max Chains** caps the total number of chains (largest segments kept first); **Min Separation** culls chains whose midpoints are closer together than the specified distance, eliminating stacked duplicates on layered card meshes.
- **Bones Per Chain** — sets the number of bones in each chain as a direct count (replaces a distance-based spacing approach).
- **Clear operator** — removes previously generated `Hair_Armature` objects to support re-running with adjusted settings.
- **N-panel UI** — "Hair Rig" tab in the 3D Viewport sidebar, with parameters grouped under Segmentation, Chain Density, and Bones sections.
- **Hot-reload support** — the standard `_needs_reload` guard in `__init__.py` enables Blender's Reload Scripts workflow during development.
