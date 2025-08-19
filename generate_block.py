"""
Generate a 3D cube block with 3 visible faces textured using an input image.
This script is ideal for creating Minecraft-like blocks for logos or assets.

Requirements:
    pip install matplotlib pillow numpy

Usage:
    python generate_block.py
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


# === Configuration ===
TEXTURE_PATH = "default_ice.png"      # Path to your texture image
OUTPUT_PATH = "block_textured.png"    # Output file name
FIGSIZE = (6, 6)                      # Figure size in inches
FACE_RES = 200                        # Texture resolution per face
ELEV_ANGLE = 30                       # Camera elevation
AZIM_ANGLE = -35                      # Camera azimuth (rotate left/right)
USE_ORTHO = True                      # Use orthographic projection
# ======================


def sample_texture(texture: np.ndarray, u: np.ndarray, v: np.ndarray) -> np.ndarray:
    """
    Sample a texture image at normalized coordinates (u, v).

    Args:
        texture: Numpy array (H, W, 4) of RGBA texture values in [0, 1].
        u: Normalized horizontal coordinates in [0,1].
        v: Normalized vertical coordinates in [0,1].

    Returns:
        RGBA values for the sampled texture coordinates.
    """
    h, w = texture.shape[:2]
    u = np.clip(u, 0, 1)
    v = np.clip(v, 0, 1)

    x = (u * (w - 1)).astype(int)
    y = (v * (h - 1)).astype(int)

    return texture[y, x]


def generate_block(texture_path: str, output_path: str):
    """
    Generate a textured cube with 3 visible faces (TOP, FRONT, RIGHT).

    Args:
        texture_path: Path to the input texture image.
        output_path: Path to save the rendered cube.
    """
    # Load texture (RGBA normalized to [0,1])
    tex = np.array(Image.open(texture_path).convert("RGBA")) / 255.0

    # Setup figure
    fig = plt.figure(figsize=FIGSIZE)
    ax = fig.add_subplot(111, projection="3d")

    L = 1.0
    u = np.linspace(0, 1, FACE_RES)
    v = np.linspace(0, 1, FACE_RES)
    U, V = np.meshgrid(u, v)

    # --- Cube faces ---
    # TOP
    X_top = U * L
    Y_top = V * L
    Z_top = np.full_like(U, L)
    C_top = sample_texture(tex, U, 1 - V)

    # FRONT (y=0)
    X_front = U * L
    Y_front = np.zeros_like(U)
    Z_front = V * L
    C_front = sample_texture(tex, U, 1 - V)

    # RIGHT (x=L)
    X_right = np.full_like(U, L)
    Y_right = U * L
    Z_right = V * L
    C_right = sample_texture(tex, U, 1 - V)

    # Plot order: right → front → top
    ax.plot_surface(X_right, Y_right, Z_right, facecolors=C_right,
                    rstride=1, cstride=1, linewidth=0, antialiased=False, shade=False)
    ax.plot_surface(X_front, Y_front, Z_front, facecolors=C_front,
                    rstride=1, cstride=1, linewidth=0, antialiased=False, shade=False)
    ax.plot_surface(X_top,   Y_top,   Z_top,   facecolors=C_top,
                    rstride=1, cstride=1, linewidth=0, antialiased=False, shade=False)

    # Axis/limits
    ax.set_xlim(0, L)
    ax.set_ylim(0, L)
    ax.set_zlim(0, L)
    ax.set_box_aspect([1, 1, 1])
    ax.axis("off")

    # Camera
    ax.view_init(elev=ELEV_ANGLE, azim=AZIM_ANGLE)
    if USE_ORTHO:
        ax.set_proj_type("ortho")

    # Save
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.savefig(output_path, dpi=300, transparent=True)
    plt.close(fig)

    print(f"Block saved to: {output_path}")


if __name__ == "__main__":
    generate_block(TEXTURE_PATH, OUTPUT_PATH)
