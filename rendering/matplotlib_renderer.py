"""
Matplotlib Renderer Module
==========================
Renders static 3D surface plots using Matplotlib's mplot3d.
Supports color mapping, wireframe, and surface styles.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.figure import Figure
from typing import Optional


# Available Matplotlib colormaps for surface rendering
COLORMAPS = [
    "viridis",
    "plasma",
    "inferno",
    "magma",
    "cividis",
    "coolwarm",
    "Spectral",
    "RdYlBu",
    "twilight",
    "turbo",
]


def render_surface(
    X: np.ndarray,
    Y: np.ndarray,
    Z: np.ndarray,
    colormap: str = "viridis",
    title: str = "3D Surface",
    alpha: float = 0.9,
    elev: float = 30,
    azim: float = 45,
    show: bool = True,
) -> Figure:
    """
    Render a static 3D surface plot using Matplotlib.

    Parameters
    ----------
    X, Y, Z : np.ndarray
        Mesh grid and computed height values.
    colormap : str
        Matplotlib colormap name.
    title : str
        Plot title.
    alpha : float
        Surface transparency (0–1).
    elev : float
        Elevation angle in degrees.
    azim : float
        Azimuth angle in degrees.
    show : bool
        Whether to display the plot immediately.

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    surf = ax.plot_surface(
        X, Y, Z,
        cmap=colormap,
        alpha=alpha,
        edgecolor="none",
        rstride=1,
        cstride=1,
    )

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title(title)
    ax.view_init(elev=elev, azim=azim)

    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label="Z value")

    plt.tight_layout()
    if show:
        plt.show()

    return fig


def render_wireframe(
    X: np.ndarray,
    Y: np.ndarray,
    Z: np.ndarray,
    title: str = "3D Wireframe",
    color: str = "cyan",
    elev: float = 30,
    azim: float = 45,
    show: bool = True,
) -> Figure:
    """
    Render a 3D wireframe plot.

    Parameters
    ----------
    X, Y, Z : np.ndarray
        Mesh grid and computed height values.
    title : str
        Plot title.
    color : str
        Wire color.
    elev, azim : float
        Viewing angles.
    show : bool
        Whether to display immediately.

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    ax.plot_wireframe(X, Y, Z, color=color, linewidth=0.5)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title(title)
    ax.view_init(elev=elev, azim=azim)

    plt.tight_layout()
    if show:
        plt.show()

    return fig
