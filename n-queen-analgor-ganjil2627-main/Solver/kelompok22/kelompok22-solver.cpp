// Solver Kelompok 22 - Paralel 2 Analisis Algoritme IPB University
// Anggota Kelompok:
// 1. Afdha Auliya Atiq (M0403241163)
// 2. Muhammad Andhika Putra Pratama (M0403241055)
// 3. Azra Aslam Khoiri (M0403241148)
//
// Implementasi: Optimized Backtracking dengan O(1) Constraint Propagation & Snapshot Support
#include <algorithm>
#include <string>
#include <utility>
#include <vector>

#include "nqueens.h"

namespace {

// ============================================================================
// 1. NORMAL N-QUEENS (Optimized Backtracking O(1) Lookups)
// ============================================================================
void solveNormalBacktracking(int r, int n, std::vector<int>& current_cols,
                             std::vector<bool>& col_used,
                             std::vector<bool>& diag1_used,
                             std::vector<bool>& diag2_used,
                             std::vector<std::vector<int>>& solutions) {
  if (r == n) {
    solutions.push_back(current_cols);
    NQ_SNAPSHOT(nq::queensOf(current_cols), "Solution found: #" + std::to_string(solutions.size()));
    return;
  }

  for (int c = 0; c < n; ++c) {
    int d1 = r - c + n - 1;
    int d2 = r + c;
    if (!col_used[c] && !diag1_used[d1] && !diag2_used[d2]) {
      col_used[c] = diag1_used[d1] = diag2_used[d2] = true;
      current_cols[r] = c;

      solveNormalBacktracking(r + 1, n, current_cols, col_used, diag1_used, diag2_used, solutions);

      col_used[c] = diag1_used[d1] = diag2_used[d2] = false;
      current_cols[r] = -1;
    }
  }
}

// ============================================================================
// 2. PRE-PLACED N-QUEENS
// ============================================================================
void solvePreplacedBacktracking(int r, int n,
                                const std::vector<int>& pre_col,
                                std::vector<int>& current_cols,
                                std::vector<bool>& col_used,
                                std::vector<bool>& diag1_used,
                                std::vector<bool>& diag2_used,
                                std::vector<std::vector<int>>& solutions) {
  if (r == n) {
    solutions.push_back(current_cols);
    NQ_SNAPSHOT(nq::queensOf(current_cols), "Preplaced solution #" + std::to_string(solutions.size()));
    return;
  }

  if (pre_col[r] != -1) {
    int c = pre_col[r];
    int d1 = r - c + n - 1;
    int d2 = r + c;
    if (col_used[c] || diag1_used[d1] || diag2_used[d2]) {
      return; // Preplaced conflict
    }
    col_used[c] = diag1_used[d1] = diag2_used[d2] = true;
    current_cols[r] = c;

    solvePreplacedBacktracking(r + 1, n, pre_col, current_cols, col_used, diag1_used, diag2_used, solutions);

    col_used[c] = diag1_used[d1] = diag2_used[d2] = false;
    current_cols[r] = -1;
  } else {
    for (int c = 0; c < n; ++c) {
      int d1 = r - c + n - 1;
      int d2 = r + c;
      if (!col_used[c] && !diag1_used[d1] && !diag2_used[d2]) {
        col_used[c] = diag1_used[d1] = diag2_used[d2] = true;
        current_cols[r] = c;

        solvePreplacedBacktracking(r + 1, n, pre_col, current_cols, col_used, diag1_used, diag2_used, solutions);

        col_used[c] = diag1_used[d1] = diag2_used[d2] = false;
        current_cols[r] = -1;
      }
    }
  }
}

// ============================================================================
// 3. HOLES N-QUEENS (Attacks pass through holes, queens cannot sit on holes)
// ============================================================================
void solveHolesBacktracking(int r, int n,
                            const std::vector<std::string>& grid,
                            std::vector<int>& current_cols,
                            std::vector<bool>& col_used,
                            std::vector<bool>& diag1_used,
                            std::vector<bool>& diag2_used,
                            std::vector<std::vector<int>>& solutions) {
  if (r == n) {
    solutions.push_back(current_cols);
    NQ_SNAPSHOT(nq::queensOf(current_cols), "Holes solution #" + std::to_string(solutions.size()));
    return;
  }

  for (int c = 0; c < n; ++c) {
    if (grid[r][c] == 'H') continue; // cannot place queen on a hole

    int d1 = r - c + n - 1;
    int d2 = r + c;
    if (!col_used[c] && !diag1_used[d1] && !diag2_used[d2]) {
      col_used[c] = diag1_used[d1] = diag2_used[d2] = true;
      current_cols[r] = c;

      solveHolesBacktracking(r + 1, n, grid, current_cols, col_used, diag1_used, diag2_used, solutions);

      col_used[c] = diag1_used[d1] = diag2_used[d2] = false;
      current_cols[r] = -1;
    }
  }
}

// ============================================================================
// 4. WALLED N-QUEENS (Walls block attacks! Maximize total queens)
// ============================================================================
bool canPlaceWalled(int r, int c, int n, const std::vector<std::string>& grid,
                    const std::vector<std::pair<int, int>>& queens) {
  if (grid[r][c] == 'W') return false;

  for (const auto& q : queens) {
    int qr = q.first;
    int qc = q.second;

    // Check same row
    if (qr == r) {
      int step = (qc > c) ? 1 : -1;
      bool blocked = false;
      for (int k = c + step; k != qc; k += step) {
        if (grid[r][k] == 'W') { blocked = true; break; }
      }
      if (!blocked) return false;
    }
    // Check same col
    else if (qc == c) {
      int step = (qr > r) ? 1 : -1;
      bool blocked = false;
      for (int k = r + step; k != qr; k += step) {
        if (grid[k][c] == 'W') { blocked = true; break; }
      }
      if (!blocked) return false;
    }
    // Check main diagonal
    else if (qr - qc == r - c) {
      int rstep = (qr > r) ? 1 : -1;
      int cstep = (qc > c) ? 1 : -1;
      bool blocked = false;
      for (int kr = r + rstep, kc = c + cstep; kr != qr; kr += rstep, kc += cstep) {
        if (grid[kr][kc] == 'W') { blocked = true; break; }
      }
      if (!blocked) return false;
    }
    // Check anti diagonal
    else if (qr + qc == r + c) {
      int rstep = (qr > r) ? 1 : -1;
      int cstep = (qc > c) ? 1 : -1;
      bool blocked = false;
      for (int kr = r + rstep, kc = c + cstep; kr != qr; kr += rstep, kc += cstep) {
        if (grid[kr][kc] == 'W') { blocked = true; break; }
      }
      if (!blocked) return false;
    }
  }
  return true;
}

void solveWalledSearch(int cell_idx, int n, const std::vector<std::string>& grid,
                       std::vector<std::pair<int, int>>& current_queens,
                       int& max_queens,
                       std::vector<std::vector<std::pair<int, int>>>& best_boards) {
  int total_cells = n * n;
  int remaining_cells = total_cells - cell_idx;
  if ((int)current_queens.size() + remaining_cells < max_queens) {
    return; // Pruning bound
  }

  if (cell_idx == total_cells) {
    int q_count = static_cast<int>(current_queens.size());
    if (q_count > max_queens) {
      max_queens = q_count;
      best_boards.clear();
      best_boards.push_back(current_queens);
      NQ_SNAPSHOT(current_queens, "New Max Queens: " + std::to_string(max_queens));
    } else if (q_count == max_queens && max_queens > 0) {
      best_boards.push_back(current_queens);
    }
    return;
  }

  int r = cell_idx / n;
  int c = cell_idx % n;

  // Try placing queen if valid
  if (canPlaceWalled(r, c, n, grid, current_queens)) {
    current_queens.emplace_back(r, c);
    solveWalledSearch(cell_idx + 1, n, grid, current_queens, max_queens, best_boards);
    current_queens.pop_back();
  }

  // Try skipping this cell
  solveWalledSearch(cell_idx + 1, n, grid, current_queens, max_queens, best_boards);
}

} // namespace

// ---- Solvers Export ---------------------------------------------------------
std::vector<std::vector<int>> solveNQueens(int n) {
  std::vector<std::vector<int>> solutions;
  std::vector<int> current_cols(n, -1);
  std::vector<bool> col_used(n, false);
  std::vector<bool> diag1_used(2 * n - 1, false);
  std::vector<bool> diag2_used(2 * n - 1, false);

  solveNormalBacktracking(0, n, current_cols, col_used, diag1_used, diag2_used, solutions);
  return solutions;
}

std::vector<std::vector<int>> solvePreplaced(int n, const std::vector<std::pair<int, int>>& preplaced) {
  std::vector<std::vector<int>> solutions;
  std::vector<int> pre_col(n, -1);
  std::vector<bool> col_used(n, false);
  std::vector<bool> diag1_used(2 * n - 1, false);
  std::vector<bool> diag2_used(2 * n - 1, false);

  // Validate preplaced positions
  for (const auto& p : preplaced) {
    int r = p.first;
    int c = p.second;
    if (r < 0 || r >= n || c < 0 || c >= n) return {};
    if (pre_col[r] != -1 && pre_col[r] != c) return {};
    int d1 = r - c + n - 1;
    int d2 = r + c;
    if (col_used[c] || diag1_used[d1] || diag2_used[d2]) return {};
    pre_col[r] = c;
    col_used[c] = diag1_used[d1] = diag2_used[d2] = true;
  }

  // Reset masks for backtracking loop
  std::fill(col_used.begin(), col_used.end(), false);
  std::fill(diag1_used.begin(), diag1_used.end(), false);
  std::fill(diag2_used.begin(), diag2_used.end(), false);

  std::vector<int> current_cols(n, -1);
  solvePreplacedBacktracking(0, n, pre_col, current_cols, col_used, diag1_used, diag2_used, solutions);
  return solutions;
}

std::vector<std::vector<int>> solveHoles(int n, const std::vector<std::string>& grid) {
  std::vector<std::vector<int>> solutions;
  std::vector<int> current_cols(n, -1);
  std::vector<bool> col_used(n, false);
  std::vector<bool> diag1_used(2 * n - 1, false);
  std::vector<bool> diag2_used(2 * n - 1, false);

  solveHolesBacktracking(0, n, grid, current_cols, col_used, diag1_used, diag2_used, solutions);
  return solutions;
}

std::vector<std::vector<std::pair<int, int>>> solveWalled(int n, const std::vector<std::string>& grid) {
  std::vector<std::vector<std::pair<int, int>>> best_boards;
  std::vector<std::pair<int, int>> current_queens;
  int max_queens = 0;

  solveWalledSearch(0, n, grid, current_queens, max_queens, best_boards);
  return best_boards;
}
