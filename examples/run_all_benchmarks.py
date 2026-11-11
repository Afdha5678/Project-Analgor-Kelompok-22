#!/usr/bin/env python3
"""
Eksekusi Benchmark Komparatif Menyeluruh & Ekspor Hasil
Kelompok 22 - Analisis Algoritme
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.benchmark.benchmark_engine import BenchmarkEngine


def main():
    print("=" * 70)
    print("MENJALANKAN BENCHMARK KOMPARATIF MENYELURUH (N = 4 s.d 12)")
    print("=" * 70)

    engine = BenchmarkEngine()
    engine.run_suite(list(range(4, 13)))

    print("\nHASIL BENCHMARK:")
    print(engine.format_table())

    csv_path = "output/benchmark_results.csv"
    engine.export_csv(csv_path)
    engine.plot_charts("output")
    print(f"\n[Selesai] Semua data dan plot telah disimpan di folder output/.")


if __name__ == "__main__":
    main()
