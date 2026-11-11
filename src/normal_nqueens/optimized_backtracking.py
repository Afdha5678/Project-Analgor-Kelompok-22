"""
Implementasi Optimized Backtracking untuk Normal N-Queens Problem.
Sesuai dengan slide perkuliahan Analisis Algoritme (Complete Search & Backtracking).
Menggunakan tabel lookup boolean untuk kolom dan dua diagonal sehingga validitas O(1).
"""

import time
from typing import List, Optional, Tuple, Dict, Any


class OptimizedBacktrackingNQueens:
    r"""
    Optimized Backtracking dengan Lookup Array O(1) untuk kolom dan dua diagonal.
    - col[c]: apakah kolom c sudah ditempati ratu
    - d1[r + c]: diagonal utama (/)
    - d2[r - c + n - 1]: diagonal sekunder (\)
    
    Kompleksitas Ruang: O(N)
    Pengecekan Keamanan: O(1)
    """

    def __init__(self, n: int):
        if n < 1:
            raise ValueError("Ukuran papan N harus >= 1")
        self.n = n

    def solve_decision(self) -> Tuple[Optional[List[int]], Dict[str, Any]]:
        """Mencari 1 solusi pertama (Decision)."""
        start_time = time.perf_counter()
        n = self.n
        pos = [-1] * n
        col = [False] * n
        d1 = [False] * (2 * n - 1)
        d2 = [False] * (2 * n - 1)
        nodes_explored = 0
        pruned_branches = 0
        solution: Optional[List[int]] = None

        def dfs(r: int) -> bool:
            nonlocal nodes_explored, pruned_branches, solution
            nodes_explored += 1
            if r == n:
                solution = pos.copy()
                return True

            for c in range(n):
                a = r + c
                b = r - c + n - 1
                if col[c] or d1[a] or d2[b]:
                    pruned_branches += 1
                    continue

                pos[r] = c
                col[c] = d1[a] = d2[b] = True

                if dfs(r + 1):
                    return True

                pos[r] = -1
                col[c] = d1[a] = d2[b] = False

            return False

        dfs(0)
        elapsed = time.perf_counter() - start_time
        stats = {
            "n": self.n,
            "mode": "decision",
            "algorithm": "Optimized Backtracking (Lookup Array O(1))",
            "nodes_explored": nodes_explored,
            "pruned_branches": pruned_branches,
            "time_seconds": elapsed,
            "found": solution is not None
        }
        return solution, stats

    def solve_counting(self) -> Tuple[int, Dict[str, Any]]:
        """Menghitung total solusi (Counting)."""
        start_time = time.perf_counter()
        n = self.n
        pos = [-1] * n
        col = [False] * n
        d1 = [False] * (2 * n - 1)
        d2 = [False] * (2 * n - 1)
        nodes_explored = 0
        pruned_branches = 0
        count = 0

        def dfs(r: int):
            nonlocal nodes_explored, pruned_branches, count
            nodes_explored += 1
            if r == n:
                count += 1
                return

            for c in range(n):
                a = r + c
                b = r - c + n - 1
                if col[c] or d1[a] or d2[b]:
                    pruned_branches += 1
                    continue

                pos[r] = c
                col[c] = d1[a] = d2[b] = True

                dfs(r + 1)

                pos[r] = -1
                col[c] = d1[a] = d2[b] = False

        dfs(0)
        elapsed = time.perf_counter() - start_time
        stats = {
            "n": self.n,
            "mode": "counting",
            "algorithm": "Optimized Backtracking (Lookup Array O(1))",
            "nodes_explored": nodes_explored,
            "pruned_branches": pruned_branches,
            "time_seconds": elapsed,
            "total_solutions": count
        }
        return count, stats

    def solve_enumeration(self) -> Tuple[List[List[int]], Dict[str, Any]]:
        """Mencari semua solusi valid (Enumeration)."""
        start_time = time.perf_counter()
        n = self.n
        pos = [-1] * n
        col = [False] * n
        d1 = [False] * (2 * n - 1)
        d2 = [False] * (2 * n - 1)
        nodes_explored = 0
        pruned_branches = 0
        solutions: List[List[int]] = []

        def dfs(r: int):
            nonlocal nodes_explored, pruned_branches
            nodes_explored += 1
            if r == n:
                solutions.append(pos.copy())
                return

            for c in range(n):
                a = r + c
                b = r - c + n - 1
                if col[c] or d1[a] or d2[b]:
                    pruned_branches += 1
                    continue

                pos[r] = c
                col[c] = d1[a] = d2[b] = True

                dfs(r + 1)

                pos[r] = -1
                col[c] = d1[a] = d2[b] = False

        dfs(0)
        elapsed = time.perf_counter() - start_time
        stats = {
            "n": self.n,
            "mode": "enumeration",
            "algorithm": "Optimized Backtracking (Lookup Array O(1))",
            "nodes_explored": nodes_explored,
            "pruned_branches": pruned_branches,
            "time_seconds": elapsed,
            "total_solutions": len(solutions)
        }
        return solutions, stats
