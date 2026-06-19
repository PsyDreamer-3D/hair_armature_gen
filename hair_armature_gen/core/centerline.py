import numpy as np
from mathutils import Vector


def compute_centerline(faces):
    """Return (p0, p1) as mathutils.Vectors defining the PCA major-axis endpoints.

    Collects all unique vertex positions from *faces* (a list of BMFace),
    runs SVD to find the principal axis, then projects vertices onto that
    axis to find the two extreme endpoints.
    """
    seen = {}
    for face in faces:
        for vert in face.verts:
            if vert.index not in seen:
                seen[vert.index] = vert.co.copy()

    positions = np.array([list(v) for v in seen.values()], dtype=np.float64)

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
