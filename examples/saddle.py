"""
Saddle Surface Example
======================
Demonstrates rendering of z = a(x² − y²).
Run standalone: python -m examples.saddle
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.grid_generator import generate_grid
from core.function_engine import saddle
from rendering.matplotlib_renderer import render_surface
from rendering.plotly_renderer import create_surface_figure


def main():
    X, Y = generate_grid(resolution=100)
    Z = saddle(X, Y, a=1.0)

    render_surface(X, Y, Z, colormap="coolwarm", title="Saddle: z = x² − y²")

    fig = create_surface_figure(X, Y, Z, colormap="RdBu", title="Saddle: z = x² − y²")
    fig.show()


if __name__ == "__main__":
    main()
