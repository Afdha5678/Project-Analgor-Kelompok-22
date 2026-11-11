"""
Kumpulan konfigurasi papan Blocked N-Queens preset dan generator acak.
Berdasarkan katalog dan variasi eksperimental Gabriel Gimenez Franz.
"""

import random
from typing import Dict, List, Tuple, Any, Optional
from .blocked_board import BlockedBoard


PRESETS: Dict[str, Dict[str, Any]] = {
    "0-W_classic": {
        "n": 8,
        "name": "0-W Board (Papan Catur Standar 8x8)",
        "description": "Papan tanpa rintangan. Nilai papan = 8 dengan 92 solusi optimal.",
        "walls": []
    },
    "1-W_corner": {
        "n": 8,
        "name": "1-W Corner Wall Board",
        "description": "1 Tembok pada sudut papan (0, 0).",
        "walls": [(0, 0)]
    },
    "1-W_center": {
        "n": 8,
        "name": "1-W Center Wall Board",
        "description": "1 Tembok pada pusat papan (3, 3).",
        "walls": [(3, 3)]
    },
    "2-W_diagonal": {
        "n": 8,
        "name": "2-W Diagonal Split",
        "description": "2 Tembok pada diagonal utama (2, 2) dan (5, 5).",
        "walls": [(2, 2), (5, 5)]
    },
    "3-W_gabriel": {
        "n": 8,
        "name": "3-W Asymmetric Board",
        "description": "3 Tembok asimetris pada (1, 2), (4, 4), dan (6, 1).",
        "walls": [(1, 2), (4, 4), (6, 1)]
    },
    "4-W_symmetrical": {
        "n": 8,
        "name": "4-W Symmetrical Fortress",
        "description": "4 Tembok simetris kuadran (2, 2), (2, 5), (5, 2), (5, 5).",
        "walls": [(2, 2), (2, 5), (5, 2), (5, 5)]
    },
    "high_value_9_queens": {
        "n": 8,
        "name": "High-Value Board (Mampu Menampung 9 Ratu)",
        "description": "Tembok strategis yang membagi baris dan kolom sehingga memungkinkan 9 ratu non-attacking.",
        "walls": [(1, 3), (3, 1), (4, 6), (6, 4)]
    },
    "high_value_10_queens": {
        "n": 8,
        "name": "High-Value Board (Mampu Menampung 10 Ratu)",
        "description": "Tembok ganda strategis yang memblokir garis pandang antar petak.",
        "walls": [(0, 3), (1, 4), (3, 0), (4, 1), (6, 3), (7, 4), (3, 7), (4, 6)]
    }
}


def get_preset_board(preset_key: str) -> BlockedBoard:
    """Mengambil papan preset berdasarkan kunci."""
    if preset_key not in PRESETS:
        raise KeyError(f"Preset '{preset_key}' tidak ditemukan. Pilihan: {list(PRESETS.keys())}")
    data = PRESETS[preset_key]
    return BlockedBoard(n=data["n"], walls=data["walls"])


def list_presets() -> List[Dict[str, Any]]:
    """Mendaftar semua preset yang tersedia."""
    result = []
    for k, v in PRESETS.items():
        result.append({
            "key": k,
            "name": v["name"],
            "description": v["description"],
            "n": v["n"],
            "walls_count": len(v["walls"])
        })
    return result


def create_random_blocked_board(n: int = 8, num_walls: int = 4, seed: Optional[int] = None) -> BlockedBoard:
    """Membangkitkan papan terblokir secara acak dengan jumlah tembok tertentu."""
    if seed is not None:
        random.seed(seed)
    all_coords = [(r, c) for r in range(n) for c in range(n)]
    num_walls = min(num_walls, n * n - 1)
    chosen_walls = random.sample(all_coords, num_walls)
    return BlockedBoard(n=n, walls=chosen_walls)
