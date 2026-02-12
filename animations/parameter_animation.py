"""
Parameter Animation Module
===========================
Generates parameter value sequences for smooth surface morphing animations.
"""

import numpy as np
from typing import Tuple


def generate_parameter_sweep(
    start: float = 0.1,
    end: float = 3.0,
    steps: int = 30,
    bounce: bool = True,
) -> np.ndarray:
    """
    Generate a smooth parameter sweep array.

    Parameters
    ----------
    start : float
        Starting parameter value.
    end : float
        Ending parameter value.
    steps : int
        Number of interpolation steps.
    bounce : bool
        If True, the sweep goes start→end→start for a looping animation.

    Returns
    -------
    np.ndarray
        Array of parameter values.
    """
    forward = np.linspace(start, end, steps)
    if bounce:
        backward = np.linspace(end, start, steps)
        return np.concatenate([forward, backward])
    return forward


def generate_rotation_sweep(
    start_deg: float = 0.0,
    end_deg: float = 360.0,
    steps: int = 60,
) -> np.ndarray:
    """
    Generate a rotation angle sweep.

    Parameters
    ----------
    start_deg : float
        Starting angle in degrees.
    end_deg : float
        Ending angle in degrees.
    steps : int
        Number of steps.

    Returns
    -------
    np.ndarray
        Array of angle values in degrees.
    """
    return np.linspace(start_deg, end_deg, steps)


def smooth_interpolation(
    start: float,
    end: float,
    steps: int = 30,
) -> np.ndarray:
    """
    Smooth (ease-in-out) interpolation using a cosine curve.

    Parameters
    ----------
    start, end : float
        Value range.
    steps : int
        Number of steps.

    Returns
    -------
    np.ndarray
        Smoothly interpolated values.
    """
    t = np.linspace(0, np.pi, steps)
    # Cosine ease: goes from 0 → 1 smoothly
    blend = (1 - np.cos(t)) / 2
    return start + (end - start) * blend
