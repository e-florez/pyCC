#!/usr/bin/python3.8

def dihedral(p0, p1, p2, p3):
    """Praxeolitic formula
    1 sqrt, 1 cross product

    computing DIHEDRAL angle
            p2
            /
    p0----p1
            \
            p3

    - order matters!
    
    
    taken from:
    
    https://stackoverflow.com/questions/20305272/dihedral-torsion-angle-from-four-points-in-cartesian-coordinates-in-python
    
    also from:
    
    https://web.stanford.edu/class/archive/cs/cs279/cs279.1182/assignments/Ramachandran_Plot.py
    
    """
    import numpy as np

    b0 = -1.0*(p1 - p0)
    b1 = p2 - p1
    b2 = p3 - p2

    if np.linalg.norm(b1) < 0.1:
        return 0

    # normalize b1 so that it does not influence magnitude of vector
    # rejections that come next
    b1 = b1 / np.linalg.norm(b1)

    # vector rejections
    # v = projection of b0 onto plane perpendicular to b1
    #   = b0 minus component that aligns with b1
    # w = projection of b2 onto plane perpendicular to b1
    #   = b2 minus component that aligns with b1
    v = b0 - np.dot(b0, b1)*b1
    w = b2 - np.dot(b2, b1)*b1

    # angle between v and w in a plane is the torsion angle
    # v and w may not be normalized but that's fine since tan is y/x
    x = np.dot(v, w)
    y = np.dot(np.cross(b1, v), w)

    dihedral_angle = np.arctan2(y, x)
    dihedral_angle_degrees = abs(np.degrees(dihedral_angle))

    return dihedral_angle_degrees

# ------------------------------------------------------------------
