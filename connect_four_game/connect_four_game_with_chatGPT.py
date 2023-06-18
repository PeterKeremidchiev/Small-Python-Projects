from collections import deque
import operator
from colorama import Fore
import openai
import random
openai.api_key = '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'

def generate_chat_response(user_input):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=user_input,
        max_tokens=50,
        temperature=0.7,
        n=1,
        stop=None,
        timeout=10,
    )

    return str(random.choice(range(1, 7)))

def print_board():
    [print(f"[ {', '.join(row)} ]") for row in board]

def placed_circle():
    row = 0

    while row != ROWS and board[row][player_col] == "0":
        row += 1
    board[row - 1][player_col] = player_sign
    return row - 1

def get_circles_count(row, col, dx, dy, operator_func):
    current_count = 0

    for i in range(1, 4):
        new_row = operator_func(row, dx * i)
        new_col = operator_func(col, dy * i)

        if not (0 <= new_row < ROWS and 0 <= new_col < COlUMNS):
            break

        if board[new_row][new_col] != player_sign:
            break
        current_count += 1
    return current_count

def check_for_win(row, col):
    for x, y in directions:
        count_sym = get_circles_count(row, col, x, y, operator.add) + get_circles_count(row, col, x, y, operator.sub) + 1

        if count_sym >= 4:
            return True

    if counter_for_draw == ROWS * COlUMNS:
        print_board()
        print("Draw!")
        raise SystemExit

    return False

ROWS, COlUMNS = 6, 7

counter_for_draw = 0

board = [["0"] * COlUMNS for row in range(ROWS)]

player_one_sign = Fore.RED + "P1" + Fore.RESET
player_two_sign = Fore.BLUE + "P2" + Fore.RESET

turns = deque([[1, player_one_sign], [2, player_two_sign]])

win = False

directions = (
    (-1, 0),
    (0, -1),
    (-1, -1),
    (-1, 1),
)
while not win:
    print_board()

    player_number, player_sign = turns[0]

    try:
        if player_number == 1:
            player_col = int(input("Player 1, please choose a column: ")) - 1
        else:
            print("Player 2, please choose a column: ")
            player2_input = generate_chat_response(" ".join(str(x) for x in board))
            player_col = int(player2_input) - 1
    except ValueError:
        print(Fore.RED + f"Please select a valid number in range (1-{COlUMNS})" + Fore.RESET)
        continue
    if not 0 <= player_col < COlUMNS:
        print(Fore.RED + f"Please select a valid number in range (1-{COlUMNS})" + Fore.RESET)
        continue
    if board[0][player_col] != "0":
        print(Fore.RED + "No empty spaces on that row. Choose another column: " + Fore.RESET)
        continue

    row = placed_circle()
    counter_for_draw += 1
    win = check_for_win(row, player_col)

    turns.rotate()

if win:
    print_board()
print(f"Player {turns[1][0]} wins!")