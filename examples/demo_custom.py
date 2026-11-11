#!/usr/bin/env python3
"""
Demo Custom Board N-Queens Problem (Kelompok 22)
Mendemonstrasikan papan berbentuk Belah Ketupat (Diamond), Lingkaran (Circle),
dan Toroidal Board (Teorema George Polya).
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.custom_board.board_shapes import (
    create_diamond_board,
    create_circle_board,
    ToroidalBoard
)
from src.custom_board.custom_solver import CustomBoardSolver
from src.visualizer.ascii_renderer import render_custom_ascii
from src.visualizer.plot_renderer import plot_custom_solution


def main():
    print("=" * 60)
    print("DEMO CUSTOM BOARD N-QUEENS PROBLEM")
    print("=" * 60)

    # 1. Diamond Board (Radius 3 -> Grid 7x7)
    print("\n--- 1. DIAMOND BOARD (Radius = 3) ---")
    diamond = create_diamond_board(radius=3)
    solver_diamond = CustomBoardSolver(diamond)
    max_q, sol_d, stats_d = solver_diamond.find_max_queens()
    if sol_d:
        print(f"Solusi Optimal Max-Queens ({max_q} Ratu) pada Papan Belah Ketupat ({stats_d['time_seconds']:.6f} detik):")
        print(render_custom_ascii(diamond, sol_d))
        plot_custom_solution(diamond, sol_d, "output/demo_diamond_board.png")

    # 2. Toroidal Board - Bukti Teorema Polya
    print("\n--- 2. TOROIDAL BOARD (Wrap-Around Diagonals) ---")
    print("Teorema George Polya (1918): Solusi ada JIKA DAN HANYA JIKA gcd(N, 6) == 1.")

    for n in [4, 5, 6, 7, 8]:
        torus = ToroidalBoard(n)
        s_torus = CustomBoardSolver(torus)
        cnt, st = s_torus.solve_counting(n)
        status = "SOLUSI ADA" if cnt > 0 else "TIDAK ADA SOLUSI (0)"
        print(f"N = {n} (gcd({n}, 6) = {1 if n in [5, 7] else 2 if n%2==0 else 3}): Total Solusi = {cnt:3d} -> {status}")


if __name__ == "__main__":
    main()
