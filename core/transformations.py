"""
Transformations Module
======================
Implements 3D transformations: Scaling, Rotation (Z-axis), and Translation.
These operate on the computed Z surface to demonstrate CG transformation concepts.
"""

import numpy as np
from typing import Tuple


def scale_surface(
    Z: np.ndarray,
    factor: float = 1.0,
) -> np.ndarray:
    """
    Scale the Z values uniformly.

    Parameters
    ----------
    Z : np.ndarray
        Surface height values.
    factor : float
        Multiplicative scale factor.

    Returns
    -------
    np.ndarray
        Scaled Z values.
    """
    return Z * factor


def translate_surface(
    Z: np.ndarray,
    offset: float = 0.0,
) -> np.ndarray:
    """
    Translate (shift) the surface along the Z axis.

    Parameters
    ----------
    Z : np.ndarray
        Surface height values.
    offset : float
        Additive offset along Z.

    Returns
    -------
    np.ndarray
        Translated Z values.
    """
    return Z + offset


def rotate_surface_z(
    X: np.ndarray,
    Y: np.ndarray,
    angle_deg: float = 0.0,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Rotate the X-Y grid around the Z axis by the given angle.

    Parameters
    ----------
    X, Y : np.ndarray
        Mesh grid arrays.
    angle_deg : float
        Rotation angle in degrees.

    Returns
    -------
    X_rot, Y_rot : np.ndarray
        Rotated mesh grid arrays.
    """
    theta = np.radians(angle_deg)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    X_rot = X * cos_t - Y * sin_t
    Y_rot = X * sin_t + Y * cos_t
    return X_rot, Y_rot
