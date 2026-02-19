from __future__ import annotations

from battleship.game.constants import BOARD_SIZE, HIT, MISS, SHIP, WATER


def parse_shot(text: str) -> tuple[int, int] | None:
    text = text.strip()
    if len(text) < 2:
        return None

    letter = text[0].lower()
    if not ("a" <= letter <= "j"):
        return None

    number_part = text[1:]
    if not number_part.isdigit():
        return None

    col = ord(letter) - ord("a")
    row = int(number_part) - 1

    if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
        return None

    return (row, col)


def ask_shot() -> tuple[int, int]:
    while True:
        try:
            raw = input("Введите координаты выстрела (например, a5): ")
        except (EOFError, KeyboardInterrupt):
            print()
            raise SystemExit("Ввод прерван. Игра завершена.")
        shot = parse_shot(raw)
        if shot is None:
            print("Некорректный ввод. Пример: A5 или j10.")
            continue
        return shot


def apply_shot(board: list[list[str]], shot: tuple[int, int]) -> str:
    r, c = shot
    cell = board[r][c]

    if cell == WATER:
        board[r][c] = MISS
        return "miss"
    if cell == SHIP:
        board[r][c] = HIT
        return "hit"
    return "repeat"

