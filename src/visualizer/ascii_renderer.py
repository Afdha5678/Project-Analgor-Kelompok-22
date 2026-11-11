"""
ASCII Renderer untuk terminal: Normal N-Queens, Custom Board, dan Blocked N-Queens.
Dilengkapi penomoran baris/kolom dan opsi warna ANSI.
"""

from typing import List, Tuple, Optional, Set
from ..custom_board.board_shapes import CustomBoard
from ..blocked_nqueens.blocked_board import BlockedBoard

# ANSI Colors
COLOR_RESET = "\033[0m"
COLOR_QUEEN = "\033[1;33m"   # Kuning terang
COLOR_WALL = "\033[1;31m"    # Merah terang
COLOR_EMPTY = "\033[0;37m"   # Abu-abu
COLOR_INACTIVE = "\033[0;90m"# Gelap
COLOR_HEADER = "\033[1;36m"  # Cyan


def render_normal_ascii(pos: List[int], use_color: bool = True) -> str:
    """
    Merender papan N-Queens standar.
    pos[r] = kolom ratu pada baris r.
    """
    n = len(pos)
    lines = []
    
    # Header kolom
    col_hdr = "    " + " ".join(f"{c:2d}" for c in range(n))
    if use_color:
        col_hdr = COLOR_HEADER + col_hdr + COLOR_RESET
    lines.append(col_hdr)
    lines.append("   +" + "--" * n + "-+")

    for r in range(n):
        row_str = f"{r:2d} | "
        if use_color:
            row_str = COLOR_HEADER + f"{r:2d}" + COLOR_RESET + " | "
        
        for c in range(n):
            if pos[r] == c:
                token = "Q "
                if use_color:
                    token = COLOR_QUEEN + "Q " + COLOR_RESET
            else:
                token = ". "
                if use_color:
                    token = COLOR_EMPTY + ". " + COLOR_RESET
            row_str += token
        row_str += "|"
        lines.append(row_str)

    lines.append("   +" + "--" * n + "-+")
    return "\n".join(lines)


def render_custom_ascii(board: CustomBoard, queens: List[Tuple[int, int]], use_color: bool = True) -> str:
    """
    Merender papan kustom (dengan sel yang mungkin tidak aktif/berlubang).
    """
    rows = board.rows
    cols = board.cols
    queen_set = set(queens)
    lines = []

    col_hdr = "    " + " ".join(f"{c:2d}" for c in range(cols))
    if use_color:
        col_hdr = COLOR_HEADER + col_hdr + COLOR_RESET
    lines.append(col_hdr)
    lines.append("   +" + "--" * cols + "-+")

    for r in range(rows):
        row_str = f"{r:2d} | "
        if use_color:
            row_str = COLOR_HEADER + f"{r:2d}" + COLOR_RESET + " | "

        for c in range(cols):
            if not board.is_valid_cell(r, c):
                token = "  "
            elif (r, c) in queen_set:
                token = "Q "
                if use_color:
                    token = COLOR_QUEEN + "Q " + COLOR_RESET
            else:
                token = ". "
                if use_color:
                    token = COLOR_EMPTY + ". " + COLOR_RESET
            row_str += token
        row_str += "|"
        lines.append(row_str)

    lines.append("   +" + "--" * cols + "-+")
    return "\n".join(lines)


def render_blocked_ascii(board: BlockedBoard, queens: List[Tuple[int, int]], use_color: bool = True) -> str:
    """
    Merender papan Blocked N-Queens dengan tembok (#) dan ratu (Q).
    """
    rows = board.rows
    cols = board.cols
    queen_set = set(queens)
    lines = []

    col_hdr = "    " + " ".join(f"{c:2d}" for c in range(cols))
    if use_color:
        col_hdr = COLOR_HEADER + col_hdr + COLOR_RESET
    lines.append(col_hdr)
    lines.append("   +" + "--" * cols + "-+")

    for r in range(rows):
        row_str = f"{r:2d} | "
        if use_color:
            row_str = COLOR_HEADER + f"{r:2d}" + COLOR_RESET + " | "

        for c in range(cols):
            if board.is_wall(r, c):
                token = "# "
                if use_color:
                    token = COLOR_WALL + "# " + COLOR_RESET
            elif (r, c) in queen_set:
                token = "Q "
                if use_color:
                    token = COLOR_QUEEN + "Q " + COLOR_RESET
            else:
                token = ". "
                if use_color:
                    token = COLOR_EMPTY + ". " + COLOR_RESET
            row_str += token
        row_str += "|"
        lines.append(row_str)

    lines.append("   +" + "--" * cols + "-+")
    legend = "   Legend: "
    if use_color:
        legend += f"{COLOR_QUEEN}Q{COLOR_RESET} = Queen, {COLOR_WALL}#{COLOR_RESET} = Wall/Block, {COLOR_EMPTY}.{COLOR_RESET} = Empty tile"
    else:
        legend += "Q = Queen, # = Wall/Block, . = Empty tile"
    lines.append(legend)
    return "\n".join(lines)
