# 📜 Hair Mesh Structural Armature Generator Add-on
## Scope of Work & Technical Development Roadmap

### 🚀 Executive Summary

This document defines the scope, technical requirements, and implementation plan for an advanced Blender add-on. The tool's purpose is to automate the detection of structural boundaries within a unified card mesh (representing hair) and automatically generate a parented armature structure that acts as a geometric guide for subsequent manual rigging work. This tool does not create deformers; it creates **markers**.

---

### 🎯 Project Goal & Objectives

**Primary Goal:** To provide an automated, non-destructive method of segmenting complex card mesh hair into distinct structural zones and placing a dedicated bone chain within each zone.

**Success Criteria:** The resulting armature must be clean, logically structured, and easily transferable/usable by the artist for manual rigging refinement (e.g., transferring to Rigify or custom weight painting).

### ⚙️ I. Technical Assumptions & Constraints

The success of this add-on relies on adhering strictly to these established parameters:

1.  **Input Geometry:** The primary input must be a unified mesh composed of **card geometry** (planar, polygon surfaces) representing the hair volume.
2.  **Segmentation Trigger:** Structural boundaries are defined solely by **hard edges**. An edge is considered a boundary if its surrounding vertices demonstrate significant and quantifiable changes in surface normal or curvature (discontinuity).
3.  **Output Structure:** The output armature must be composed of:
    *   A single, global root bone (`Bone_ROOT`).
    *   Multiple child chains of parented bones (one chain per detected structural section).

### 📏 II. Core Algorithmic Workflow (The Blueprint)

The add-on will execute a three-phase process upon execution:

#### Phase A: Initialization & Root Bone Placement
1.  **Input Validation:** Validate the selected mesh object and ensure it meets minimum geometric requirements.
2.  **Root Positioning:** Calculate the overall geometric centroid of the input mesh's bounding volume. The `Bone_ROOT` bone is placed at this center point, acting as the master parent for all subsequent chains.

#### Phase B: Structural Segmentation (Boundary Detection)
1.  **Edge Analysis:** Traverse and analyze every edge on the input mesh.
2.  **Hard Boundary Identification:** Use geometric calculations to identify edges where the local surface normal changes abruptly (the "hard crease" definition).
3.  **Component Isolation:** Based on these identified boundaries, perform a connected component analysis, mathematically separating the unified mesh into distinct, structurally isolated sections.

#### Phase C: Bone Chain Generation & Assembly
1.  **Centerline Pathing:** For each segmented section, calculate its optimal centerline curve path.
2.  **Sampling & Placement:** Sample points along this centerline at fixed, user-defined intervals (e.g., 5 cm).
3.  **Bone Creation:** Generate a bone for every sampled point, creating a linear chain of parented bones.
4.  **Assembly:** Parent the first bone of each new chain to the global `Bone_ROOT`.

---

### ✨ III. Functional Requirements (User Interface & Features)

The add-on must include the following mandatory features:

| Feature | Description | Priority |
| :--- | :--- | :--- |
| **UI Panel** | Clean, intuitive Blender panel structure for operation. | High |
| **Input Selection** | Mandatory selection field targeting the single mesh object to be analyzed. | Critical |
| **Parameter Control 1: Segmentation Threshold** | A user-adjustable slider/input defining the sensitivity of hard edge detection (controls boundary tightness). | Critical |
| **Parameter Control 2: Bone Interval Spacing** | A float input defining the fixed distance between generated bones along the centerline. | High |
| **Execution Logic** | A single `Generate Structural Rig` button that runs the entire Phase I $\rightarrow$ III workflow in sequence. | Critical |
| **Output Management** | The ability to clean up and group all generated bones into a single, easily selectable armature object. | High |

### 🚫 IV. Out of Scope (V2.0+ Features)

The following features are explicitly *excluded* from the Minimum Viable Product (MVP) scope but should be noted for future development phases:

*   ❌ **Deformation:** The tool will not generate vertex weight maps or deformers.
*   ❌ **Curved Input Support:** Cannot process raw spline/curve objects as input geometry.
*   ❌ **Advanced Rigging Logic:** Will not automatically structure bones for complex kinematics (e.g., IK setup).

---

### 🗓️ V. Development Roadmap & Milestones

The project will be executed in three sequential phases, ensuring stability and testable milestones at each stage.

#### 🥇 Phase I: Setup & Foundation
*   **Goal:** Establish the input pipeline and define the root structure.
*   **Deliverables:** Operational UI framework; successful mesh validation; calculation and placement of `Bone_ROOT` at the object's centroid.

#### 🥈 Phase II: Structural Core Development
*   **Goal:** Implement the most complex logic—detecting boundaries and isolating sections.
*   **Deliverables:** Robust edge normal analysis function (Hard Boundary Detection); functional connected component isolation routine; centerline curve extraction per section.

#### 🥉 Phase III: Assembly & Final Polish
*   **Goal:** Convert abstract paths into usable bone geometry and finalize the user experience.
*   **Deliverables:** Bone chain creation and parenting logic implemented; final single armature assembly; comprehensive documentation, including a tutorial on interpreting the generated guide bones.
