#!/usr/bin/env python3
"""
Demo Normal N-Queens Problem (Kelompok 22)
Mendemonstrasikan penyelesaian Decision, Counting, dan Enumeration dengan berbagai algoritma.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.normal_nqueens.optimized_backtracking import OptimizedBacktrackingNQueens
from src.normal_nqueens.bitwise_solver import BitwiseNQueens
from src.visualizer.ascii_renderer import render_normal_ascii
from src.visualizer.plot_renderer import plot_normal_solution


def main():
    print("=" * 60)
    print("DEMO NORMAL N-QUEENS PROBLEM (N = 8)")
    print("=" * 60)

    n = 8
    # 1. Optimized Backtracking (Slide Dosen)
    solver = OptimizedBacktrackingNQueens(n)
    sol, stats_dec = solver.solve_decision()

    print(f"\n[1] 1 Solusi Pertama (Decision) via Optimized Backtracking:")
    print(render_normal_ascii(sol))
    print(f"Posisi Kolom: {sol}")
    print(f"Waktu: {stats_dec['time_seconds']:.6f} detik | Node: {stats_dec['nodes_explored']} | Pruned: {stats_dec['pruned_branches']}")

    # Simpan Gambar
    plot_normal_solution(sol, "output/demo_normal_8queens.png")

    # 2. Counting via Bitwise Solver
    bitwise_solver = BitwiseNQueens(n)
    total_sols, stats_cnt = bitwise_solver.solve_counting()
    print(f"\n[2] Total Solusi (Counting) via Bitwise Solver:")
    print(f"Total Solusi Valid N={n}: {total_sols} (Sesuai OEIS A000170)")
    print(f"Waktu: {stats_cnt['time_seconds']:.6f} detik | Panggilan Rekursif: {stats_cnt['recursive_calls']}")


if __name__ == "__main__":
    main()
