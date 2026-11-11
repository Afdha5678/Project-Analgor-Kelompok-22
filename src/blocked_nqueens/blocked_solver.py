"""
Solver Backtracking & Optimasi untuk Blocked N-Queens Problem.
Mendukung:
- Pencarian Keputusan (Decision: Tempatkan K ratu)
- Pencarian Pencacahan (Counting: Hitung jumlah konfigurasi K ratu)
- Pencarian Penomoran (Enumeration: Daftar seluruh konfigurasi K ratu)
- Pencarian Nilai Papan (Board Value / Maximum Queens Optimization)
"""

import time
from typing import List, Tuple, Optional, Dict, Any, Set
from .blocked_board import BlockedBoard


class BlockedNQueensSolver:
    """
    Solver untuk Blocked N-Queens dengan pemangkasan cabang (Backtracking & Branch-and-Bound).
    """

    def __init__(self, board: BlockedBoard):
        self.board = board
        self.available_cells = self.board.get_available_queen_cells()

    def solve_decision(self, k: int) -> Tuple[Optional[List[Tuple[int, int]]], Dict[str, Any]]:
        """
        Mencari 1 konfigurasi penempatan K ratu yang tidak saling menyerang.
        """
        start_time = time.perf_counter()
        cells = self.available_cells
        total_cells = len(cells)
        solution: Optional[List[Tuple[int, int]]] = None
        nodes_explored = 0

        if k > total_cells:
            elapsed = time.perf_counter() - start_time
            return None, {"found": False, "k": k, "nodes_explored": 0, "time_seconds": elapsed}

        queens: List[Tuple[int, int]] = []

        def dfs(idx: int, placed: int) -> bool:
            nonlocal nodes_explored, solution
            nodes_explored += 1

            if placed == k:
                solution = queens.copy()
                return True

            # Pruning bound: jika sisa petak tidak mencukupi untuk mencapai k
            if placed + (total_cells - idx) < k:
                return False

            for i in range(idx, total_cells):
                r, c = cells[i]
                if self.board.is_safe_placement(r, c, queens):
                    queens.append((r, c))
                    if dfs(i + 1, placed + 1):
                        return True
                    queens.pop()

            return False

        dfs(0, 0)
        elapsed = time.perf_counter() - start_time
        stats = {
            "mode": "decision",
            "k": k,
            "walls_count": self.board.num_walls,
            "nodes_explored": nodes_explored,
            "time_seconds": elapsed,
            "found": solution is not None
        }
        return solution, stats

    def solve_counting(self, k: int) -> Tuple[int, Dict[str, Any]]:
        """
        Menghitung total konfigurasi penempatan K ratu.
        """
        start_time = time.perf_counter()
        cells = self.available_cells
        total_cells = len(cells)
        count = 0
        nodes_explored = 0

        if k > total_cells:
            elapsed = time.perf_counter() - start_time
            return 0, {"k": k, "total_solutions": 0, "nodes_explored": 0, "time_seconds": elapsed}

        queens: List[Tuple[int, int]] = []

        def dfs(idx: int, placed: int):
            nonlocal nodes_explored, count
            nodes_explored += 1

            if placed == k:
                count += 1
                return

            if placed + (total_cells - idx) < k:
                return

            for i in range(idx, total_cells):
                r, c = cells[i]
                if self.board.is_safe_placement(r, c, queens):
                    queens.append((r, c))
                    dfs(i + 1, placed + 1)
                    queens.pop()

        dfs(0, 0)
        elapsed = time.perf_counter() - start_time
        stats = {
            "mode": "counting",
            "k": k,
            "walls_count": self.board.num_walls,
            "nodes_explored": nodes_explored,
            "time_seconds": elapsed,
            "total_solutions": count
        }
        return count, stats

    def solve_enumeration(self, k: int) -> Tuple[List[List[Tuple[int, int]]], Dict[str, Any]]:
        """
        Mencari dan mendaftar semua konfigurasi penempatan K ratu.
        """
        start_time = time.perf_counter()
        cells = self.available_cells
        total_cells = len(cells)
        solutions: List[List[Tuple[int, int]]] = []
        nodes_explored = 0

        if k > total_cells:
            elapsed = time.perf_counter() - start_time
            return [], {"k": k, "total_solutions": 0, "nodes_explored": 0, "time_seconds": elapsed}

        queens: List[Tuple[int, int]] = []

        def dfs(idx: int, placed: int):
            nonlocal nodes_explored
            nodes_explored += 1

            if placed == k:
                solutions.append(queens.copy())
                return

            if placed + (total_cells - idx) < k:
                return

            for i in range(idx, total_cells):
                r, c = cells[i]
                if self.board.is_safe_placement(r, c, queens):
                    queens.append((r, c))
                    dfs(i + 1, placed + 1)
                    queens.pop()

        dfs(0, 0)
        elapsed = time.perf_counter() - start_time
        stats = {
            "mode": "enumeration",
            "k": k,
            "walls_count": self.board.num_walls,
            "nodes_explored": nodes_explored,
            "time_seconds": elapsed,
            "total_solutions": len(solutions)
        }
        return solutions, stats

    def find_board_value(self) -> Tuple[int, List[Tuple[int, int]], Dict[str, Any]]:
        """
        Menghitung Nilai Papan (Board Value) sesuai riset Gabriel Gimenez Franz:
        Jumlah ratu maksimum yang dapat dimuat pada papan dengan rintangan ini.
        Menggunakan algoritma Branch-and-Bound dengan batas atas (Upper Bound Pruning).
        """
        start_time = time.perf_counter()
        cells = self.available_cells
        total_cells = len(cells)
        best_queens: List[Tuple[int, int]] = []
        current_queens: List[Tuple[int, int]] = []
        nodes_explored = 0

        def dfs(idx: int):
            nonlocal best_queens, nodes_explored
            nodes_explored += 1

            if len(current_queens) > len(best_queens):
                best_queens = current_queens.copy()

            # Pruning bound: jika total ratu saat ini + sisa petak <= rekor terbaik, pangkas!
            if len(current_queens) + (total_cells - idx) <= len(best_queens):
                return

            for i in range(idx, total_cells):
                # Pangkas lagi di dalam loop
                if len(current_queens) + (total_cells - i) <= len(best_queens):
                    break

                r, c = cells[i]
                if self.board.is_safe_placement(r, c, current_queens):
                    current_queens.append((r, c))
                    dfs(i + 1)
                    current_queens.pop()

        dfs(0)
        elapsed = time.perf_counter() - start_time
        board_value = len(best_queens)
        stats = {
            "mode": "board_value_optimization",
            "board_value": board_value,
            "walls_count": self.board.num_walls,
            "nodes_explored": nodes_explored,
            "time_seconds": elapsed,
            "optimal_placement": best_queens
        }
        return board_value, best_queens, stats
