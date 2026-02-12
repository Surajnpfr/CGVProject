"""
Plotly Renderer Module
======================
Renders interactive 3D surface plots using Plotly.
Neutral theme — no neon, no glow — matches the clean glassmorphism UI.
"""

import numpy as np
import plotly.graph_objects as go
from typing import Optional

# Available Plotly colormaps
COLORMAPS = [
    "Viridis",
    "Plasma",
    "Inferno",
    "Magma",
    "Cividis",
    "Turbo",
    "Tealgrn",
    "RdBu",
    "Spectral",
    "YlGnBu",
    "Hot",
    "Portland",
    "Earth",
    "Temps",
]


def create_surface_figure(
    X: np.ndarray,
    Y: np.ndarray,
    Z: np.ndarray,
    colormap: str = "Viridis",
    title: str = "3D Surface",
    dark_mode: bool = False,
    opacity: float = 0.96,
    show_contour: bool = False,
) -> go.Figure:
    """
    Create an interactive 3D surface plot with a neutral academic theme.
    """
    contours_z = None
    if show_contour:
        contours_z = dict(
            show=True,
            usecolormap=True,
            highlightcolor="#0EA5A4",
            project_z=True,
        )

    surface = go.Surface(
        x=X,
        y=Y,
        z=Z,
        colorscale=colormap,
        opacity=opacity,
        contours_z=contours_z,
        colorbar=dict(
            title="Z",
            thickness=14,
            len=0.55,
            tickfont=dict(size=11, family="Inter, Segoe UI, sans-serif"),
        ),
    )

    # ── Neutral theme tokens (readable contrast) ──
    if dark_mode:
        bg_color = "rgb(26, 26, 46)"
        grid_color = "rgba(180, 180, 210, 0.18)"
        font_color = "#e8e8f0"
        paper_color = "rgb(24, 24, 42)"
    else:
        bg_color = "rgb(244, 245, 249)"
        grid_color = "rgba(100, 116, 139, 0.18)"
        font_color = "#1e293b"                 # slate-800
        paper_color = "rgb(246, 247, 251)"

    font_family = "Inter, Segoe UI, system-ui, sans-serif"

    layout = go.Layout(
        title=dict(
            text=title,
            font=dict(size=16, color=font_color, family=font_family),
            x=0.5,
        ),
        scene=dict(
            xaxis=dict(
                title=dict(text="X", font=dict(color=font_color, family=font_family)),
                backgroundcolor=bg_color,
                gridcolor=grid_color,
                showbackground=True,
                tickfont=dict(color=font_color, size=10, family=font_family),
            ),
            yaxis=dict(
                title=dict(text="Y", font=dict(color=font_color, family=font_family)),
                backgroundcolor=bg_color,
                gridcolor=grid_color,
                showbackground=True,
                tickfont=dict(color=font_color, size=10, family=font_family),
            ),
            zaxis=dict(
                title=dict(text="Z", font=dict(color=font_color, family=font_family)),
                backgroundcolor=bg_color,
                gridcolor=grid_color,
                showbackground=True,
                tickfont=dict(color=font_color, size=10, family=font_family),
            ),
        ),
        paper_bgcolor=paper_color,
        margin=dict(l=0, r=0, t=40, b=0),
        font=dict(color=font_color, family=font_family),
    )

    fig = go.Figure(data=[surface], layout=layout)

    fig.update_layout(
        scene_camera=dict(
            eye=dict(x=1.5, y=1.5, z=1.2),
        ),
    )

    return fig


def create_animation_frames(
    X: np.ndarray,
    Y: np.ndarray,
    func,
    a_values: np.ndarray,
    colormap: str = "Viridis",
    dark_mode: bool = False,
) -> go.Figure:
    """
    Create an animated 3D surface with parameter sweep.
    """
    Z_init = func(X, Y, a_values[0])
    fig = create_surface_figure(X, Y, Z_init, colormap=colormap, dark_mode=dark_mode)

    frames = []
    for a in a_values:
        Z = func(X, Y, a)
        frames.append(
            go.Frame(
                data=[go.Surface(x=X, y=Y, z=Z, colorscale=colormap)],
                name=f"a={a:.2f}",
            )
        )

    fig.frames = frames

    # Neutral-styled play / pause
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                y=0,
                x=0.5,
                xanchor="center",
                font=dict(family="Inter, Segoe UI, sans-serif", size=12),
                buttons=[
                    dict(
                        label="Play",
                        method="animate",
                        args=[
                            None,
                            dict(
                                frame=dict(duration=80, redraw=True),
                                fromcurrent=True,
                                mode="immediate",
                            ),
                        ],
                    ),
                    dict(
                        label="Pause",
                        method="animate",
                        args=[
                            [None],
                            dict(
                                frame=dict(duration=0, redraw=False),
                                mode="immediate",
                            ),
                        ],
                    ),
                ],
            )
        ],
        sliders=[
            dict(
                active=0,
                steps=[
                    dict(
                        args=[
                            [f"a={a:.2f}"],
                            dict(
                                frame=dict(duration=80, redraw=True),
                                mode="immediate",
                            ),
                        ],
                        label=f"{a:.2f}",
                        method="animate",
                    )
                    for a in a_values
                ],
                x=0.05,
                len=0.9,
                y=-0.05,
                currentvalue=dict(
                    prefix="Parameter a = ",
                    visible=True,
                    xanchor="center",
                    font=dict(family="Inter, Segoe UI, sans-serif", size=13),
                ),
                transition=dict(duration=50),
            )
        ],
    )

    return fig
