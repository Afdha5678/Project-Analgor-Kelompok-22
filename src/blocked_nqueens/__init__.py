"""
Modul Blocked N-Queens Problem
Berdasarkan riset dan konsep Gabriel Gimenez Franz (blocked-n-queens).
Ratu tidak dapat diletakkan di atas rintangan (walls/pawns),
dan rintangan menghalangi garis pandang serangan ratu (sight blocking).
"""

from .blocked_board import BlockedBoard
from .blocked_solver import BlockedNQueensSolver
from .puzzle_presets import (
    get_preset_board,
    list_presets,
    create_random_blocked_board
)

__all__ = [
    "BlockedBoard",
    "BlockedNQueensSolver",
    "get_preset_board",
    "list_presets",
    "create_random_blocked_board"
]
