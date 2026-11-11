#!/usr/bin/env python3
"""
Aplikasi Utama & Antarmuka CLI - Project Akhir Analisis Algoritme
Kelompok 22 (Paralel 2):
1. Muhammad Andhika Putra Pratama (M0403241055)
2. Azra Aslam Khoiri (M0403241148)
3. Afdha Auliya Atiq (M0403241163)

Mendukung 3 Kasus Masalah:
- Normal N-Queens Problem
- Custom Board N-Queens Problem (Geometri & Topologi Kustom)
- Blocked N-Queens Problem (Rintangan Tembok Pemblokir Pandangan)
"""

import sys
import os
import argparse
from typing import List, Tuple

# Tambahkan path src
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.normal_nqueens.brute_force import BruteForceNQueens
from src.normal_nqueens.standard_backtracking import StandardBacktrackingNQueens
from src.normal_nqueens.optimized_backtracking import OptimizedBacktrackingNQueens
from src.normal_nqueens.bitwise_solver import BitwiseNQueens

from src.custom_board.board_shapes import (
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
from src.custom_board.custom_solver import CustomBoardSolver

from src.blocked_nqueens.blocked_board import BlockedBoard
from src.blocked_nqueens.blocked_solver import BlockedNQueensSolver
from src.blocked_nqueens.puzzle_presets import get_preset_board, list_presets, PRESETS

from src.benchmark.benchmark_engine import BenchmarkEngine
from src.visualizer.ascii_renderer import (
    render_normal_ascii,
    render_custom_ascii,
    render_blocked_ascii
)
from src.visualizer.plot_renderer import (
    plot_normal_solution,
    plot_custom_solution,
    plot_blocked_solution
)


def print_banner():
    print("=" * 75)
    print("   PROJECT AKHIR ANALISIS ALGORITME (KOM206) - KELOMPOK 22 (PARALEL 2)   ")
    print("   Topik: N-Queens Problem & Variasi (Normal, Custom Board, Blocked)    ")
    print("=" * 75)
    print("Anggota Kelompok:")
    print(" 1. Muhammad Andhika Putra Pratama (M0403241055)")
    print(" 2. Azra Aslam Khoiri              (M0403241148)")
    print(" 3. Afdha Auliya Atiq              (M0403241163)")
    print("-" * 75)


def handle_normal_menu():
    print("\n[1] NORMAL N-QUEENS PROBLEM")
    try:
        n = int(input("Masukkan ukuran papan N (contoh: 8): ").strip() or "8")
    except ValueError:
        n = 8

    print("\nPilih Algoritma:")
    print(" 1. Optimized Backtracking (Array Lookup O(1) - Sesuai Slide Kuliah)")
    print(" 2. Bitwise Backtracking (Ultra-Fast Bitwise DFS)")
    print(" 3. Standard Backtracking (Pemeriksaan Baris O(N))")
    print(" 4. Brute Force Permutasi (Hanya untuk N <= 9)")
    algo_choice = input("Pilihan [1-4, default=1]: ").strip() or "1"

    print("\nPilih Mode:")
    print(" 1. Decision (Temukan 1 solusi pertama & tampilkan papan)")
    print(" 2. Counting (Hitung total seluruh solusi)")
    print(" 3. Enumeration (Tampilkan semua solusi)")
    mode_choice = input("Pilihan [1-3, default=1]: ").strip() or "1"

    algo_map = {
        "1": ("Optimized Backtracking", OptimizedBacktrackingNQueens(n)),
        "2": ("Bitwise Backtracking", BitwiseNQueens(n)),
        "3": ("Standard Backtracking", StandardBacktrackingNQueens(n)),
        "4": ("Brute Force", BruteForceNQueens(n))
    }
    algo_name, solver = algo_map.get(algo_choice, algo_map["1"])

    print(f"\nMenjalankan {algo_name} untuk N = {n}...")

    if mode_choice == "1":
        sol, stats = solver.solve_decision()
        if sol:
            print(f"\n[SUKSES] Solusi Ditemukan dalam {stats['time_seconds']:.6f} detik:")
            print(render_normal_ascii(sol))
            print(f"Posisi Kolom Ratu (baris 0 s.d {n-1}): {sol}")
            out_img = f"output/normal_n{n}_solution.png"
            plot_normal_solution(sol, out_img)
        else:
            print(f"[GAGAL] Tidak ada solusi untuk N = {n} (waktu: {stats['time_seconds']:.6f} detik).")
        print(f"Statistik: {stats}")

    elif mode_choice == "2":
        count, stats = solver.solve_counting()
        print(f"\n[HASIL COUNTING] Total Solusi Valid untuk N = {n}: {count}")
        print(f"Waktu Eksekusi: {stats['time_seconds']:.6f} detik")
        print(f"Statistik: {stats}")

    elif mode_choice == "3":
        sols, stats = solver.solve_enumeration()
        print(f"\n[HASIL ENUMERATION] Ditemukan {len(sols)} solusi untuk N = {n}:")
        limit = min(5, len(sols))
        for i in range(limit):
            print(f"\n--- Solusi #{i+1} ---")
            print(render_normal_ascii(sols[i]))
        if len(sols) > limit:
            print(f"\n... dan {len(sols) - limit} solusi lainnya.")
        print(f"Waktu Eksekusi: {stats['time_seconds']:.6f} detik")


def handle_custom_menu():
    print("\n[2] CUSTOM BOARD N-QUEENS PROBLEM")
    print("Pilih Bentuk Geometri / Topologi Bidang:")
    print(" 1. Rectangular Board (Persegi Panjang M x N)")
    print(" 2. Diamond / Belah Ketupat (Radius R)")
    print(" 3. Circular / Lingkaran (Radius R)")
    print(" 4. Triangular / Tangga Segitiga (Height H)")
    print(" 5. Cross / Tanda Tambah (Palang Simetris)")
    print(" 6. Toroidal Board (Wrap-around Diagonals - Teorema Polya)")
    print(" 7. Papan Berlubang (Center Hole Board)")
    print(" 8. Papan Kustom dari Input Teks ASCII")

    choice = input("Pilihan [1-8, default=2]: ").strip() or "2"

    if choice == "1":
        m = int(input("Jumlah baris M: ").strip() or "6")
        n = int(input("Jumlah kolom N: ").strip() or "8")
        k = int(input(f"Jumlah ratu K [default={min(m, n)}]: ").strip() or str(min(m, n)))
        board = RectangularBoard(m, n, k_queens=k)
    elif choice == "2":
        r = int(input("Radius Diamond R [default=3 -> grid 7x7]: ").strip() or "3")
        k = int(input(f"Jumlah ratu K [default={2*r}]: ").strip() or str(2 * r))
        board = create_diamond_board(r, k_queens=k)
    elif choice == "3":
        r = int(input("Radius Lingkaran R [default=3]: ").strip() or "3")
        k = int(input(f"Jumlah ratu K [default={2*r}]: ").strip() or str(2 * r))
        board = create_circle_board(r, k_queens=k)
    elif choice == "4":
        h = int(input("Tinggi Tangga H [default=6]: ").strip() or "6")
        board = create_triangle_board(h)
    elif choice == "5":
        arm = int(input("Panjang Lengan [default=2]: ").strip() or "2")
        mid = int(input("Lebar Pusat [default=3]: ").strip() or "3")
        board = create_cross_board(arm, mid)
    elif choice == "6":
        n = int(input("Dimensi Torus N [solusi ada jika gcd(N,6)==1, misal 5, 7, 11]: ").strip() or "7")
        board = ToroidalBoard(n)
    elif choice == "7":
        n = int(input("Dimensi Papan N [default=8]: ").strip() or "8")
        board = create_hole_board(n, 2, 2, 4, 4)
    elif choice == "8":
        print("Masukkan ASCII art papan (. = aktif, spasi = kosong), akhiri baris kosong:")
        lines = []
        while True:
            line = input()
            if not line:
                break
            lines.append(line)
        art = "\n".join(lines) if lines else "... .\n ...\n.. .."
        board = board_from_ascii(art)
    else:
        board = create_diamond_board(3)

    solver = CustomBoardSolver(board)
    print(f"\nMemproses Papan Kustom ({board.rows}x{board.cols}, total petak aktif: {len(board.get_valid_cells())})...")

    print("\nPilih Operasi:")
    print(" 1. Cari 1 Solusi (Decision)")
    print(" 2. Hitung Total Solusi (Counting)")
    print(" 3. Cari Jumlah Ratu Maksimum (Max-Queens Optimization)")
    op = input("Pilihan [1-3, default=1]: ").strip() or "1"

    if op == "1":
        sol, stats = solver.solve_decision()
        if sol:
            print(f"\n[SUKSES] Solusi Ditemukan ({len(sol)} Ratu) dalam {stats['time_seconds']:.6f} detik:")
            print(render_custom_ascii(board, sol))
            plot_custom_solution(board, sol, "output/custom_board_solution.png")
        else:
            print(f"\n[GAGAL] Tidak ditemukan konfigurasi valid untuk {stats.get('k', 'N')} ratu.")
        print(f"Statistik: {stats}")

    elif op == "2":
        count, stats = solver.solve_counting()
        print(f"\n[HASIL COUNTING] Total Konfigurasi Valid: {count}")
        print(f"Waktu Eksekusi: {stats['time_seconds']:.6f} detik")

    elif op == "3":
        max_q, best_queens, stats = solver.find_max_queens()
        print(f"\n[MAX QUEENS OPTIMIZATION] Jumlah Ratu Maksimum Non-Attacking: {max_q}")
        print(render_custom_ascii(board, best_queens))
        plot_custom_solution(board, best_queens, "output/custom_max_queens.png")
        print(f"Statistik: {stats}")


def handle_blocked_menu():
    print("\n[3] BLOCKED N-QUEENS PROBLEM (GABRIEL GIMENEZ FRANZ VARIANT)")
    print("Rintangan (Tembok) menghalangi garis pandang serangan antar ratu!")
    print("\nPilih Sumber Papan:")
    print(" 1. Gunakan Preset Puzzles")
    print(" 2. Input Manual Koordinat Tembok")
    print(" 3. Bangkitkan Papan Acak (Random Blocked Board)")

    src_choice = input("Pilihan [1-3, default=1]: ").strip() or "1"

    if src_choice == "1":
        print("\nDaftar Preset Tersedia:")
        presets = list_presets()
        for idx, p in enumerate(presets):
            print(f" {idx+1}. {p['name']} ({p['walls_count']} tembok) - {p['description']}")
        p_idx = int(input(f"Pilih nomor preset [1-{len(presets)}, default=6]: ").strip() or "6") - 1
        p_key = presets[max(0, min(len(presets)-1, p_idx))]["key"]
        board = get_preset_board(p_key)
        print(f"\nMemuat Preset: {PRESETS[p_key]['name']}")

    elif src_choice == "2":
        n = int(input("Ukuran Papan N [default=8]: ").strip() or "8")
        board = BlockedBoard(n)
        print("Masukkan koordinat tembok r c (contoh: '2 3', akhiri baris kosong):")
        while True:
            coord = input().strip()
            if not coord:
                break
            parts = coord.split()
            if len(parts) >= 2:
                board.add_wall(int(parts[0]), int(parts[1]))

    elif src_choice == "3":
        n = int(input("Ukuran Papan N [default=8]: ").strip() or "8")
        w = int(input("Jumlah Tembok Acak [default=4]: ").strip() or "4")
        from src.blocked_nqueens.puzzle_presets import create_random_blocked_board
        board = create_random_blocked_board(n=n, num_walls=w)
    else:
        board = get_preset_board("4-W_symmetrical")

    print("\nKondisi Awal Papan Blocked N-Queens:")
    print(render_blocked_ascii(board, []))

    solver = BlockedNQueensSolver(board)

    print("\nPilih Mode Analisis:")
    print(" 1. Cari Nilai Papan (Board Value / Maximum Queens Optimization)")
    print(" 2. Cari Solusi Penempatan K Ratu (Decision)")
    print(" 3. Hitung Jumlah Solusi Penempatan K Ratu (Counting)")
    b_mode = input("Pilihan [1-3, default=1]: ").strip() or "1"

    if b_mode == "1":
        print("\nMenghitung Nilai Papan (Maksimum Ratu)...")
        val, best_placement, stats = solver.find_board_value()
        print(f"\n[SUKSES] NILAI PAPAN (BOARD VALUE) = {val} Ratu!")
        print(f"Waktu Pencarian: {stats['time_seconds']:.6f} detik ({stats['nodes_explored']} node dieksplorasi)")
        print(render_blocked_ascii(board, best_placement))
        print(f"Koordinat Posisi Ratu: {best_placement}")
        plot_blocked_solution(board, best_placement, "output/blocked_board_value.png")

    elif b_mode == "2":
        k = int(input(f"Masukkan jumlah ratu K [default={board.rows}]: ").strip() or str(board.rows))
        sol, stats = solver.solve_decision(k)
        if sol:
            print(f"\n[SUKSES] Solusi {k} Ratu Ditemukan:")
            print(render_blocked_ascii(board, sol))
            plot_blocked_solution(board, sol, f"output/blocked_{k}queens.png")
        else:
            print(f"\n[GAGAL] Tidak dapat menaruh {k} ratu tanpa saling menyerang.")
        print(f"Statistik: {stats}")

    elif b_mode == "3":
        k = int(input(f"Masukkan jumlah ratu K [default={board.rows}]: ").strip() or str(board.rows))
        count, stats = solver.solve_counting(k)
        print(f"\n[HASIL COUNTING] Total Konfigurasi Penempatan {k} Ratu: {count}")
        print(f"Waktu Eksekusi: {stats['time_seconds']:.6f} detik")


def handle_benchmark_menu():
    print("\n[4] SUITE BENCHMARK KOMPARASI ALGORITMA")
    n_min = int(input("Nilai N awal [default=4]: ").strip() or "4")
    n_max = int(input("Nilai N akhir [default=12]: ").strip() or "12")

    engine = BenchmarkEngine()
    print(f"\nMenjalankan benchmark untuk N = {n_min} s.d {n_max}...")
    engine.run_suite(list(range(n_min, n_max + 1)))

    print("\nHASIL BENCHMARK LENGKAP:")
    print(engine.format_table())

    csv_path = "output/benchmark_results.csv"
    engine.export_csv(csv_path)
    engine.plot_charts("output")
    print("\nBenchmark selesai dan grafik telah diperbarui di folder output/.")


def handle_test_menu():
    print("\n[5] MENJALANKAN AUTOMATED UNIT TESTS")
    import unittest
    loader = unittest.TestLoader()
    suite = loader.discover("tests")
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


def main():
    parser = argparse.ArgumentParser(description="Proyek Akhir Analisis Algoritme - Kelompok 22 (N-Queens)")
    parser.add_argument("--mode", choices=["normal", "custom", "blocked", "benchmark", "test", "menu"], default="menu")
    parser.add_argument("--n", type=int, default=8, help="Ukuran papan N")
    parser.add_argument("--algo", choices=["optimized", "bitwise", "standard", "brute"], default="optimized")
    parser.add_argument("--preset", type=str, default="4-W_symmetrical", help="Preset Blocked Board")
    args = parser.parse_args()

    if args.mode == "normal":
        algo_cls = {
            "optimized": OptimizedBacktrackingNQueens,
            "bitwise": BitwiseNQueens,
            "standard": StandardBacktrackingNQueens,
            "brute": BruteForceNQueens
        }[args.algo]
        solver = algo_cls(args.n)
        sol, stats = solver.solve_decision()
        print(f"Normal N-Queens N={args.n} ({args.algo}):")
        if sol:
            print(render_normal_ascii(sol))
        print(stats)
        return

    if args.mode == "benchmark":
        engine = BenchmarkEngine()
        engine.run_suite(list(range(4, args.n + 1)))
        print(engine.format_table())
        engine.export_csv("output/benchmark_results.csv")
        engine.plot_charts("output")
        return

    # Interactive Loop
    while True:
        print_banner()
        print("Pilih Menu Utama:")
        print(" 1. Kasus 1: Normal N-Queens Problem")
        print(" 2. Kasus 2: Custom Board N-Queens Problem (Bidang Kustom)")
        print(" 3. Kasus 3: Blocked N-Queens Problem (Rintangan / Tembok)")
        print(" 4. Suite Benchmark Kinerja (Tabel Komparasi & Grafik)")
        print(" 5. Jalankan Automated Unit Tests")
        print(" 0. Keluar")
        choice = input("\nMasukkan pilihan [0-5]: ").strip()

        if choice == "1":
            handle_normal_menu()
        elif choice == "2":
            handle_custom_menu()
        elif choice == "3":
            handle_blocked_menu()
        elif choice == "4":
            handle_benchmark_menu()
        elif choice == "5":
            handle_test_menu()
        elif choice == "0":
            print("\nTerima kasih! Semoga sukses proyek akhirnya.")
            break
        else:
            print("\nPilihan tidak valid.")

        input("\nTekan Enter untuk kembali ke menu utama...")


if __name__ == "__main__":
    main()
