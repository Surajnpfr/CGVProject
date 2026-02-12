"""
Function Engine Module
======================
Registry of mathematical functions for 3D surface visualization.
Each function accepts X, Y grids and optional parameters,
and returns the computed Z values.
"""

import numpy as np
from typing import Callable, Dict, Any, List


# ---------------------------------------------------------------------------
# Function definitions
# ---------------------------------------------------------------------------

def paraboloid(X: np.ndarray, Y: np.ndarray, a: float = 1.0) -> np.ndarray:
    """z = a * (x² + y²)"""
    return a * (X ** 2 + Y ** 2)


def sincos(X: np.ndarray, Y: np.ndarray, a: float = 1.0) -> np.ndarray:
    """z = a * sin(x) * cos(y)"""
    return a * np.sin(X) * np.cos(Y)


def gaussian(X: np.ndarray, Y: np.ndarray, a: float = 1.0) -> np.ndarray:
    """z = a * exp(-(x² + y²))"""
    return a * np.exp(-(X ** 2 + Y ** 2))


def saddle(X: np.ndarray, Y: np.ndarray, a: float = 1.0) -> np.ndarray:
    """z = a * (x² - y²)"""
    return a * (X ** 2 - Y ** 2)


def ripple(X: np.ndarray, Y: np.ndarray, a: float = 1.0) -> np.ndarray:
    """z = a * sin(sqrt(x² + y²))"""
    R = np.sqrt(X ** 2 + Y ** 2)
    # Avoid division by zero for sinc-like behavior
    return a * np.sin(R)


def wave(X: np.ndarray, Y: np.ndarray, a: float = 1.0) -> np.ndarray:
    """z = a * sin(x) * sin(y)"""
    return a * np.sin(X) * np.sin(Y)


def egg_carton(X: np.ndarray, Y: np.ndarray, a: float = 1.0) -> np.ndarray:
    """z = a * (cos(x) + cos(y))"""
    return a * (np.cos(X) + np.cos(Y))


def monkey_saddle(X: np.ndarray, Y: np.ndarray, a: float = 1.0) -> np.ndarray:
    """z = a * (x³ - 3xy²)"""
    return a * (X ** 3 - 3 * X * Y ** 2)


# ---------------------------------------------------------------------------
# Function Registry
# ---------------------------------------------------------------------------

FUNCTION_REGISTRY: Dict[str, Dict[str, Any]] = {
    "Paraboloid  z = a(x² + y²)": {
        "func": paraboloid,
        "description": "A bowl-shaped surface opening upward.",
        "default_a": 1.0,
    },
    "Sin·Cos  z = a·sin(x)·cos(y)": {
        "func": sincos,
        "description": "Oscillating wave surface combining sine and cosine.",
        "default_a": 1.0,
    },
    "Gaussian  z = a·e^(-(x²+y²))": {
        "func": gaussian,
        "description": "A bell-curve surface (Gaussian bump).",
        "default_a": 1.0,
    },
    "Saddle  z = a(x² − y²)": {
        "func": saddle,
        "description": "A hyperbolic paraboloid (saddle shape).",
        "default_a": 1.0,
    },
    "Ripple  z = a·sin(√(x²+y²))": {
        "func": ripple,
        "description": "Concentric ripple waves radiating from the origin.",
        "default_a": 1.0,
    },
    "Wave  z = a·sin(x)·sin(y)": {
        "func": wave,
        "description": "A double-sine wave pattern.",
        "default_a": 1.0,
    },
    "Egg Carton  z = a(cos(x)+cos(y))": {
        "func": egg_carton,
        "description": "An egg-carton shaped periodic surface.",
        "default_a": 1.0,
    },
    "Monkey Saddle  z = a(x³ − 3xy²)": {
        "func": monkey_saddle,
        "description": "A saddle surface with three downward slopes.",
        "default_a": 0.1,
    },
}


def get_function_names() -> List[str]:
    """Return list of available function display names."""
    return list(FUNCTION_REGISTRY.keys())


def compute_surface(
    name: str,
    X: np.ndarray,
    Y: np.ndarray,
    a: float = 1.0,
) -> np.ndarray:
    """
    Compute Z values for the named surface function.

    Parameters
    ----------
    name : str
        Display name of the function (must be in FUNCTION_REGISTRY).
    X, Y : np.ndarray
        Mesh grid arrays.
    a : float
        Scaling / transformation parameter.

    Returns
    -------
    Z : np.ndarray
    """
    entry = FUNCTION_REGISTRY[name]
    return entry["func"](X, Y, a)


def get_default_param(name: str) -> float:
    """Return the default 'a' parameter for a given function."""
    return FUNCTION_REGISTRY[name]["default_a"]


def get_description(name: str) -> str:
    """Return the description string for a given function."""
    return FUNCTION_REGISTRY[name]["description"]
