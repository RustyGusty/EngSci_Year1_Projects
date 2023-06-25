#%%
from samoku import *
import os


location = os.path.dirname(__file__)

ans = []

with open(os.path.join(location, "output.txt"), "r") as f:
    for line in f:
        ans.append(line[:-1])

with open(os.path.join(location, "cases.txt"), "r") as f:
    success_count = 0
    for count, line in enumerate(f):
        params, _board = line.split(",")
        _board = _board[:-1]

        colo, length = params[0], int(params[1])

        board = make_empty_board(8)

        for i in range(64):
            board[i//8][i%8] = _board[i]

        # Testing cases
        res = str(detect_rows(board, colo, length))
        if res == ans[count]:
            print(f"TEST {count} PASSED")
            success_count += 1
        else:
            print(f"\nTEST {count} FAILED")
            print(f"Expected: {ans[count]}\nYour Output: {res}:")
            print(f"Function tested: detect_rows(board, {colo}, {length})\nBoard:")
            print_board(board)
            print()

        # Uncomment if writing to output file
        '''
        with open(os.path.join(location, "output.txt"), "a") as o:
            o.write(f"{detect_rows(board, colo, length)}\n")
        '''
    print(f"SUCCESS COUNT: {success_count}")

# %%
