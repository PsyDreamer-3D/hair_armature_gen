import numpy as np
from mathutils import Vector, kdtree


def compute_centerline(vertex_positions):
    """Return (p0, p1) as mathutils.Vectors defining the PCA major-axis endpoints.

    *vertex_positions* is a list of mathutils.Vector (world-space or local-space
    positions of vertices belonging to one segment, as returned by segment_mesh).
    Runs SVD to find the principal axis and projects vertices onto it to find
    the two extreme endpoints.
    """
    positions = np.array([list(v) for v in vertex_positions], dtype=np.float64)

    centroid = positions.mean(axis=0)
    centered = positions - centroid

    _, _, Vt = np.linalg.svd(centered, full_matrices=False)
    axis = Vt[0]

    projections = centered @ axis
    t_min = projections.min()
    t_max = projections.max()

    p0 = Vector(centroid + t_min * axis)
    p1 = Vector(centroid + t_max * axis)
    return p0, p1


def sample_centerline(p0, p1, spacing):
    """Return a list of evenly-spaced points from p0 to p1.

    Always includes p0 and p1.  If the distance is shorter than *spacing*,
    returns [p0, p1] (one bone).
    """
    direction = p1 - p0
    length = direction.length
    if length < 1e-6:
        return [p0.copy(), p1.copy()]

    unit = direction / length
    n_intervals = max(1, round(length / spacing))
    step = length / n_intervals

    points = [p0 + unit * (i * step) for i in range(n_intervals)]
    points.append(p1.copy())
    return points


def snap_to_vertices(points, vertex_positions):
    """Snap each point to the nearest vertex in *vertex_positions*.

    Deduplicates consecutive positions that land on the same vertex to
    prevent zero-length bones.  Always returns at least 2 points; if all
    points collapse to one vertex the first and last snapped positions are
    kept so the caller can decide whether to skip the chain.
    """
    kd = kdtree.KDTree(len(vertex_positions))
    for i, v in enumerate(vertex_positions):
        kd.insert(v, i)
    kd.balance()

    snapped = [kd.find(pt)[0].copy() for pt in points]

    deduped = [snapped[0]]
    for co in snapped[1:]:
        if (co - deduped[-1]).length > 1e-6:
            deduped.append(co)

    if len(deduped) < 2:
        deduped = [snapped[0], snapped[-1]]

    return deduped
