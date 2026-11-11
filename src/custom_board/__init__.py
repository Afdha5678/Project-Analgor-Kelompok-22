"""
Modul Custom Board N-Queens Problem
Mendukung berbagai topologi dan geometri bidang kustom:
- Rectangular Board (M x N)
- Irregular / Masked Board (Diamond, Circle, Triangle, Cross, Custom ASCII)
- Toroidal Board (Wrap-around Diagonals - Teorema Polya)
"""

from .board_shapes import (
    CustomBoard,
    RectangularBoard,
    MaskedBoard,
    ToroidalBoard,
    create_diamond_board,
    create_circle_board,
    create_triangle_board,
    create_cross_board,
    create_hole_board,
    board_from_ascii
)
from .custom_solver import CustomBoardSolver

__all__ = [
    "CustomBoard",
    "RectangularBoard",
    "MaskedBoard",
    "ToroidalBoard",
    "create_diamond_board",
    "create_circle_board",
    "create_triangle_board",
    "create_cross_board",
    "create_hole_board",
    "board_from_ascii",
    "CustomBoardSolver"
]
