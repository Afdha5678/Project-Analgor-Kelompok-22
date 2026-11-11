"""
Unit tests untuk Blocked N-Queens Problem.
"""

import unittest
from src.blocked_nqueens.blocked_board import BlockedBoard
from src.blocked_nqueens.blocked_solver import BlockedNQueensSolver
from src.blocked_nqueens.puzzle_presets import get_preset_board


class TestBlockedNQueens(unittest.TestCase):

    def test_line_of_sight_blocking(self):
        # Buat papan 5x5
        board = BlockedBoard(5)
        # Tanpa tembok, (0, 0) dan (0, 4) saling serang
        self.assertTrue(board.can_see(0, 0, 0, 4))

        # Tambahkan tembok di antara keduanya pada (0, 2)
        board.add_wall(0, 2)
        # Sekarang penglihatan terhalang tembok!
        self.assertFalse(board.can_see(0, 0, 0, 4))

        # Tetapi diagonal (0, 0) ke (4, 4) masih saling serang
        self.assertTrue(board.can_see(0, 0, 4, 4))
        # Halangi diagonal dengan tembok di (2, 2)
        board.add_wall(2, 2)
        self.assertFalse(board.can_see(0, 0, 4, 4))

    def test_classic_0w_board(self):
        # 0-W Board harus menghasilkan 92 solusi untuk K=8
        board = get_preset_board("0-W_classic")
        solver = BlockedNQueensSolver(board)
        count, _ = solver.solve_counting(8)
        self.assertEqual(count, 92)

    def test_high_value_board_allows_9_queens(self):
        # High value board memungkinkan meletakkan 9 ratu pada papan 8x8!
        board = get_preset_board("high_value_9_queens")
        solver = BlockedNQueensSolver(board)
        sol, stats = solver.solve_decision(9)
        self.assertIsNotNone(sol)
        self.assertEqual(len(sol), 9)

        # Verifikasi bahwa tidak ada dua ratu yang saling melihat
        for i in range(len(sol)):
            for j in range(i + 1, len(sol)):
                r1, c1 = sol[i]
                r2, c2 = sol[j]
                self.assertFalse(board.can_see(r1, c1, r2, c2))

    def test_board_value_optimization(self):
        board = BlockedBoard(4, walls=[(1, 1), (2, 2)])
        solver = BlockedNQueensSolver(board)
        val, best, _ = solver.find_board_value()
        self.assertGreaterEqual(val, 4)


if __name__ == "__main__":
    unittest.main()
