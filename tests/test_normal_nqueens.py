"""
Unit tests untuk implementasi Normal N-Queens Problem.
Menguji kebenaran solusi berdasarkan barisan referensi OEIS A000170:
N=1: 1
N=2: 0
N=3: 0
N=4: 2
N=5: 10
N=6: 4
N=7: 40
N=8: 92
"""

import unittest
from src.normal_nqueens.brute_force import BruteForceNQueens
from src.normal_nqueens.standard_backtracking import StandardBacktrackingNQueens
from src.normal_nqueens.optimized_backtracking import OptimizedBacktrackingNQueens
from src.normal_nqueens.bitwise_solver import BitwiseNQueens


class TestNormalNQueens(unittest.TestCase):

    KNOWN_SOLUTIONS = {
        1: 1,
        2: 0,
        3: 0,
        4: 2,
        5: 10,
        6: 4,
        7: 40,
        8: 92
    }

    def _verify_validity(self, n: int, pos: list):
        self.assertEqual(len(pos), n)
        self.assertEqual(len(set(pos)), n)
        for i in range(n):
            for j in range(i + 1, n):
                self.assertNotEqual(abs(i - j), abs(pos[i] - pos[j]))

    def test_brute_force_counting(self):
        for n in [1, 2, 3, 4, 5, 6]:
            solver = BruteForceNQueens(n)
            count, _ = solver.solve_counting()
            self.assertEqual(count, self.KNOWN_SOLUTIONS[n])

    def test_standard_backtracking_counting(self):
        for n in [1, 2, 3, 4, 5, 6, 7, 8]:
            solver = StandardBacktrackingNQueens(n)
            count, _ = solver.solve_counting()
            self.assertEqual(count, self.KNOWN_SOLUTIONS[n])

    def test_optimized_backtracking_counting(self):
        for n in [1, 2, 3, 4, 5, 6, 7, 8]:
            solver = OptimizedBacktrackingNQueens(n)
            count, _ = solver.solve_counting()
            self.assertEqual(count, self.KNOWN_SOLUTIONS[n])

    def test_bitwise_counting(self):
        for n in [1, 2, 3, 4, 5, 6, 7, 8]:
            solver = BitwiseNQueens(n)
            count, _ = solver.solve_counting()
            self.assertEqual(count, self.KNOWN_SOLUTIONS[n])

    def test_decision_solutions_are_safe(self):
        for n in [4, 5, 6, 7, 8]:
            solver = OptimizedBacktrackingNQueens(n)
            sol, stats = solver.solve_decision()
            self.assertIsNotNone(sol)
            self._verify_validity(n, sol)

    def test_no_solution_for_2_and_3(self):
        for n in [2, 3]:
            solver = OptimizedBacktrackingNQueens(n)
            sol, _ = solver.solve_decision()
            self.assertIsNone(sol)


if __name__ == "__main__":
    unittest.main()
