"""
Definisi representasi geometri dan topologi papan catur kustom.
Mendukung:
- Papan Persegi Panjang (M x N)
- Papan Masking Tak Beraturan (Arbitrary Masked / Irregular Shape)
- Papan Toroidal (Wrap-around Diagonals)
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Set, Optional


class CustomBoard(ABC):
    """Kelas dasar abstrak untuk representasi papan kustom."""

    @property
    @abstractmethod
    def rows(self) -> int:
        pass

    @property
    @abstractmethod
    def cols(self) -> int:
        pass

    @abstractmethod
    def is_valid_cell(self, r: int, c: int) -> bool:
        """Memeriksa apakah koordinat (r, c) merupakan petak aktif dalam papan."""
        pass

    @abstractmethod
    def attack(self, r1: int, c1: int, r2: int, c2: int) -> bool:
        """Memeriksa apakah ratu di (r1, c1) menyerang ratu di (r2, c2)."""
        pass

    @abstractmethod
    def get_valid_cells(self) -> List[Tuple[int, int]]:
        """Mengembalikan daftar seluruh petak aktif pada papan."""
        pass


class RectangularBoard(CustomBoard):
    """
    Papan Catur Persegi Panjang berukuran M x N.
    """

    def __init__(self, m: int, n: int, k_queens: Optional[int] = None):
        if m < 1 or n < 1:
            raise ValueError("Dimensi baris dan kolom harus >= 1")
        self._rows = m
        self._cols = n
        self.k_queens = k_queens if k_queens is not None else min(m, n)

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def cols(self) -> int:
        return self._cols

    def is_valid_cell(self, r: int, c: int) -> bool:
        return 0 <= r < self._rows and 0 <= c < self._cols

    def attack(self, r1: int, c1: int, r2: int, c2: int) -> bool:
        return (r1 == r2) or (c1 == c2) or (abs(r1 - r2) == abs(c1 - c2))

    def get_valid_cells(self) -> List[Tuple[int, int]]:
        return [(r, c) for r in range(self._rows) for c in range(self._cols)]


class MaskedBoard(CustomBoard):
    """
    Papan Catur Bebas / Tak Beraturan berbasis Mask Boolean.
    Hanya petak dengan mask == True yang dapat ditempati ratu.
    """

    def __init__(self, mask: List[List[bool]], name: str = "Masked Board", k_queens: Optional[int] = None):
        if not mask or not mask[0]:
            raise ValueError("Mask papan tidak boleh kosong")
        self._rows = len(mask)
        self._cols = len(mask[0])
        self.mask = mask
        self.name = name
        self._valid_cells = [
            (r, c) for r in range(self._rows) for c in range(self._cols) if mask[r][c]
        ]
        self.k_queens = k_queens if k_queens is not None else min(self._rows, self._cols)

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def cols(self) -> int:
        return self._cols

    def is_valid_cell(self, r: int, c: int) -> bool:
        if 0 <= r < self._rows and 0 <= c < self._cols:
            return self.mask[r][c]
        return False

    def attack(self, r1: int, c1: int, r2: int, c2: int) -> bool:
        return (r1 == r2) or (c1 == c2) or (abs(r1 - r2) == abs(c1 - c2))

    def get_valid_cells(self) -> List[Tuple[int, int]]:
        return self._valid_cells


class ToroidalBoard(CustomBoard):
    """
    Papan Catur Toroidal (N x N) dengan Teorema George Polya.
    Petak-petak di batas sisi papan melipat / wrap-around ke sisi seberang.
    Diagonal diperiksa secara modular:
    - (r1 - c1) % N == (r2 - c2) % N
    - (r1 + c1) % N == (r2 + c2) % N
    
    Teorema Polya (1918): Solusi ada jika dan hanya jika gcd(N, 6) == 1.
    """

    def __init__(self, n: int):
        if n < 1:
            raise ValueError("Ukuran papan N harus >= 1")
        self.n = n

    @property
    def rows(self) -> int:
        return self.n

    @property
    def cols(self) -> int:
        return self.n

    def is_valid_cell(self, r: int, c: int) -> bool:
        return 0 <= r < self.n and 0 <= c < self.n

    def attack(self, r1: int, c1: int, r2: int, c2: int) -> bool:
        if r1 == r2 or c1 == c2:
            return True
        # Wrap-around diagonals mod N
        d1_mod = (r1 - c1) % self.n == (r2 - c2) % self.n
        d2_mod = (r1 + c1) % self.n == (r2 + c2) % self.n
        return d1_mod or d2_mod

    def get_valid_cells(self) -> List[Tuple[int, int]]:
        return [(r, c) for r in range(self.n) for c in range(self.n)]


# =====================================================================
# Preset Geometri Bidang Kustom Populer
# =====================================================================

def create_diamond_board(radius: int, k_queens: Optional[int] = None) -> MaskedBoard:
    """
    Membuat papan berbentuk Belah Ketupat / Diamond.
    Ukuran grid: (2*radius + 1) x (2*radius + 1).
    Kondisi sel aktif: |r - radius| + |c - radius| <= radius.
    """
    dim = 2 * radius + 1
    mask = [[False] * dim for _ in range(dim)]
    for r in range(dim):
        for c in range(dim):
            if abs(r - radius) + abs(c - radius) <= radius:
                mask[r][c] = True
    return MaskedBoard(mask, name=f"Diamond Board (radius={radius})", k_queens=k_queens)


def create_circle_board(radius: int, k_queens: Optional[int] = None) -> MaskedBoard:
    """
    Membuat papan berbentuk Lingkaran.
    Kondisi sel aktif: (r - radius)^2 + (c - radius)^2 <= radius^2.
    """
    dim = 2 * radius + 1
    mask = [[False] * dim for _ in range(dim)]
    for r in range(dim):
        for c in range(dim):
            if (r - radius) ** 2 + (c - radius) ** 2 <= radius ** 2:
                mask[r][c] = True
    return MaskedBoard(mask, name=f"Circular Board (radius={radius})", k_queens=k_queens)


def create_triangle_board(height: int, k_queens: Optional[int] = None) -> MaskedBoard:
    """
    Membuat papan berbentuk Tangga / Segitiga Siku-siku (Triangular / Staircase).
    Pada baris r, kolom yang valid adalah 0 <= c <= r.
    """
    mask = [[False] * height for _ in range(height)]
    for r in range(height):
        for c in range(r + 1):
            mask[r][c] = True
    return MaskedBoard(mask, name=f"Triangular Board (height={height})", k_queens=k_queens)


def create_cross_board(arm_length: int, center_width: int, k_queens: Optional[int] = None) -> MaskedBoard:
    """
    Membuat papan berbentuk Palang / Cross / Plus.
    """
    dim = 2 * arm_length + center_width
    mask = [[False] * dim for _ in range(dim)]
    center_start = arm_length
    center_end = arm_length + center_width

    for r in range(dim):
        for c in range(dim):
            in_horizontal_bar = center_start <= r < center_end
            in_vertical_bar = center_start <= c < center_end
            if in_horizontal_bar or in_vertical_bar:
                mask[r][c] = True
    return MaskedBoard(mask, name=f"Cross Board (arm={arm_length}, width={center_width})", k_queens=k_queens)


def create_hole_board(n: int, hole_r: int, hole_c: int, hole_h: int, hole_w: int, k_queens: Optional[int] = None) -> MaskedBoard:
    """
    Membuat papan normal berukuran N x N dengan area lubang yang dipotong di tengah.
    """
    mask = [[True] * n for _ in range(n)]
    for r in range(hole_r, min(n, hole_r + hole_h)):
        for c in range(hole_c, min(n, hole_c + hole_w)):
            mask[r][c] = False
    return MaskedBoard(mask, name=f"Hole Board (N={n}, hole={hole_w}x{hole_h})", k_queens=k_queens)


def board_from_ascii(ascii_art: str, name: str = "Custom ASCII Board", k_queens: Optional[int] = None) -> MaskedBoard:
    """
    Membuat papan dari representasi string ASCII.
    '.' atau 'O' atau '1' = Petak aktif
    ' ' atau 'X' atau '0' atau '#' = Petak kosong / tidak ada papan
    """
    import textwrap
    cleaned = textwrap.dedent(ascii_art).strip()
    lines = [line.rstrip() for line in cleaned.split("\n") if line.strip()]
    rows = len(lines)
    cols = max(len(line) for line in lines)
    mask = [[False] * cols for _ in range(rows)]
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char in ".O1o*":
                mask[r][c] = True
    return MaskedBoard(mask, name=name, k_queens=k_queens)
