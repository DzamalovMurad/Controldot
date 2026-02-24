from __future__ import annotations

import random

from battleship.game.constants import BOARD_SIZE, FLEET, SHIP, WATER


def _ship_cells(
    start: tuple[int, int], length: int, horizontal: bool
) -> list[tuple[int, int]]:
    row, col = start
    if horizontal:
        return [(row, col + i) for i in range(length)]
    return [(row + i, col) for i in range(length)]


def _can_place(board: list[list[str]], cells: list[tuple[int, int]]) -> bool:
    for row, col in cells:
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return False
        if board[row][col] != WATER:
            return False

        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = row + dr, col + dc
                if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                    if board[nr][nc] != WATER:
                        return False

    return True


def random_place_fleet(board: list[list[str]]) -> None:
    while True:
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                board[r][c] = WATER

        ok = True
        for size in FLEET:
            placed = False
            for _ in range(300):
                horizontal = random.choice([True, False])
                start_row = random.randrange(BOARD_SIZE)
                start_col = random.randrange(BOARD_SIZE)
                cells = _ship_cells((start_row, start_col), size, horizontal)

                if _can_place(board, cells):
                    for rr, cc in cells:
                        board[rr][cc] = SHIP
                    placed = True
                    break

            if not placed:
                ok = False
                break

        if ok:
            break

