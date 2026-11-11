"""
Implementasi Standard Backtracking untuk Normal N-Queens Problem.
Pengecekan keamanan posisi ratu dilakukan dengan iterasi baris sebelumnya O(r).
"""

import time
from typing import List, Optional, Tuple, Dict, Any


class StandardBacktrackingNQueens:
    """
    Standard Backtracking dengan pemangkasan cabang (pruning).
    Pemeriksaan konflik kolom dan diagonal dilakukan secara iteratif terhadap
    ratu-ratu yang telah diletakkan pada baris 0 s.d. r-1 (O(N) per langkah).
    """

    def __init__(self, n: int):
        if n < 1:
            raise ValueError("Ukuran papan N harus >= 1")
        self.n = n

    def _is_safe(self, pos: List[int], r: int, c: int) -> bool:
        """
        Memeriksa apakah aman menaruh ratu di baris r, kolom c.
        Memeriksa semua ratu di baris 0..r-1.
        """
        for i in range(r):
            # Cek kolom yang sama atau diagonal yang sama
            if pos[i] == c or abs(i - r) == abs(pos[i] - c):
                return False
        return True

    def solve_decision(self) -> Tuple[Optional[List[int]], Dict[str, Any]]:
        """Mencari 1 solusi pertama."""
        start_time = time.perf_counter()
        pos = [-1] * self.n
        nodes_explored = 0
        solution: Optional[List[int]] = None

        def dfs(r: int) -> bool:
            nonlocal nodes_explored, solution
            nodes_explored += 1
            if r == self.n:
                solution = pos.copy()
                return True

            for c in range(self.n):
                if self._is_safe(pos, r, c):
                    pos[r] = c
                    if dfs(r + 1):
                        return True
                    pos[r] = -1
            return False

        dfs(0)
        elapsed = time.perf_counter() - start_time
        stats = {
            "n": self.n,
            "mode": "decision",
            "algorithm": "Standard Backtracking (O(N) check)",
            "nodes_explored": nodes_explored,
            "time_seconds": elapsed,
            "found": solution is not None
        }
        return solution, stats

    def solve_counting(self) -> Tuple[int, Dict[str, Any]]:
        """Menghitung total solusi."""
        start_time = time.perf_counter()
        pos = [-1] * self.n
        nodes_explored = 0
        count = 0

        def dfs(r: int):
            nonlocal nodes_explored, count
            nodes_explored += 1
            if r == self.n:
                count += 1
                return

            for c in range(self.n):
                if self._is_safe(pos, r, c):
                    pos[r] = c
                    dfs(r + 1)
                    pos[r] = -1

        dfs(0)
        elapsed = time.perf_counter() - start_time
        stats = {
            "n": self.n,
            "mode": "counting",
            "algorithm": "Standard Backtracking (O(N) check)",
            "nodes_explored": nodes_explored,
            "time_seconds": elapsed,
            "total_solutions": count
        }
        return count, stats

    def solve_enumeration(self) -> Tuple[List[List[int]], Dict[str, Any]]:
        """Mencari seluruh konfigurasi solusi."""
        start_time = time.perf_counter()
        pos = [-1] * self.n
        nodes_explored = 0
        solutions: List[List[int]] = []

        def dfs(r: int):
            nonlocal nodes_explored
            nodes_explored += 1
            if r == self.n:
                solutions.append(pos.copy())
                return

            for c in range(self.n):
                if self._is_safe(pos, r, c):
                    pos[r] = c
                    dfs(r + 1)
                    pos[r] = -1

        dfs(0)
        elapsed = time.perf_counter() - start_time
        stats = {
            "n": self.n,
            "mode": "enumeration",
            "algorithm": "Standard Backtracking (O(N) check)",
            "nodes_explored": nodes_explored,
            "time_seconds": elapsed,
            "total_solutions": len(solutions)
        }
        return solutions, stats
