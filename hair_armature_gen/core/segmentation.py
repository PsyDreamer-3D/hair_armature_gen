import math
import bmesh


def segment_mesh(mesh_obj, angle_threshold_rad):
    """Return a list of vertex-position groups (one group per connected component).

    Two faces are in the same component if the edge between them has a
    dihedral angle less than *angle_threshold_rad*.  Border edges (only one
    linked face) are never boundary edges.

    Vertex positions are extracted and copied before the BMesh is freed, so
    callers receive plain mathutils.Vector lists with no BMesh dependency.

    Returns list[list[mathutils.Vector]], sorted largest group first.
    """
    bm = bmesh.new()
    bm.from_mesh(mesh_obj.data)
    bm.normal_update()

    boundary_edges = set()
    for edge in bm.edges:
        if len(edge.link_faces) != 2:
            continue
        n0 = edge.link_faces[0].normal
        n1 = edge.link_faces[1].normal
        dot = max(-1.0, min(1.0, n0.dot(n1)))
        if math.acos(dot) > angle_threshold_rad:
            boundary_edges.add(edge.index)

    visited = set()
    raw_segments = []

    for start_face in bm.faces:
        if start_face.index in visited:
            continue

        face_group = []
        queue = [start_face]
        visited.add(start_face.index)

        while queue:
            face = queue.pop()
            face_group.append(face)
            for edge in face.edges:
                if edge.index in boundary_edges:
                    continue
                if len(edge.link_faces) != 2:
                    continue
                for neighbour in edge.link_faces:
                    if neighbour.index not in visited:
                        visited.add(neighbour.index)
                        queue.append(neighbour)

        raw_segments.append(face_group)

    raw_segments.sort(key=lambda g: len(g), reverse=True)

    # Extract vertex positions while the BMesh is still alive.
    segments = []
    for face_group in raw_segments:
        seen = {}
        for face in face_group:
            for vert in face.verts:
                if vert.index not in seen:
                    seen[vert.index] = vert.co.copy()
        segments.append(list(seen.values()))

    bm.free()
    return segments
