from __future__ import annotations

from battleship.game.constants import BOARD_SIZE, COLS, SHIP, WATER


def create_board() -> list[list[str]]:
    board: list[list[str]] = []
    for _ in range(BOARD_SIZE):
        row: list[str] = []
        for _ in range(BOARD_SIZE):
            row.append(WATER)
        board.append(row)
    return board


def render_board(board: list[list[str]], show_ships: bool = True) -> None:
    print("    " + " ".join(COLS))
    for r in range(BOARD_SIZE):
        print(f"{r + 1:2} |", end=" ")
        for c in range(BOARD_SIZE):
            cell = board[r][c]
            if not show_ships and cell == SHIP:
                cell = WATER
            print(cell, end=" ")
        print()


def has_ships_left(board: list[list[str]]) -> bool:
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == SHIP:
                return True
    return False

