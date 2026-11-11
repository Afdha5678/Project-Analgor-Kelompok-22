#!/usr/bin/env python3
"""
Demo Blocked N-Queens Problem (Kelompok 22)
Berdasarkan riset Gabriel Gimenez Franz.
Mendemonstrasikan efek rintangan (walls) yang menghalangi garis pandang serangan,
memungkinkan penempatan 9 ratu pada papan 8x8, serta mencari Nilai Papan (Board Value).
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.blocked_nqueens.puzzle_presets import get_preset_board, PRESETS
from src.blocked_nqueens.blocked_solver import BlockedNQueensSolver
from src.visualizer.ascii_renderer import render_blocked_ascii
from src.visualizer.plot_renderer import plot_blocked_solution


def main():
    print("=" * 60)
    print("DEMO BLOCKED N-QUEENS PROBLEM (GABRIEL GIMENEZ FRANZ)")
    print("=" * 60)

    # 1. High-Value Board: 9 Ratu pada Papan 8x8
    print("\n--- 1. HIGH-VALUE BOARD (9 Ratu pada Papan 8x8 dengan 4 Tembok) ---")
    board_9 = get_preset_board("high_value_9_queens")
    solver_9 = BlockedNQueensSolver(board_9)
    sol_9, stats_9 = solver_9.solve_decision(9)

    if sol_9:
        print(f"Solusi 9 Ratu Ditemukan dalam {stats_9['time_seconds']:.6f} detik:")
        print(render_blocked_ascii(board_9, sol_9))
        plot_blocked_solution(board_9, sol_9, "output/demo_blocked_9queens.png")

    # 2. Optimal Board Value
    print("\n--- 2. MENCARI NILAI PAPAN (BOARD VALUE) PADA PRESET 4-W SYMMETRICAL ---")
    board_sym = get_preset_board("4-W_symmetrical")
    solver_sym = BlockedNQueensSolver(board_sym)
    val, best, stats_val = solver_sym.find_board_value()
    print(f"Nilai Papan (Board Value) = {val} Ratu!")
    print(render_blocked_ascii(board_sym, best))
    plot_blocked_solution(board_sym, best, "output/demo_blocked_4w_value.png")


if __name__ == "__main__":
    main()
