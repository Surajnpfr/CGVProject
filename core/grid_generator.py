"""
Grid Generator Module
=====================
Generates 2D mesh grids for 3D surface computation.
Supports adaptive resolution based on device type.
"""

import numpy as np
from typing import Tuple

# Device-based grid resolution presets (from UI requirements)
GRID_PRESETS = {
    "desktop": 100,
    "tablet": 75,
    "mobile": 50,
}


def generate_grid(
    x_range: Tuple[float, float] = (-5, 5),
    y_range: Tuple[float, float] = (-5, 5),
    resolution: int = 100,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate a 2D mesh grid for surface computation.

    Parameters
    ----------
    x_range : tuple of float
        (min, max) range for the X axis.
    y_range : tuple of float
        (min, max) range for the Y axis.
    resolution : int
        Number of points per axis (resolution x resolution grid).

    Returns
    -------
    X, Y : np.ndarray
        2D mesh grid arrays.
    """
    x = np.linspace(x_range[0], x_range[1], resolution)
    y = np.linspace(y_range[0], y_range[1], resolution)
    X, Y = np.meshgrid(x, y)
    return X, Y


def get_resolution_for_device(device: str = "desktop") -> int:
    """
    Return the optimal grid resolution for a given device type.

    Parameters
    ----------
    device : str
        One of 'desktop', 'tablet', 'mobile'.

    Returns
    -------
    int
        Grid resolution.
    """
    return GRID_PRESETS.get(device.lower(), GRID_PRESETS["desktop"])
