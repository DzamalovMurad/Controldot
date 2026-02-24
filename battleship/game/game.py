from __future__ import annotations

import os

from battleship.game.board import create_board, has_ships_left, render_board
from battleship.game.ships import random_place_fleet
from battleship.game.shots import apply_shot, ask_shot


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def header(player: int) -> None:
    print("=" * 24)
    print(f"      ХОД ИГРОКА {player}")
    print("=" * 24)
    print()


def switch_player(current: int) -> int:
    return 2 if current == 1 else 1


def select_boards(
    b1: list[list[str]], b2: list[list[str]], current: int
) -> tuple[list[list[str]], list[list[str]]]:
    if current == 1:
        return b1, b2
    return b2, b1


def render_turn(my_board: list[list[str]], enemy_board: list[list[str]]) -> None:
    print("Ваше поле:")
    render_board(my_board, show_ships=True)
    print()
    print("Поле соперника:")
    render_board(enemy_board, show_ships=False)
    print()


def check_win(enemy_board: list[list[str]], player: int) -> bool:
    if not has_ships_left(enemy_board):
        print(f"Игрок {player} победил! Все корабли соперника уничтожены.")
        return True
    return False


def pause(msg: str = "Нажмите Enter, чтобы продолжить...") -> None:
    try:
        input(msg)
    except (EOFError, KeyboardInterrupt):
        print()
        raise SystemExit("Ввод прерван. Игра завершена.")


def play_game() -> None:
    b1 = create_board()
    b2 = create_board()
    random_place_fleet(b1)
    random_place_fleet(b2)

    current = 1

    while True:
        clear_screen()
        my_board, enemy_board = select_boards(b1, b2, current)
        header(current)
        render_turn(my_board, enemy_board)

        shot = ask_shot()
        result = apply_shot(enemy_board, shot)

        if result == "repeat":
            print("Вы уже стреляли в эту клетку. Попробуйте снова.")
            pause()
            continue

        if result == "miss":
            print("Промах!")
            pause("Нажмите Enter и передайте ход другому игроку...")
            current = switch_player(current)
            continue

        # hit
        print("Попадание!")
        if check_win(enemy_board, current):
            break
        pause()

