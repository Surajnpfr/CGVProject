"""
Interactive 3D Visualization of Mathematical Functions
======================================================
Main Streamlit application — clean glassmorphism UI.
Run: streamlit run main.py
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go

from core.grid_generator import generate_grid, GRID_PRESETS
from core.function_engine import (
    FUNCTION_REGISTRY,
    get_function_names,
    compute_surface,
    get_default_param,
    get_description,
)
from core.transformations import scale_surface, translate_surface, rotate_surface_z
from rendering.plotly_renderer import create_surface_figure, create_animation_frames, COLORMAPS
from animations.parameter_animation import generate_parameter_sweep

# ──────────────────────────────────────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="3D Math Visualizer",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# Session State Defaults
# ──────────────────────────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False  # Light mode default — academic / calm

# ──────────────────────────────────────────────────────────────────────────────
# Clean Glassmorphism CSS
# ──────────────────────────────────────────────────────────────────────────────

def inject_css(dark: bool = False):
    """Inject neutral glassmorphism + responsive CSS — optimised for readability."""
    if dark:
        bg_gradient = "linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)"
        glass_bg = "rgba(255, 255, 255, 0.10)"
        glass_border = "rgba(255, 255, 255, 0.15)"
        text_color = "#f1f1f4"
        text_muted = "#b0b5c3"
        accent = "#2dd4bf"          # teal-400
        accent_hover = "#14b8a6"    # teal-500
        sidebar_bg = "rgba(22, 22, 40, 0.96)"
        input_bg = "rgba(255, 255, 255, 0.09)"
        input_border = "rgba(255, 255, 255, 0.14)"
        shadow = "0 10px 30px rgba(0, 0, 0, 0.30)"
        btn_bg = "#475569"
        btn_hover = "#64748b"
        divider = "rgba(255, 255, 255, 0.10)"
    else:
        bg_gradient = "linear-gradient(135deg, #F6F7FB 0%, #EEF1F5 100%)"
        glass_bg = "rgba(255, 255, 255, 0.60)"
        glass_border = "rgba(255, 255, 255, 0.70)"
        text_color = "#111827"
        text_muted = "#374151"
        accent = "#0EA5A4"          # teal
        accent_hover = "#0d9695"
        sidebar_bg = "rgba(255, 255, 255, 0.78)"
        input_bg = "rgba(255, 255, 255, 0.65)"
        input_border = "rgba(180, 185, 200, 0.50)"
        shadow = "0 10px 30px rgba(17, 24, 39, 0.08)"
        btn_bg = "#334155"
        btn_hover = "#1e293b"
        divider = "rgba(17, 24, 39, 0.10)"

    css = f"""
    <style>
    /* ─── Fonts ─── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ─── Global ─── */
    .stApp {{
        background: {bg_gradient};
        background-attachment: fixed;
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
        color: {text_color};
    }}

    /* Force all Streamlit text to inherit our color */
    .stApp p,
    .stApp span,
    .stApp label,
    .stApp div {{
        color: {text_color};
    }}

    /* ─── Hide Streamlit chrome ─── */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header[data-testid="stHeader"] {{
        background: transparent;
    }}

    /* ─── Sidebar ─── */
    section[data-testid="stSidebar"] {{
        background: {sidebar_bg} !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border-right: 1px solid {glass_border};
    }}
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stCheckbox label span,
    section[data-testid="stSidebar"] .stSlider label,
    section[data-testid="stSidebar"] .stSlider [data-testid="stTickBarMin"],
    section[data-testid="stSidebar"] .stSlider [data-testid="stTickBarMax"],
    section[data-testid="stSidebar"] .stNumberInput label {{
        color: {text_color} !important;
    }}
    section[data-testid="stSidebar"] hr {{
        border-color: {divider} !important;
        margin: 0.8rem 0 !important;
    }}

    /* ─── Glass Card (primary panel) ─── */
    .glass-card {{
        background: {glass_bg};
        border: 1px solid {glass_border};
        border-radius: 20px;
        box-shadow: {shadow};
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 1.5rem 2rem;
        margin-bottom: 1rem;
    }}
    .glass-card--tight {{ border-radius: 16px; }}

    /* ─── Header Card ─── */
    .header-card {{
        background: {glass_bg};
        border: 1px solid {glass_border};
        border-radius: 20px;
        box-shadow: {shadow};
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 1.6rem 2rem;
        margin-bottom: 1.2rem;
        text-align: center;
    }}
    .header-card h1 {{
        margin: 0 0 0.25rem 0;
        font-size: 1.65rem;
        font-weight: 700;
        color: {text_color} !important;
        letter-spacing: -0.02em;
    }}
    .header-card p {{
        margin: 0;
        font-size: 0.9rem;
        color: {text_muted} !important;
        font-weight: 400;
    }}

    /* ─── Info Card (small) ─── */
    .info-card {{
        background: {glass_bg};
        border: 1px solid {glass_border};
        border-radius: 16px;
        box-shadow: {shadow};
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 1rem 1.25rem;
        margin: 0.4rem 0;
        font-size: 0.88rem;
        line-height: 1.65;
        color: {text_color} !important;
    }}
    .info-card strong {{
        color: {accent} !important;
    }}

    /* ─── Buttons — flat, neutral ─── */
    .stButton > button {{
        background: {btn_bg} !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.55rem 1.25rem !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif !important;
        transition: background 0.2s ease !important;
        box-shadow: none !important;
    }}
    .stButton > button:hover {{
        background: {btn_hover} !important;
    }}

    /* ─── Sliders ─── */
    .stSlider > div > div > div {{
        background: {accent} !important;
    }}
    .stSlider [data-testid="stThumbValue"],
    .stSlider [data-baseweb="slider"] div {{
        color: {text_color} !important;
    }}

    /* ─── Selects / Inputs ─── */
    .stSelectbox label,
    .stSlider label,
    .stNumberInput label,
    .stCheckbox label {{
        color: {text_color} !important;
    }}
    .stSelectbox [data-baseweb="select"] {{
        background: {input_bg} !important;
        border: 1px solid {input_border} !important;
        border-radius: 10px !important;
    }}
    .stSelectbox [data-baseweb="select"] span,
    .stSelectbox [data-baseweb="select"] div {{
        color: {text_color} !important;
    }}
    .stNumberInput input {{
        color: {text_color} !important;
        background: {input_bg} !important;
        border: 1px solid {input_border} !important;
        border-radius: 8px !important;
    }}
    .stCheckbox span {{
        color: {text_color} !important;
    }}

    /* ─── Main content area markdown ─── */
    .stMarkdown p,
    .stMarkdown strong,
    .stMarkdown code {{
        color: {text_color} !important;
    }}

    /* ─── Plotly container ─── */
    .stPlotlyChart {{
        border-radius: 20px;
        overflow: hidden;
        box-shadow: {shadow};
    }}

    /* ─── Footer ─── */
    .footer-bar {{
        background: {glass_bg};
        border: 1px solid {glass_border};
        border-radius: 14px;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 0.7rem 1.25rem;
        text-align: center;
        font-size: 0.8rem;
        color: {text_muted} !important;
        margin-top: 1.5rem;
    }}

    /* ─── Sidebar section labels ─── */
    .sidebar-label {{
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: {text_muted} !important;
        margin-bottom: 0.35rem;
        padding-left: 2px;
    }}

    /* ─── Responsive ─── */
    @media (max-width: 768px) {{
        .header-card h1 {{ font-size: 1.3rem; }}
        .header-card {{ padding: 1.2rem 1rem; }}
        .glass-card {{ padding: 1rem; border-radius: 16px; }}
        .info-card {{ padding: 0.8rem 1rem; }}
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# Apply CSS
# ──────────────────────────────────────────────────────────────────────────────
inject_css(dark=st.session_state.dark_mode)

# ──────────────────────────────────────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="header-card">
        <h1>Interactive 3D Math Visualizer</h1>
        <p>Explore mathematical surfaces with real-time parameter control and animation</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────────────────
# Sidebar Controls
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-label">Theme</div>', unsafe_allow_html=True)
    theme_label = "Switch to Light Mode" if st.session_state.dark_mode else "Switch to Dark Mode"
    if st.button(theme_label, width="stretch"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    st.markdown("---")

    # ── Function ──
    st.markdown('<div class="sidebar-label">Function</div>', unsafe_allow_html=True)
    func_names = get_function_names()
    selected_func = st.selectbox(
        "Select a surface function",
        func_names,
        index=0,
        label_visibility="collapsed",
    )

    desc = get_description(selected_func)
    st.markdown(
        f'<div class="info-card"><strong>Description:</strong> {desc}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── Parameter ──
    st.markdown('<div class="sidebar-label">Parameter</div>', unsafe_allow_html=True)
    default_a = get_default_param(selected_func)
    param_a = st.slider(
        "Parameter  a",
        min_value=-5.0,
        max_value=5.0,
        value=default_a,
        step=0.1,
        help="Controls the scaling / shape of the surface.",
    )

    st.markdown("---")

    # ── Grid & Rendering ──
    st.markdown('<div class="sidebar-label">Grid &amp; Rendering</div>', unsafe_allow_html=True)
    resolution = st.slider(
        "Grid Resolution",
        min_value=20,
        max_value=150,
        value=100,
        step=5,
        help="Higher = smoother surface but slower.",
    )

    x_range = st.slider(
        "X Range",
        min_value=-10.0,
        max_value=10.0,
        value=(-5.0, 5.0),
        step=0.5,
    )

    y_range = st.slider(
        "Y Range",
        min_value=-10.0,
        max_value=10.0,
        value=(-5.0, 5.0),
        step=0.5,
    )

    colormap = st.selectbox("Colormap", COLORMAPS, index=0)

    show_contour = st.checkbox("Show Z-contour projection", value=False)

    st.markdown("---")

    # ── Transformations ──
    st.markdown('<div class="sidebar-label">Transformations</div>', unsafe_allow_html=True)
    scale_factor = st.slider("Z Scale", 0.1, 5.0, 1.0, 0.1)
    z_offset = st.slider("Z Offset", -10.0, 10.0, 0.0, 0.5)
    rotation_angle = st.slider("XY Rotation (°)", 0, 360, 0, 5)

    st.markdown("---")

    # ── Animation ──
    st.markdown('<div class="sidebar-label">Animation</div>', unsafe_allow_html=True)
    animate = st.checkbox("Enable parameter animation", value=False)
    if animate:
        anim_start = st.number_input("Start a", value=0.1, step=0.1)
        anim_end = st.number_input("End a", value=3.0, step=0.1)
        anim_steps = st.slider("Frames", 10, 60, 30)
        anim_bounce = st.checkbox("Bounce (loop)", value=True)

    st.markdown("---")

    # ── Reset ──
    if st.button("Reset to Defaults", width="stretch"):
        st.session_state.dark_mode = False
        st.rerun()

# ──────────────────────────────────────────────────────────────────────────────
# Computation
# ──────────────────────────────────────────────────────────────────────────────

X, Y = generate_grid(x_range=x_range, y_range=y_range, resolution=resolution)

if rotation_angle != 0:
    X, Y = rotate_surface_z(X, Y, angle_deg=rotation_angle)

Z = compute_surface(selected_func, X, Y, a=param_a)
Z = scale_surface(Z, factor=scale_factor)
Z = translate_surface(Z, offset=z_offset)

# ──────────────────────────────────────────────────────────────────────────────
# Visualization
# ──────────────────────────────────────────────────────────────────────────────

if animate:
    a_values = generate_parameter_sweep(
        start=anim_start,
        end=anim_end,
        steps=anim_steps,
        bounce=anim_bounce,
    )
    func_callable = FUNCTION_REGISTRY[selected_func]["func"]
    fig = create_animation_frames(
        X, Y,
        func=func_callable,
        a_values=a_values,
        colormap=colormap,
        dark_mode=st.session_state.dark_mode,
    )
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f"**Animating** `{selected_func}` — parameter sweep **a** ∈ [{anim_start}, {anim_end}]")
    st.plotly_chart(fig, width="stretch", key="anim_plot")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    func_entry = selected_func.split("  ")[1] if "  " in selected_func else selected_func
    title = f"{func_entry}  |  a = {param_a}"
    fig = create_surface_figure(
        X, Y, Z,
        colormap=colormap,
        title=title,
        dark_mode=st.session_state.dark_mode,
        show_contour=show_contour,
    )
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.plotly_chart(fig, width="stretch", key="main_plot")
    st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# CG Concepts (info row)
# ──────────────────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="info-card">
            <strong>Mesh Grid</strong><br>
            NumPy generates a 2D grid of (X, Y) points. Each point is evaluated
            through the selected function to produce Z heights.
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="info-card">
            <strong>Color Mapping</strong><br>
            Height-based color gradients map Z values to a color spectrum,
            revealing surface topology at a glance.
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="info-card">
            <strong>Transformations</strong><br>
            Scaling, rotation, and translation are core CG operations.
            Adjust them in the sidebar to see real-time surface changes.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ──────────────────────────────────────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="footer-bar">
        Interactive 3D Visualization of Mathematical Functions &mdash; Computer Graphics Academic Project
        &nbsp;&middot;&nbsp; Python &middot; NumPy &middot; Plotly &middot; Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
