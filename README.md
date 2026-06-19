# Hair Armature Generator

A Blender add-on that analyses a hair card mesh, detects structural boundaries between cards, and generates a guide armature — one bone chain per card section. The result is a clean, hierarchical armature intended as a starting point for manual rigging or weight-paint transfer; it does not create deformers or drive geometry directly.

## Requirements

- Blender 5.1.0 or later
- A mesh composed of planar card geometry (quads) representing hair volume

## Installation

1. In Blender, open **Edit → Preferences → Add-ons**.
2. Click **Install from Disk** and select the `hair_armature_gen/` folder (or a `.zip` of it).
3. Enable **Hair Armature Generator** in the add-on list.
4. The **Hair Rig** tab appears in the 3D Viewport N-panel.

## Usage

### 1. Prepare your mesh

The add-on detects boundaries by comparing the angle between adjacent face normals. Cards that are clearly planar and separated from their neighbours by hard-angle edges work best. No manual edge marking is required.

### 2. Configure parameters

Open the **Hair Rig** N-panel tab and set your target object, then adjust the parameters below.

#### Segmentation

| Parameter | Default | Description |
| :--- | :---: | :--- |
| **Angle Threshold** | 30° | Minimum dihedral angle between two adjacent faces for the shared edge to be treated as a card boundary. Raise to merge sections; lower to split them further. |

#### Chain Density

| Parameter | Default | Description |
| :--- | :---: | :--- |
| **Max Chains** | 0 | Hard cap on the total number of bone chains generated. Chains from the largest mesh segments are kept first. `0` means no limit. |
| **Min Separation** | 0 m | Minimum world-space distance between chain midpoints. Any candidate chain whose midpoint falls within this distance of an already-accepted chain is discarded. Use this to eliminate stacked or duplicate chains on layered card meshes. |

#### Bones

| Parameter | Default | Description |
| :--- | :---: | :--- |
| **Bones Per Chain** | 4 | Number of bones in each chain. Bone positions are sampled evenly along the card's PCA centerline and then snapped to the nearest mesh vertex. |

### 3. Generate

Click **Generate Structural Rig**. A `Hair_Armature` object is created in the active collection, containing:

- **`Bone_ROOT`** — a single root bone placed at the mesh's bounding-box centre.
- **`Hair_NNN_NNN`** — one chain of bones per detected card section, each chain parented to `Bone_ROOT`. Chains run top-to-bottom (head at scalp end, tail at tip end).

### 4. Clear

Click **Clear Structural Rig** to remove any previously generated `Hair_Armature` objects from the scene. This supports re-running the generator with adjusted settings.

## How it works

**Phase A — Segmentation**
The mesh is loaded into a BMesh and face normals are updated. Every edge shared by exactly two faces is tested: if the angle between those face normals exceeds the Angle Threshold, the edge is marked as a boundary. A flood-fill then groups faces into connected components (segments) that share no boundary edges.

**Phase B — Centerline extraction**
For each segment, vertex positions are collected and a principal component analysis (PCA via NumPy SVD) finds the dominant axis of elongation. The two extreme projections onto this axis become the endpoints of the centerline. The endpoint with the higher world-space Z coordinate is designated the root end, so chains always run scalp-to-tip.

**Phase C — Bone placement**
Sample points are distributed evenly along the centerline (count = Bones Per Chain + 1), then each point is snapped to the nearest vertex within the same segment using a KD-tree. Consecutive duplicate positions are removed to prevent zero-length bones. The resulting point sequence is used to create a connected bone chain in the armature's Edit Mode, with the first bone parented to `Bone_ROOT`.

## Out of scope (planned for v2.0+)

- Vertex weight map / deformer generation
- Raw spline/curve object input
- Automatic IK setup
