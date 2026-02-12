"""
Paraboloid Example
==================
Demonstrates rendering of z = a(x² + y²).
Run standalone: python -m examples.paraboloid
"""

import sys
import os

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.grid_generator import generate_grid
from core.function_engine import paraboloid
from rendering.matplotlib_renderer import render_surface
from rendering.plotly_renderer import create_surface_figure


def main():
    X, Y = generate_grid(resolution=100)
    Z = paraboloid(X, Y, a=1.0)

    # Static Matplotlib render
    render_surface(X, Y, Z, colormap="viridis", title="Paraboloid: z = x² + y²")

    # Interactive Plotly render
    fig = create_surface_figure(X, Y, Z, colormap="Viridis", title="Paraboloid: z = x² + y²")
    fig.show()


if __name__ == "__main__":
    main()
