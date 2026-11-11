"""
Solver Backtracking untuk Custom Board N-Queens.
Mendukung pencarian Decision, Counting, Enumeration, dan Optimasi Max-Queens.
"""

import time
from typing import List, Tuple, Optional, Dict, Any, Set
from .board_shapes import CustomBoard, ToroidalBoard, RectangularBoard, MaskedBoard


class CustomBoardSolver:
    """
    Algoritma Backtracking dengan pruning untuk papan bergeometri kustom.
    """

    def __init__(self, board: CustomBoard):
        self.board = board
        self.rows = board.rows
        self.cols = board.cols

    def _get_active_columns_by_row(self) -> List[List[int]]:
        """Mengelompokkan kolom aktif per baris."""
        row_cols: List[List[int]] = [[] for _ in range(self.rows)]
        for r, c in self.board.get_valid_cells():
            row_cols[r].append(c)
        return row_cols

    def solve_decision(self, k: Optional[int] = None) -> Tuple[Optional[List[Tuple[int, int]]], Dict[str, Any]]:
        """
        Menemukan 1 penempatan valid untuk K ratu.
        Jika K tidak ditentukan, default menggunakan min(rows, cols) atau k_queens board.
        """
        start_time = time.perf_counter()
        if k is None:
            k = getattr(self.board, "k_queens", min(self.rows, self.cols))

        valid_cells = self.board.get_valid_cells()
        if k > len(valid_cells):
            elapsed = time.perf_counter() - start_time
            return None, {"found": False, "k": k, "time_seconds": elapsed, "reason": "k > valid_cells"}

        # Jika tiap baris maksimal 1 ratu dan k == rows (papan persegi/persegi panjang)
        row_cols = self._get_active_columns_by_row()
        active_rows = [r for r in range(self.rows) if row_cols[r]]

        nodes_explored = 0
        solution: Optional[List[Tuple[int, int]]] = None

        # Strategi baris-ke-baris jika k <= rows
        if k <= len(active_rows):
            queens: List[Tuple[int, int]] = []

            def dfs(row_idx: int, placed: int) -> bool:
                nonlocal nodes_explored, solution
                nodes_explored += 1
                if placed == k:
                    solution = queens.copy()
                    return True

                remaining_rows = len(active_rows) - row_idx
                if placed + remaining_rows < k:
                    return False  # Pruning bound

                r = active_rows[row_idx]
                # Pilihan 1: Coba letakkan ratu di salah satu kolom aktif pada baris r
                for c in row_cols[r]:
                    is_safe = True
                    for qr, qc in queens:
                        if self.board.attack(qr, qc, r, c):
                            is_safe = False
                            break
                    if is_safe:
                        queens.append((r, c))
                        if dfs(row_idx + 1, placed + 1):
                            return True
                        queens.pop()

                # Pilihan 2: Lewati baris r tanpa menaruh ratu (jika k < rows)
                if dfs(row_idx + 1, placed):
                    return True

                return False

            dfs(0, 0)
        else:
            # Penempatan umum cell-by-cell jika k > rows
            queens = []

            def dfs_general(cell_idx: int, placed: int) -> bool:
                nonlocal nodes_explored, solution
                nodes_explored += 1
                if placed == k:
                    solution = queens.copy()
                    return True

                remaining = len(valid_cells) - cell_idx
                if placed + remaining < k:
                    return False

                r, c = valid_cells[cell_idx]
                is_safe = True
                for qr, qc in queens:
                    if self.board.attack(qr, qc, r, c):
                        is_safe = False
                        break

                if is_safe:
                    queens.append((r, c))
                    if dfs_general(cell_idx + 1, placed + 1):
                        return True
                    queens.pop()

                return dfs_general(cell_idx + 1, placed)

            dfs_general(0, 0)

        elapsed = time.perf_counter() - start_time
        stats = {
            "mode": "decision",
            "k": k,
            "nodes_explored": nodes_explored,
            "time_seconds": elapsed,
            "found": solution is not None
        }
        return solution, stats

    def solve_counting(self, k: Optional[int] = None) -> Tuple[int, Dict[str, Any]]:
        """Menghitung total konfigurasi penempatan K ratu."""
        start_time = time.perf_counter()
        if k is None:
            k = getattr(self.board, "k_queens", min(self.rows, self.cols))

        valid_cells = self.board.get_valid_cells()
        if k > len(valid_cells):
            elapsed = time.perf_counter() - start_time
            return 0, {"k": k, "total_solutions": 0, "time_seconds": elapsed}

        row_cols = self._get_active_columns_by_row()
        active_rows = [r for r in range(self.rows) if row_cols[r]]
        count = 0
        nodes_explored = 0

        if k <= len(active_rows):
            queens: List[Tuple[int, int]] = []

            def dfs(row_idx: int, placed: int):
                nonlocal count, nodes_explored
                nodes_explored += 1
                if placed == k:
                    count += 1
                    return

                remaining_rows = len(active_rows) - row_idx
                if placed + remaining_rows < k:
                    return

                r = active_rows[row_idx]
                for c in row_cols[r]:
                    is_safe = True
                    for qr, qc in queens:
                        if self.board.attack(qr, qc, r, c):
                            is_safe = False
                            break
                    if is_safe:
                        queens.append((r, c))
                        dfs(row_idx + 1, placed + 1)
                        queens.pop()

                dfs(row_idx + 1, placed)

            dfs(0, 0)
        else:
            queens = []

            def dfs_general(cell_idx: int, placed: int):
                nonlocal count, nodes_explored
                nodes_explored += 1
                if placed == k:
                    count += 1
                    return

                remaining = len(valid_cells) - cell_idx
                if placed + remaining < k:
                    return

                r, c = valid_cells[cell_idx]
                is_safe = True
                for qr, qc in queens:
                    if self.board.attack(qr, qc, r, c):
                        is_safe = False
                        break

                if is_safe:
                    queens.append((r, c))
                    dfs_general(cell_idx + 1, placed + 1)
                    queens.pop()

                dfs_general(cell_idx + 1, placed)

            dfs_general(0, 0)

        elapsed = time.perf_counter() - start_time
        stats = {
            "mode": "counting",
            "k": k,
            "nodes_explored": nodes_explored,
            "time_seconds": elapsed,
            "total_solutions": count
        }
        return count, stats

    def solve_enumeration(self, k: Optional[int] = None) -> Tuple[List[List[Tuple[int, int]]], Dict[str, Any]]:
        """Mencari semua konfigurasi penempatan K ratu."""
        start_time = time.perf_counter()
        if k is None:
            k = getattr(self.board, "k_queens", min(self.rows, self.cols))

        valid_cells = self.board.get_valid_cells()
        solutions: List[List[Tuple[int, int]]] = []
        if k > len(valid_cells):
            elapsed = time.perf_counter() - start_time
            return [], {"k": k, "total_solutions": 0, "time_seconds": elapsed}

        row_cols = self._get_active_columns_by_row()
        active_rows = [r for r in range(self.rows) if row_cols[r]]
        nodes_explored = 0

        if k <= len(active_rows):
            queens: List[Tuple[int, int]] = []

            def dfs(row_idx: int, placed: int):
                nonlocal nodes_explored
                nodes_explored += 1
                if placed == k:
                    solutions.append(queens.copy())
                    return

                remaining_rows = len(active_rows) - row_idx
                if placed + remaining_rows < k:
                    return

                r = active_rows[row_idx]
                for c in row_cols[r]:
                    is_safe = True
                    for qr, qc in queens:
                        if self.board.attack(qr, qc, r, c):
                            is_safe = False
                            break
                    if is_safe:
                        queens.append((r, c))
                        dfs(row_idx + 1, placed + 1)
                        queens.pop()

                dfs(row_idx + 1, placed)

            dfs(0, 0)
        else:
            queens = []

            def dfs_general(cell_idx: int, placed: int):
                nonlocal nodes_explored
                nodes_explored += 1
                if placed == k:
                    solutions.append(queens.copy())
                    return

                remaining = len(valid_cells) - cell_idx
                if placed + remaining < k:
                    return

                r, c = valid_cells[cell_idx]
                is_safe = True
                for qr, qc in queens:
                    if self.board.attack(qr, qc, r, c):
                        is_safe = False
                        break

                if is_safe:
                    queens.append((r, c))
                    dfs_general(cell_idx + 1, placed + 1)
                    queens.pop()

                dfs_general(cell_idx + 1, placed)

            dfs_general(0, 0)

        elapsed = time.perf_counter() - start_time
        stats = {
            "mode": "enumeration",
            "k": k,
            "nodes_explored": nodes_explored,
            "time_seconds": elapsed,
            "total_solutions": len(solutions)
        }
        return solutions, stats

    def find_max_queens(self) -> Tuple[int, List[Tuple[int, int]], Dict[str, Any]]:
        """
        Mencari jumlah ratu maksimum yang dapat diletakkan (Max-Queens Optimization).
        """
        start_time = time.perf_counter()
        valid_cells = self.board.get_valid_cells()
        best_queens: List[Tuple[int, int]] = []
        current_queens: List[Tuple[int, int]] = []
        nodes_explored = 0

        # Pengurutan heuristik: coba dari baris teratas
        row_cols = self._get_active_columns_by_row()
        active_rows = [r for r in range(self.rows) if row_cols[r]]

        def dfs(row_idx: int):
            nonlocal best_queens, nodes_explored
            nodes_explored += 1

            if len(current_queens) > len(best_queens):
                best_queens = current_queens.copy()

            if row_idx == len(active_rows):
                return

            remaining_rows = len(active_rows) - row_idx
            # Pruning bound: jika kuota maksimal tersisa tidak dapat melampaui best_queens
            if len(current_queens) + remaining_rows <= len(best_queens):
                return

            r = active_rows[row_idx]
            # Coba setiap kolom di baris r
            for c in row_cols[r]:
                is_safe = True
                for qr, qc in current_queens:
                    if self.board.attack(qr, qc, r, c):
                        is_safe = False
                        break
                if is_safe:
                    current_queens.append((r, c))
                    dfs(row_idx + 1)
                    current_queens.pop()

            # Pilihan lewati baris r
            dfs(row_idx + 1)

        dfs(0)
        elapsed = time.perf_counter() - start_time
        stats = {
            "mode": "max_queens_optimization",
            "max_queens": len(best_queens),
            "nodes_explored": nodes_explored,
            "time_seconds": elapsed
        }
        return len(best_queens), best_queens, stats
