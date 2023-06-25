from gomoku import *
import os


location = os.path.dirname(__file__)

ans = []

with open(os.path.join(location, "output3-1.txt"), "r") as f:
    for line in f:
        ans.append(line[:-1])


with open(os.path.join(location, "cases3-1.txt"), "r") as f:
    for count, line in enumerate(f):
        _, _board = line.split(",")
        _board = _board[:-1]

        board = make_empty_board(8)

        for i in range(64):
            board[i//8][i%8] = _board[i]

        # Testing cases
        res = is_win(board)

        if res in ans[count]:
            print(f"TEST {count} PASSED")
        else:
            print(f"\nTEST {count} FAILED")
            print(f"Expected: {ans[count]}\nYour Output: {res}")
            print("Board:")
            print_board(board)
            print()
