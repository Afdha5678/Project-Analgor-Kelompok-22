"""
Unit tests untuk Custom Board N-Queens Problem.
"""

import unittest
from src.custom_board.board_shapes import (
    RectangularBoard,
    MaskedBoard,
    ToroidalBoard,
    create_diamond_board,
    create_circle_board,
    create_triangle_board,
    board_from_ascii
)
from src.custom_board.custom_solver import CustomBoardSolver


class TestCustomBoard(unittest.TestCase):

    def test_rectangular_board(self):
        # Papan 4 x 5, letakkan 4 ratu
        board = RectangularBoard(4, 5, k_queens=4)
        solver = CustomBoardSolver(board)
        sol, stats = solver.solve_decision(4)
        self.assertIsNotNone(sol)
        self.assertEqual(len(sol), 4)

        # Pastikan tidak saling serang
        for i in range(4):
            for j in range(i + 1, 4):
                self.assertFalse(board.attack(sol[i][0], sol[i][1], sol[j][0], sol[j][1]))

    def test_toroidal_polya_theorem(self):
        """
        Teorema Polya: Solusi ada jika dan hanya jika gcd(N, 6) == 1.
        Untuk N = 4, 6, 8, 9, 10, 12 -> 0 solusi!
        Untuk N = 5, 7, 11 -> ada solusi (> 0)!
        """
        # N = 4 (gcd(4, 6) = 2 != 1) -> 0 solusi
        board4 = ToroidalBoard(4)
        solver4 = CustomBoardSolver(board4)
        count4, _ = solver4.solve_counting(4)
        self.assertEqual(count4, 0)

        # N = 5 (gcd(5, 6) = 1) -> ada solusi (tepatnya 10 solusi)
        board5 = ToroidalBoard(5)
        solver5 = CustomBoardSolver(board5)
        count5, _ = solver5.solve_counting(5)
        self.assertEqual(count5, 10)

        # N = 7 (gcd(7, 6) = 1) -> ada solusi
        board7 = ToroidalBoard(7)
        solver7 = CustomBoardSolver(board7)
        sol7, _ = solver7.solve_decision(7)
        self.assertIsNotNone(sol7)

    def test_diamond_board(self):
        board = create_diamond_board(radius=2)
        solver = CustomBoardSolver(board)
        max_q, best, _ = solver.find_max_queens()
        self.assertGreaterEqual(max_q, 3)

    def test_ascii_board_creation(self):
        art = """
        . . . .
        . . . .
        . . . .
        """
        board = board_from_ascii(art)
        self.assertEqual(board.rows, 3)
        self.assertEqual(board.cols, 7)  # spasi dihitung


if __name__ == "__main__":
    unittest.main()
