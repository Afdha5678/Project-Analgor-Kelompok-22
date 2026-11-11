"""
Implementasi Brute Force untuk Normal N-Queens Problem.
Membangkitkan seluruh permutasi kolom O(N!) dan memvalidasi kondisi diagonal.
"""

import time
import itertools
from typing import List, Optional, Tuple, Dict, Any


class BruteForceNQueens:
    """
    Solver N-Queens berbasis Brute Force / Complete Search Permutasi.
    Secara implisit memastikan setiap baris dan kolom hanya memiliki 1 ratu,
    kemudian menguji apakah ada dua ratu pada diagonal yang sama.
    Kompleksitas Waktu: O(N * N!)
    Kompleksitas Ruang: O(N)
    """

    def __init__(self, n: int):
        if n < 1:
            raise ValueError("Ukuran papan N harus >= 1")
        self.n = n

    def _is_valid_diagonal(self, perm: Tuple[int, ...]) -> bool:
        """
        Memeriksa apakah ada 2 ratu yang saling menyerang secara diagonal.
        Ratu di (i, perm[i]) dan (j, perm[j]) saling serang jika:
        |i - j| == |perm[i] - perm[j]|
        """
        n = self.n
        for i in range(n):
            for j in range(i + 1, n):
                if abs(i - j) == abs(perm[i] - perm[j]):
                    return False
        return True

    def solve_decision(self) -> Tuple[Optional[List[int]], Dict[str, Any]]:
        """
        Mencari 1 solusi pertama (Decision).
        Return: (posisi_ratu, stats)
        """
        start_time = time.perf_counter()
        nodes_checked = 0
        solution = None

        for perm in itertools.permutations(range(self.n)):
            nodes_checked += 1
            if self._is_valid_diagonal(perm):
                solution = list(perm)
                break

        elapsed = time.perf_counter() - start_time
        stats = {
            "n": self.n,
            "mode": "decision",
            "algorithm": "Brute Force",
            "nodes_checked": nodes_checked,
            "time_seconds": elapsed,
            "found": solution is not None
        }
        return solution, stats

    def solve_counting(self) -> Tuple[int, Dict[str, Any]]:
        """
        Menghitung total seluruh solusi valid (Counting).
        """
        start_time = time.perf_counter()
        count = 0
        nodes_checked = 0

        for perm in itertools.permutations(range(self.n)):
            nodes_checked += 1
            if self._is_valid_diagonal(perm):
                count += 1

        elapsed = time.perf_counter() - start_time
        stats = {
            "n": self.n,
            "mode": "counting",
            "algorithm": "Brute Force",
            "nodes_checked": nodes_checked,
            "time_seconds": elapsed,
            "total_solutions": count
        }
        return count, stats

    def solve_enumeration(self) -> Tuple[List[List[int]], Dict[str, Any]]:
        """
        Mencari dan mencatat semua solusi valid (Enumeration).
        """
        start_time = time.perf_counter()
        solutions: List[List[int]] = []
        nodes_checked = 0

        for perm in itertools.permutations(range(self.n)):
            nodes_checked += 1
            if self._is_valid_diagonal(perm):
                solutions.append(list(perm))

        elapsed = time.perf_counter() - start_time
        stats = {
            "n": self.n,
            "mode": "enumeration",
            "algorithm": "Brute Force",
            "nodes_checked": nodes_checked,
            "time_seconds": elapsed,
            "total_solutions": len(solutions)
        }
        return solutions, stats
