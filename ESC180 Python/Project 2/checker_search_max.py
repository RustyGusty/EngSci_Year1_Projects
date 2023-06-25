from gomoku import *
import os
import ast


location = os.path.dirname(__file__)

ans = []

with open(os.path.join(location, "output2.txt"), "r") as f:
    for line in f:
        ans.append(ast.literal_eval(line[:-1]))


with open(os.path.join(location, "cases.txt"), "r") as f:
    for count, line in enumerate(f):
        _, _board = line.split(",")
        _board = _board[:-1]

        board = make_empty_board(8)

        for i in range(64):
            board[i//8][i%8] = _board[i]

        # Testing cases
        res = search_max(board)

        if res in ans[count]:
            print(f"TEST {count} PASSED")
        else:
            print(f"\nTEST {count} FAILED")
            print(f"Maximize score locations: {ans[count]}")
            print(f"Your Output: {res}:")
            print_board(board)
            print()

        # Uncomment if writing to output file
        # with open(os.path.join(location, "output2.txt"), "a") as o:
        #     o.write(f"{search_max2(board)}\n")
