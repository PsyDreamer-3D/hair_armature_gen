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

#### Output

| Parameter | Default | Description |
| :--- | :---: | :--- |
| **Merge into Active Armature** | Off | When enabled, new bone chains are added to the currently active armature object instead of creating a new one. An existing `Bone_ROOT` is reused if present; otherwise a new one is created. A warning appears in the panel if no armature is active. |

### 3. Generate

Two generation methods are available:

#### Generate Structural Rig (automatic)

Click **Generate Structural Rig**. The add-on automatically detects card boundaries and generates one chain per segment. A `Hair_Armature` object is created in the active collection (or chains are merged into the active armature if **Merge into Active Armature** is enabled), containing:

- **`Bone_ROOT`** — a single root bone placed at the mesh's bounding-box centre.
- **`Hair_NNN_NNN`** — one chain of bones per detected card section, each chain parented to `Bone_ROOT`. Chains run top-to-bottom (head at scalp end, tail at tip end).

#### Generate Chain from Selection (manual)

For precise control over which vertices define a chain:

1. Select your target mesh and set it as the **Target Object** in the panel.
2. Tab into **Edit Mode** and select the vertices that should form the chain spine — typically a row of vertices running root-to-tip along a single card.
3. Tab back to **Object Mode**.
4. Click **Generate Chain from Selection**.

Each disconnected group of selected vertices becomes its own bone chain. Vertices are ordered by traversing the edges connecting them; a PCA fallback handles closed loops or branching topology. The resulting path is resampled to **Bones Per Chain** bones. Chains run top-to-bottom by the same Z-axis convention as the automatic operator.

### 4. Clear

Click **Clear Structural Rig** to remove any previously generated `Hair_Armature` objects from the scene. This supports re-running the generator with adjusted settings.

## How it works

**Phase A — Segmentation**
The mesh is loaded into a BMesh and face normals are updated. Every edge shared by exactly two faces is tested: if the angle between those face normals exceeds the Angle Threshold, the edge is marked as a boundary. A flood-fill then groups faces into connected components (segments) that share no boundary edges.

**Phase B — Centerline extraction**
For each segment, vertex positions are collected and a principal component analysis (PCA via NumPy SVD) finds the dominant axis of elongation. The two extreme projections onto this axis become the endpoints of the centerline. The endpoint with the higher world-space Z coordinate is designated the root end, so chains always run scalp-to-tip.

**Phase C — Bone placement**
Sample points are distributed evenly along the centerline (count = Bones Per Chain + 1), then each point is snapped to the nearest vertex within the same segment using a KD-tree. Consecutive duplicate positions are removed to prevent zero-length bones. The resulting point sequence is used to create a connected bone chain in the armature's Edit Mode, with the first bone parented to `Bone_ROOT`.

### Generate Chain from Selection

**Phase A — Island detection**
Selected vertex flags (`mesh.vertices[i].select`) are read in Object Mode. Vertices are grouped into connected islands by walking edges whose both endpoints are selected.

**Phase B — Path ordering**
For each island, endpoint vertices (those with only one selected neighbour) are identified. The endpoint closest to the mesh bounding-box centre is chosen as the root; edges are then traversed greedily to produce an ordered vertex sequence. If the island forms a closed loop or has branching topology (fewer than two endpoints), ordering falls back to PCA projection onto the principal axis.

**Phase C — Resampling and bone placement**
The ordered vertex path is resampled to **Bones Per Chain + 1** evenly-spaced positions using arc-length parameterisation, preserving curve shape. These positions are used directly as bone heads and tails; no additional vertex snapping is applied since the points originate from the mesh itself. The chain runs top-to-bottom (highest Z = root) and is parented to `Bone_ROOT`.

## Out of scope (planned for v2.0+)

- Vertex weight map / deformer generation
- Raw spline/curve object input
- Automatic IK setup
