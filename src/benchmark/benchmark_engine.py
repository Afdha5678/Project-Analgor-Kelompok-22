"""
Mesin Pengujian Kinerja (Benchmark Engine) untuk Analisis Algoritme N-Queens.
Mengukur waktu eksekusi, penggunaan memori (tracemalloc), jumlah node yang dieksplorasi,
serta menghasilkan tabel komparasi dan grafik.
"""

import time
import tracemalloc
import csv
import os
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

from ..normal_nqueens.brute_force import BruteForceNQueens
from ..normal_nqueens.standard_backtracking import StandardBacktrackingNQueens
from ..normal_nqueens.optimized_backtracking import OptimizedBacktrackingNQueens
from ..normal_nqueens.bitwise_solver import BitwiseNQueens


@dataclass
class BenchmarkResult:
    n: int
    algorithm: str
    mode: str
    time_seconds: float
    nodes_or_calls: int
    peak_memory_kb: float
    solutions_count: int


class BenchmarkEngine:
    """
    Menjalankan pengujian multi-algoritma pada berbagai nilai N.
    """

    def __init__(self):
        self.results: List[BenchmarkResult] = []

    def run_single(self, algorithm_name: str, n: int, mode: str = "counting") -> BenchmarkResult:
        """Menjalankan 1 algoritma untuk N tertentu."""
        tracemalloc.start()
        start_time = time.perf_counter()

        sol_count = 0
        nodes = 0

        if algorithm_name == "Brute Force":
            solver = BruteForceNQueens(n)
            if mode == "decision":
                sol, stats = solver.solve_decision()
                sol_count = 1 if sol else 0
            else:
                sol_count, stats = solver.solve_counting()
            nodes = stats["nodes_checked"]

        elif algorithm_name == "Standard Backtracking":
            solver = StandardBacktrackingNQueens(n)
            if mode == "decision":
                sol, stats = solver.solve_decision()
                sol_count = 1 if sol else 0
            else:
                sol_count, stats = solver.solve_counting()
            nodes = stats["nodes_explored"]

        elif algorithm_name == "Optimized Backtracking":
            solver = OptimizedBacktrackingNQueens(n)
            if mode == "decision":
                sol, stats = solver.solve_decision()
                sol_count = 1 if sol else 0
            else:
                sol_count, stats = solver.solve_counting()
            nodes = stats["nodes_explored"]

        elif algorithm_name == "Bitwise Backtracking":
            solver = BitwiseNQueens(n)
            if mode == "decision":
                sol, stats = solver.solve_decision()
                sol_count = 1 if sol else 0
            else:
                sol_count, stats = solver.solve_counting()
            nodes = stats["recursive_calls"]
        else:
            raise ValueError(f"Algoritma '{algorithm_name}' tidak dikenal")

        elapsed = time.perf_counter() - start_time
        current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        res = BenchmarkResult(
            n=n,
            algorithm=algorithm_name,
            mode=mode,
            time_seconds=elapsed,
            nodes_or_calls=nodes,
            peak_memory_kb=peak_mem / 1024.0,
            solutions_count=sol_count
        )
        self.results.append(res)
        return res

    def run_suite(self, n_range: List[int], algorithms: Optional[List[str]] = None, mode: str = "counting") -> List[BenchmarkResult]:
        """
        Menjalankan rangkaian benchmark untuk rentang N.
        Otomatis membatasi Brute Force pada N <= 9 agar tidak hang.
        """
        if algorithms is None:
            algorithms = [
                "Brute Force",
                "Standard Backtracking",
                "Optimized Backtracking",
                "Bitwise Backtracking"
            ]

        suite_results = []
        for n in n_range:
            for algo in algorithms:
                if algo == "Brute Force" and n > 8:
                    continue  # Lewati brute force untuk n >= 9 agar benchmark efisien
                if algo == "Standard Backtracking" and n > 12:
                    continue  # Lewati standard backtracking lambat untuk N > 12

                res = self.run_single(algo, n, mode=mode)
                suite_results.append(res)
        return suite_results

    def format_table(self) -> str:
        """Menghasilkan representasi string tabel perbandingan kinerja."""
        if not self.results:
            return "Belum ada data benchmark."

        header = f"{'N':>3} | {'Algorithm':<24} | {'Solutions':>10} | {'Nodes/Calls':>12} | {'Time (s)':>11} | {'Peak Mem (KB)':>13}"
        separator = "-" * len(header)
        lines = [separator, header, separator]

        for r in self.results:
            lines.append(
                f"{r.n:3d} | {r.algorithm:<24} | {r.solutions_count:10d} | {r.nodes_or_calls:12d} | {r.time_seconds:11.6f} | {r.peak_memory_kb:13.2f}"
            )
        lines.append(separator)
        return "\n".join(lines)

    def export_csv(self, file_path: str):
        """Mengekspor hasil benchmark ke berkas CSV."""
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["N", "Algorithm", "Mode", "Time_Seconds", "Nodes_Calls", "Peak_Memory_KB", "Solutions"])
            for r in self.results:
                writer.writerow([r.n, r.algorithm, r.mode, r.time_seconds, r.nodes_or_calls, r.peak_memory_kb, r.solutions_count])
        print(f"[Benchmark] Data diekspor ke: {file_path}")

    def plot_charts(self, save_dir: str):
        """Membuat grafik perbandingan waktu eksekusi dan node (membutuhkan matplotlib)."""
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("[Warning] Matplotlib tidak ditemukan. Plot grafik dilewati.")
            return

        if not self.results:
            return

        os.makedirs(save_dir, exist_ok=True)

        # Kelompokkan data per algoritma
        algo_data: Dict[str, Dict[str, list]] = {}
        for r in self.results:
            if r.algorithm not in algo_data:
                algo_data[r.algorithm] = {"n": [], "time": [], "nodes": []}
            algo_data[r.algorithm]["n"].append(r.n)
            algo_data[r.algorithm]["time"].append(r.time_seconds)
            algo_data[r.algorithm]["nodes"].append(r.nodes_or_calls)

        # 1. Grafik Waktu Eksekusi (Skala Logaritmik)
        plt.figure(figsize=(9, 5.5))
        markers = {"Brute Force": "o", "Standard Backtracking": "s", "Optimized Backtracking": "^", "Bitwise Backtracking": "D"}
        colors = {"Brute Force": "#D32F2F", "Standard Backtracking": "#F57C00", "Optimized Backtracking": "#1976D2", "Bitwise Backtracking": "#388E3C"}

        for algo, data in algo_data.items():
            plt.plot(
                data["n"],
                data["time"],
                label=algo,
                marker=markers.get(algo, "o"),
                color=colors.get(algo, "#000000"),
                linewidth=2,
                markersize=6
            )

        plt.yscale("log")
        plt.xlabel("Ukuran Papan (N)", fontsize=11, fontweight="bold")
        plt.ylabel("Waktu Eksekusi (detik, log scale)", fontsize=11, fontweight="bold")
        plt.title("Perbandingan Waktu Eksekusi Algoritma N-Queens (Kelompok 22)", fontsize=12, fontweight="bold")
        plt.grid(True, which="both", ls="--", alpha=0.5)
        plt.legend(fontsize=10)
        plt.tight_layout()
        time_chart_path = os.path.join(save_dir, "benchmark_runtime.png")
        plt.savefig(time_chart_path, dpi=200)
        plt.close()
        print(f"[Benchmark] Grafik Waktu tersimpan di: {time_chart_path}")

        # 2. Grafik Jumlah Node / Panggilan Rekursif
        plt.figure(figsize=(9, 5.5))
        for algo, data in algo_data.items():
            plt.plot(
                data["n"],
                data["nodes"],
                label=algo,
                marker=markers.get(algo, "o"),
                color=colors.get(algo, "#000000"),
                linewidth=2,
                markersize=6
            )

        plt.yscale("log")
        plt.xlabel("Ukuran Papan (N)", fontsize=11, fontweight="bold")
        plt.ylabel("Node Dieksplorasi / Panggilan Rekursif (log scale)", fontsize=11, fontweight="bold")
        plt.title("Perbandingan Ruang Pencarian yang Dieksplorasi (Pruning)", fontsize=12, fontweight="bold")
        plt.grid(True, which="both", ls="--", alpha=0.5)
        plt.legend(fontsize=10)
        plt.tight_layout()
        nodes_chart_path = os.path.join(save_dir, "benchmark_nodes.png")
        plt.savefig(nodes_chart_path, dpi=200)
        plt.close()
        print(f"[Benchmark] Grafik Node tersimpan di: {nodes_chart_path}")
