"""
Implementasi Bitwise Backtracking untuk Normal N-Queens Problem.
Menggunakan manipulasi bit integer (bitwise operations) untuk efisiensi puncak.
"""

import time
from typing import List, Optional, Tuple, Dict, Any


class BitwiseNQueens:
    """
    Solver N-Queens berbasis Bitwise DFS.
    Menyimpan bitmask:
    - cols: kolom yang telah diserang
    - diags1: diagonal utama yang telah diserang (digeser ke kiri tiap level)
    - diags2: diagonal sekunder yang telah diserang (digeser ke kanan tiap level)
    
    Operasi penentuan slot aman:
    available = (~(cols | diags1 | diags2)) & ((1 << n) - 1)
    Pengambilan bit paling bawah (lowest set bit):
    bit = available & -available
    """

    def __init__(self, n: int):
        if n < 1:
            raise ValueError("Ukuran papan N harus >= 1")
        if n > 31:
            raise ValueError("Bitwise solver dirancang efisien hingga N <= 31")
        self.n = n
        self.all_ones = (1 << n) - 1

    def solve_counting(self) -> Tuple[int, Dict[str, Any]]:
        """
        Menghitung total solusi dengan kecepatan bitwise maksimal.
        """
        start_time = time.perf_counter()
        n = self.n
        all_ones = self.all_ones
        count = 0
        recursive_calls = 0

        def dfs(cols: int, d1: int, d2: int):
            nonlocal count, recursive_calls
            recursive_calls += 1
            if cols == all_ones:
                count += 1
                return

            available = (~(cols | d1 | d2)) & all_ones
            while available:
                bit = available & -available
                available -= bit
                dfs(cols | bit, (d1 | bit) << 1, (d2 | bit) >> 1)

        dfs(0, 0, 0)
        elapsed = time.perf_counter() - start_time
        stats = {
            "n": self.n,
            "mode": "counting",
            "algorithm": "Bitwise Backtracking",
            "recursive_calls": recursive_calls,
            "time_seconds": elapsed,
            "total_solutions": count
        }
        return count, stats

    def solve_decision(self) -> Tuple[Optional[List[int]], Dict[str, Any]]:
        """
        Menemukan 1 solusi pertama dengan merekonstruksi posisi papan.
        """
        start_time = time.perf_counter()
        n = self.n
        all_ones = self.all_ones
        pos = [-1] * n
        solution: Optional[List[int]] = None
        recursive_calls = 0

        def dfs(r: int, cols: int, d1: int, d2: int) -> bool:
            nonlocal recursive_calls, solution
            recursive_calls += 1
            if r == n:
                solution = pos.copy()
                return True

            available = (~(cols | d1 | d2)) & all_ones
            while available:
                bit = available & -available
                available -= bit
                c = bit.bit_length() - 1
                pos[r] = c
                if dfs(r + 1, cols | bit, (d1 | bit) << 1, (d2 | bit) >> 1):
                    return True
                pos[r] = -1
            return False

        dfs(0, 0, 0, 0)
        elapsed = time.perf_counter() - start_time
        stats = {
            "n": self.n,
            "mode": "decision",
            "algorithm": "Bitwise Backtracking",
            "recursive_calls": recursive_calls,
            "time_seconds": elapsed,
            "found": solution is not None
        }
        return solution, stats

    def solve_enumeration(self) -> Tuple[List[List[int]], Dict[str, Any]]:
        """
        Menemukan seluruh konfigurasi solusi dengan pelacakan posisi.
        """
        start_time = time.perf_counter()
        n = self.n
        all_ones = self.all_ones
        pos = [-1] * n
        solutions: List[List[int]] = []
        recursive_calls = 0

        def dfs(r: int, cols: int, d1: int, d2: int):
            nonlocal recursive_calls
            recursive_calls += 1
            if r == n:
                solutions.append(pos.copy())
                return

            available = (~(cols | d1 | d2)) & all_ones
            while available:
                bit = available & -available
                available -= bit
                c = bit.bit_length() - 1
                pos[r] = c
                dfs(r + 1, cols | bit, (d1 | bit) << 1, (d2 | bit) >> 1)
                pos[r] = -1

        dfs(0, 0, 0, 0)
        elapsed = time.perf_counter() - start_time
        stats = {
            "n": self.n,
            "mode": "enumeration",
            "algorithm": "Bitwise Backtracking",
            "recursive_calls": recursive_calls,
            "time_seconds": elapsed,
            "total_solutions": len(solutions)
        }
        return solutions, stats
