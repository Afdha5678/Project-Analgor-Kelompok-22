"""
Grafis Visualizer menggunakan Matplotlib untuk merender papan catur ke berkas gambar (PNG).
"""

import os
from typing import List, Tuple, Optional, Any
from ..custom_board.board_shapes import CustomBoard


def plot_normal_solution(pos: List[int], save_path: str, title: Optional[str] = None):
    """
    Menyimpan plot papan catur N-Queens standar ke file PNG.
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
    except ImportError:
        print("[Warning] Matplotlib tidak terpasang. Simpan gambar dilewati.")
        return

    n = len(pos)
    fig, ax = plt.subplots(figsize=(6, 6))

    # Warna kotak-kotak catur
    light_color = "#F0D9B5"
    dark_color = "#B58863"

    for r in range(n):
        for c in range(n):
            color = light_color if (r + c) % 2 == 0 else dark_color
            ax.add_patch(patches.Rectangle((c, n - 1 - r), 1, 1, facecolor=color, edgecolor="black", linewidth=0.5))

    # Ratu
    for r in range(n):
        c = pos[r]
        if c != -1:
            ax.text(c + 0.5, n - 1 - r + 0.5, "Q", fontsize=max(14, 220 // n), ha="center", va="center", color="#D32F2F", fontweight="bold")

    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_xticks([i + 0.5 for i in range(n)])
    ax.set_yticks([i + 0.5 for i in range(n)])
    ax.set_xticklabels(list(range(n)))
    ax.set_yticklabels(list(reversed(range(n))))
    ax.set_aspect("equal")

    if title:
        plt.title(title, fontsize=12, fontweight="bold", pad=12)
    else:
        plt.title(f"Normal {n}-Queens Solution", fontsize=12, fontweight="bold", pad=12)

    os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200)
    plt.close()
    print(f"[Plot] Gambar tersimpan di: {save_path}")


def plot_custom_solution(board: CustomBoard, queens: List[Tuple[int, int]], save_path: str, title: Optional[str] = None):
    """
    Menyimpan plot papan kustom ke file PNG.
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
    except ImportError:
        print("[Warning] Matplotlib tidak terpasang. Simpan gambar dilewati.")
        return

    rows = board.rows
    cols = board.cols
    queen_set = set(queens)

    fig, ax = plt.subplots(figsize=(max(5, cols * 0.8), max(5, rows * 0.8)))

    light_color = "#E8EDF9"
    dark_color = "#B8C0D8"
    inactive_color = "#2E2E2E"

    for r in range(rows):
        for c in range(cols):
            y = rows - 1 - r
            if not board.is_valid_cell(r, c):
                ax.add_patch(patches.Rectangle((c, y), 1, 1, facecolor=inactive_color, edgecolor="#444444", linewidth=0.5))
            else:
                color = light_color if (r + c) % 2 == 0 else dark_color
                ax.add_patch(patches.Rectangle((c, y), 1, 1, facecolor=color, edgecolor="black", linewidth=0.5))

    for r, c in queens:
        y = rows - 1 - r
        ax.text(c + 0.5, y + 0.5, "Q", fontsize=max(14, 180 // max(rows, cols)), ha="center", va="center", color="#C2185B", fontweight="bold")

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_xticks([i + 0.5 for i in range(cols)])
    ax.set_yticks([i + 0.5 for i in range(rows)])
    ax.set_xticklabels(list(range(cols)))
    ax.set_yticklabels(list(reversed(range(rows))))
    ax.set_aspect("equal")

    if title:
        plt.title(title, fontsize=12, fontweight="bold", pad=12)
    else:
        plt.title(f"Custom Board Solution ({len(queens)} Queens)", fontsize=12, fontweight="bold", pad=12)

    os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200)
    plt.close()
    print(f"[Plot] Gambar tersimpan di: {save_path}")


def plot_blocked_solution(board, queens: List[Tuple[int, int]], save_path: str, title: Optional[str] = None):
    """
    Menyimpan plot papan Blocked N-Queens ke file PNG.
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
    except ImportError:
        print("[Warning] Matplotlib tidak terpasang. Simpan gambar dilewati.")
        return

    rows = board.rows
    cols = board.cols
    queen_set = set(queens)

    fig, ax = plt.subplots(figsize=(max(5, cols * 0.8), max(5, rows * 0.8)))

    light_color = "#EEEED2"
    dark_color = "#769656"
    wall_color = "#3E2723"

    for r in range(rows):
        for c in range(cols):
            y = rows - 1 - r
            if board.is_wall(r, c):
                ax.add_patch(patches.Rectangle((c, y), 1, 1, facecolor=wall_color, edgecolor="black", linewidth=1.0))
                ax.text(c + 0.5, y + 0.5, "#", fontsize=max(12, 160 // max(rows, cols)), ha="center", va="center", color="#FFFFFF", fontweight="bold")
            else:
                color = light_color if (r + c) % 2 == 0 else dark_color
                ax.add_patch(patches.Rectangle((c, y), 1, 1, facecolor=color, edgecolor="black", linewidth=0.5))

    for r, c in queens:
        y = rows - 1 - r
        ax.text(c + 0.5, y + 0.5, "Q", fontsize=max(14, 180 // max(rows, cols)), ha="center", va="center", color="#D50000", fontweight="bold")

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_xticks([i + 0.5 for i in range(cols)])
    ax.set_yticks([i + 0.5 for i in range(rows)])
    ax.set_xticklabels(list(range(cols)))
    ax.set_yticklabels(list(reversed(range(rows))))
    ax.set_aspect("equal")

    if title:
        plt.title(title, fontsize=12, fontweight="bold", pad=12)
    else:
        plt.title(f"Blocked N-Queens Solution ({len(queens)} Queens, {board.num_walls} Walls)", fontsize=12, fontweight="bold", pad=12)

    os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200)
    plt.close()
    print(f"[Plot] Gambar tersimpan di: {save_path}")
