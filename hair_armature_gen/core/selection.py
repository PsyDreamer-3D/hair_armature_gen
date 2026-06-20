import numpy as np
from mathutils import Vector


def get_selected_islands(mesh_obj):
    """Return connected components of selected vertices as lists of vertex indices.

    Connectivity is determined by edges whose both endpoints are selected.
    Returns list[list[int]], one inner list per island.  Empty if nothing selected.
    """
    mesh = mesh_obj.data
    selected = {v.index for v in mesh.vertices if v.select}
    if not selected:
        return []

    adj = {i: [] for i in selected}
    for edge in mesh.edges:
        v0, v1 = edge.vertices
        if v0 in selected and v1 in selected:
            adj[v0].append(v1)
            adj[v1].append(v0)

    visited = set()
    islands = []
    for start in selected:
        if start in visited:
            continue
        island = []
        queue = [start]
        visited.add(start)
        while queue:
            v = queue.pop()
            island.append(v)
            for nb in adj[v]:
                if nb not in visited:
                    visited.add(nb)
                    queue.append(nb)
        islands.append(island)

    return islands


def _pca_order(indices, mesh_obj):
    """Order *indices* by projection onto their principal axis (fallback for loops/branches)."""
    verts = mesh_obj.data.vertices
    positions = np.array([list(verts[i].co) for i in indices], dtype=np.float64)
    centroid = positions.mean(axis=0)
    centered = positions - centroid
    _, _, Vt = np.linalg.svd(centered, full_matrices=False)
    axis = Vt[0]
    projections = centered @ axis
    order = np.argsort(projections)
    return [Vector(verts[indices[i]].co) for i in order]


def order_island_by_path(indices, mesh_obj):
    """Return vertex positions ordered root-to-tip by traversing connected edges.

    *indices* is a list of vertex indices belonging to one connected island.
    Endpoint vertices (degree <= 1 in the selected subgraph) anchor the path;
    the one closest to the mesh bounding-box centroid is chosen as the start.
    Falls back to PCA ordering for closed loops or branching topology.

    Returns list[Vector] in local space.
    """
    mesh = mesh_obj.data
    adj = {i: [] for i in indices}
    index_set = set(indices)
    for edge in mesh.edges:
        v0, v1 = edge.vertices
        if v0 in index_set and v1 in index_set:
            adj[v0].append(v1)
            adj[v1].append(v0)

    endpoints = [i for i, nbs in adj.items() if len(nbs) <= 1]
    if len(endpoints) < 2:
        return _pca_order(indices, mesh_obj)

    # Root = endpoint closest to bounding-box centroid (local space)
    bb = mesh_obj.bound_box
    world_mat = mesh_obj.matrix_world
    bb_world = [world_mat @ Vector(corner) for corner in bb]
    centroid_world = sum(bb_world, Vector()) / 8.0
    centroid_local = world_mat.inverted() @ centroid_world

    start = min(endpoints, key=lambda i: (Vector(mesh.vertices[i].co) - centroid_local).length)

    path = [start]
    visited = {start}
    current = start
    while True:
        nexts = [v for v in adj[current] if v not in visited]
        if not nexts:
            break
        current = nexts[0]
        path.append(current)
        visited.add(current)

    return [Vector(mesh.vertices[i].co) for i in path]


def resample_polyline(points, bone_count):
    """Resample a polyline to bone_count + 1 evenly-spaced points along its arc length.

    *points* is an ordered list of mathutils.Vector positions.
    Returns list[Vector] with exactly bone_count + 1 entries (minimum 2).
    """
    if len(points) < 2:
        return list(points) if points else []

    # Build cumulative arc-length table
    arc = [0.0]
    for a, b in zip(points, points[1:]):
        arc.append(arc[-1] + (b - a).length)

    total = arc[-1]
    if total < 1e-6:
        return [points[0].copy(), points[-1].copy()]

    n = max(1, bone_count)
    result = []
    for k in range(n + 1):
        t = total * k / n
        # Binary search for the segment containing t
        lo, hi = 0, len(arc) - 2
        while lo < hi:
            mid = (lo + hi) // 2
            if arc[mid + 1] < t:
                lo = mid + 1
            else:
                hi = mid
        seg_len = arc[lo + 1] - arc[lo]
        if seg_len < 1e-9:
            result.append(points[lo].copy())
        else:
            frac = (t - arc[lo]) / seg_len
            result.append(points[lo].lerp(points[lo + 1], frac))

    return result
