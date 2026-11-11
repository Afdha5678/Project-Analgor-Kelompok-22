"""
Representasi Papan Blocked N-Queens dengan Rintangan / Tembok Pembatas.
Garis pandang ratu (horizontal, vertikal, diagonal) terhalang oleh tembok.
"""

from typing import List, Tuple, Set, Optional


class BlockedBoard:
    """
    Papan Catur berukuran N x N (atau M x N) dengan sekumpulan rintangan/tembok (walls/pawns).
    
    Aturan Inti Blocked N-Queens:
    1. Ratu tidak boleh diletakkan di atas petak tembok.
    2. Dua ratu dalam satu baris, kolom, atau diagonal TIDAK saling menyerang
       jika dan hanya jika terdapat minimal satu tembok di antara keduanya
       sepanjang garis pandang tersebut.
    """

    def __init__(self, n: int, m: Optional[int] = None, walls: Optional[List[Tuple[int, int]]] = None):
        if n < 1:
            raise ValueError("Dimensi N harus >= 1")
        self.rows = n
        self.cols = m if m is not None else n
        self.walls: Set[Tuple[int, int]] = set()

        if walls:
            for r, c in walls:
                self.add_wall(r, c)

    def add_wall(self, r: int, c: int):
        """Menambahkan tembok di koordinat (r, c)."""
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            raise ValueError(f"Koordinat tembok ({r}, {c}) di luar papan {self.rows}x{self.cols}")
        self.walls.add((r, c))

    def remove_wall(self, r: int, c: int):
        """Menghapus tembok di koordinat (r, c)."""
        self.walls.discard((r, c))

    def is_wall(self, r: int, c: int) -> bool:
        """Memeriksa apakah petak (r, c) adalah tembok."""
        return (r, c) in self.walls

    def is_valid_queen_cell(self, r: int, c: int) -> bool:
        """Petak valid untuk ratu: dalam batas papan dan bukan tembok."""
        return 0 <= r < self.rows and 0 <= c < self.cols and (r, c) not in self.walls

    def can_see(self, r1: int, c1: int, r2: int, c2: int) -> bool:
        """
        Memeriksa apakah dua petak saling melihat (saling menyerang).
        Mengembalikan True jika satu garis (baris/kolom/diagonal) dan TIDAK ada tembok di antaranya.
        """
        if r1 == r2 and c1 == c2:
            return True

        dr = r2 - r1
        dc = c2 - c1

        # Cek apakah kolinear (satu baris, kolom, atau diagonal)
        is_row = (dr == 0 and dc != 0)
        is_col = (dr != 0 and dc == 0)
        is_diag = (abs(dr) == abs(dc) and dr != 0)

        if not (is_row or is_col or is_diag):
            return False  # Tidak berada di garis pandang serangan

        # Hitung langkah arah satuan (-1, 0, atau 1)
        step_r = 0 if dr == 0 else (1 if dr > 0 else -1)
        step_c = 0 if dc == 0 else (1 if dc > 0 else -1)

        # Telusuri petak-petak di antara (r1, c1) dan (r2, c2)
        curr_r = r1 + step_r
        curr_c = c1 + step_c
        while (curr_r, curr_c) != (r2, c2):
            if (curr_r, curr_c) in self.walls:
                return False  # Penglihatan terhalang tembok! Tidak saling menyerang.
            curr_r += step_r
            curr_c += step_c

        return True  # Garis pandang bebas tanpa rintangan (serangan aktif)

    def is_safe_placement(self, r: int, c: int, existing_queens: List[Tuple[int, int]]) -> bool:
        """
        Memeriksa apakah aman meletakkan ratu di (r, c) terhadap ratu-ratu yang sudah ada.
        """
        if not self.is_valid_queen_cell(r, c):
            return False

        for qr, qc in existing_queens:
            if self.can_see(r, c, qr, qc):
                return False

        return True

    def get_available_queen_cells(self) -> List[Tuple[int, int]]:
        """Mengembalikan seluruh petak yang bukan tembok."""
        cells = []
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) not in self.walls:
                    cells.append((r, c))
        return cells

    @property
    def num_walls(self) -> int:
        return len(self.walls)
