"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Oct. 28, 2022
"""

def is_empty(board):
    ''' Return True iff all elements in board are " " '''
    for row in board:
        for e in row:
            if e != " ":
                return False
    return True

def space_valid(y, x, size):
    ''' Returns False if the space defined by (y, x) is off a square board of size size'''
    return not (x < 0 or y < 0 or x >= size or y >= size)

def is_bounded(board, y_end, x_end, length, d_y, d_x):
    ''' Returns "OPEN" if the spaces after and before the sequence specified with x_end and y_end as endpoints of a length long sequence are free, "CLOSED" if neither space is free, and "SEMIOPEN" otherwise '''

    # True iff the space before / after the sequence is free
    before_free = False
    after_free = False

    # y_before and x_before define the space before the start of the seqeuence
    y_before, x_before = y_end - d_y * length, x_end - d_x*length
    # y_after and x_after define the space after the end of the sequence
    y_after, x_after = y_end + d_y, x_end + d_x

    # Check for before being blocked (if space is invalid, indexing will not occur)
    if space_valid(y_before, x_before, len(board)) and board[y_before][x_before] == " ":
        before_free = True

    # Check for after being blocked
    if space_valid(y_after, x_after, len(board)) and board[y_after][x_after] == " ":
        after_free = True

    if after_free and before_free:
        return "OPEN"
    elif not(after_free or before_free):
        return "CLOSED"
    else:
        return "SEMIOPEN"


def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    ''' Given the stone colour col, returns a tuple (open_count, semiopen_count), where open_count is the number of open sequences startng at y_start, x_start and of length l, and semiopen_count is the smae but counting semiopen sequences '''
    open_count, semiopen_count = 0, 0

    y_current = y_start
    x_current = x_start
    current_seq_length = 0
    while space_valid(y_current, x_current, len(board)):
        current_stone = board[y_current][x_current]
        # If stone is the colour col, increment count
        if current_stone == col:
            current_seq_length += 1
        # If stone is not colour col:
        else:
            # Check length
            if current_seq_length == length:
                # Determine state of the current sequence
                run_state = is_bounded(board, y_current - d_y, x_current - d_x, length, d_y, d_x)
                if run_state == "OPEN":
                    open_count += 1
                elif run_state == "SEMIOPEN":
                    semiopen_count += 1
            # Reset run counter
            current_seq_length = 0

        y_current += d_y
        x_current += d_x

    # Perform final check for semiopen sequence (last element is always bounded by the edge of the board)
    if current_seq_length == length:
        run_state = is_bounded(board, y_current - d_y, x_current - d_x, length, d_y, d_x)
        if run_state == "SEMIOPEN":
            semiopen_count += 1

    return (open_count, semiopen_count)

def detect_rows(board, col, length):
    open_count, semiopen_count = 0, 0

    # Iterate through all starting positions and their rows, columns, and diagonals where appropriate
    for i in range(len(board[0])):
        # Column (1, 0) check from (0, i)
        count = detect_row(board, col, 0, i, length, 1, 0)
        open_count += count[0]
        semiopen_count += count[1]

        # Diagonal (1, 1) check from (0, i)
        count = detect_row(board, col, 0, i, length, 1, 1)
        open_count += count[0]
        semiopen_count += count[1]

        # Diagonal (1, -1) check from (0, i)
        count = detect_row(board, col, 0, i, length, 1, -1)
        open_count += count[0]
        semiopen_count += count[1]

        # Row (0, 1) check from (i, 0)
        count = detect_row(board, col, i, 0, length, 0, 1)
        open_count += count[0]
        semiopen_count += count[1]

        if i != 0:
            # Diagonal (1, 1) check from (i, 0) (skipping the (0, 0) starting position to not duplicate with the previous loop
            count = detect_row(board, col, i, 0, length, 1, 1)
            open_count += count[0]
            semiopen_count += count[1]

            # Diagonal (1, -1) check from (i, end) (skipping the (0, end) starting position to not duplicate with the previous loop
            count = detect_row(board, col, i, len(board[0]) - 1, length, 1, -1)
            open_count += count[0]
            semiopen_count += count[1]

    return open_count, semiopen_count

def search_max(board):
    current_max = (-1, -1), float("-inf") # current_max[0] is the coords, current_max[1] is the point value
    # Iterate through all possible placements
    for row_i in range(len(board[0])):
        for col_i in range(len(board)):
            # Only check clear spaces
            if board[row_i][col_i] == " ":
                # Simulate placing a "b" to calculate its score, then immediately remove the "b"
                board[row_i][col_i] = "b"
                curr_score = score(board)
                board[row_i][col_i] = " "
                if curr_score > current_max[1]:
                    current_max = (row_i, col_i), curr_score
    return current_max[0]


def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

def is_win(board):
    ''' Returns the current status of board --> whether one stone has won, it's a draw, or play is to continue '''

    def win_check(board, y_start, x_start, dy, dx):
        ''' Given a starting position y_start, x_start and a direction dy, dx, if a winner exists returns "White won" or "Black Run" or False if no winner exists yet (winner must have 5 stones in a row exactly (no overruns) '''
        w_run, b_run = 0, 0
        y_current = y_start
        x_current = x_start

        while space_valid(y_current, x_current, len(board)):
            current_stone = board[y_current][x_current]
            if current_stone == "w":
                # Check if b_run is exactly 5. If so, then black has won
                if b_run == 5:
                    return "Black won"
                # Reset b_run (even if already 0) and increment w_run
                b_run = 0
                w_run += 1
            elif current_stone == "b":
                if w_run == 5:
                    return "White won"
                w_run = 0
                b_run += 1

            else:
                if w_run == 5:
                    return "White won"
                elif b_run == 5:
                    return "Black won"
                b_run, w_run = 0, 0

            y_current += dy
            x_current += dx
        # Final check for victory for the last sequence in the run
        if w_run == 5:
            return "White won"
        elif b_run == 5:
            return "Black won"

        return False

    # Iterate through all starting positions on the board
    for i in range(len(board[0])):

        # Column (1, 0) check from (0, i)
        current_status = win_check(board, 0, i, 1, 0)
        # False only if a winner has not been declared, and if one has, current_status holds the message to return
        if current_status != False:
            return current_status

        # Diagonal (1, 1) check from (0, i)
        current_status = win_check(board, 0, i, 1, 1)
        if current_status != False:
            return current_status

        # Diagonal (1, -1) check from (0, i)
        current_status = win_check(board, 0, i, 1, -1)
        if current_status != False:
            return current_status

        # Row (0, 1) check from (i, 0)
        current_status = win_check(board, i, 0, 0, 1)
        if current_status != False:
            return current_status

        if i != 0:
            # Diagonal (1, 1) check from (i, 0) (skipping the (0, 0) starting position to not duplicate with the previous loop
            current_status = win_check(board, i, 0, 1, 1)
            if current_status != False:
                return current_status

            # Diagonal (1, -1) check from (i, end) (skipping the (0, end) starting position to not duplicate with the previous loop
            current_status = win_check(board, i, len(board[0]) - 1, 1, -1)
            if current_status != False:
                return current_status

    # If execution reaches here, no winner has been found
    if is_empty(board):
        return "Draw"
    else:
        return "Continue playing"

def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))


def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res





        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x

def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0


def detect_rows_test(board, col, length):
    ''' Given a col, prints the number of semiopen and open runs of length length of that col across the board '''

    def print_count(count, start_index, type):
        ''' Only prints if it was not (0, 0)'''
        if count[0] != 0:
            print(f"{start_index} {type} OPEN: {count[0]}")
        if count[1] != 0:
            print(f"{start_index} {type} semiopen: {count[1]}")

    # Check all columns and diagonals from top row starting position
    for column_i in range(len(board[0])):
        # Column check
        count = detect_row(board, col, 0, column_i, length, 1, 0)
        print_count(count, (0, column_i), "column")

        # Diagonal (1, 1) check
        count = detect_row(board, col, 0, column_i, length, 1, 1)
        print_count(count, (0, column_i), "1,1 diagonal")

        # Diagonal (1, -1) check
        count = detect_row(board, col, 0, column_i, length, 1, -1)
        print_count(count, (0, column_i), "1,-1 diagonal")

    # Check all rows and (1, 1) diagonals from left column starting position, and (1, -1) diagonals from right column starting position
    for row_i in range(len(board)):
        count = detect_row(board, col, row_i, 0, length, 0, 1)
        print_count(count, (row_i, 0), "row")

        if row_i != 0:
            # Diagonal (1, 1) check (skipping the (0, 0) starting position to not duplicate with the previous loop
            count = detect_row(board, col, row_i, 0, length, 1, 1)
            print_count(count, (row_i, 0), "1,1 diagonal")

            # Diagonal (1, -1) check (skipping the (0, end) starting position to not duplicate with the previous loop
            count = detect_row(board, col, row_i, len(board[0]) - 1, length, 1, -1)
            print_count(count, (row_i, len(board[0]) - 1), "1,-1 diagonal")



if __name__ == '__main__':
    #print(play_gomoku(8))

    ## A: Board-checking functions
    board = [["b", " ", " ", "w", " "],
             ["b", "b", " ", "b", " "],
             [" ", "b", " ", "b", "b"],
             ["b", "w", "b", "b", "b"],
             ["b", " ", " ", "b", " "]]
    print_board(board)

    ## A1: is_empty
    print("A1: is_empty test")
    print("Non-empty board: ", is_empty(board))
    print("Empty board:", is_empty(make_empty_board(5)))

    ## A2: detect_row
    print("\nA2: detect_row test")
    for i in range(1, 5):
        print(f"\nLength {i}: ")
        detect_rows_test(board, "b", i)


    ## A3: detect_rows
    print("\nA3: detect_rows test")
    for i in range(1, 5):
        print(f"\nLength {i}: ")
        print(detect_rows(board, "b", i))
    #Expected output:
# Length 1:
# (7, 4)
#
# Length 2:
# (2, 10)
#
# Length 3:
# (0, 0)
#
# Length 4:
# (0, 0)

    ## A4: search_max
    print("\nA4: search_max test")
    # Given the easy situation, should be 2, 2
    print(search_max(board))

    ## A5: is_win
    print("\nA5: is_win test")
    print(is_win(board))
    put_seq_on_board(board, 0, 0, 1, 1, 5, "w")
    print(is_win(board))
    put_seq_on_board(board, 0, 4, 1, -1, 5, "b")
    print(is_win(board))

    ## B: Bigger board tests
    w = "w"
    b = "b"
    s = " "
    board = [[s, s, b, s, b, b, b, s],
             [s, s, b, s, b, b, s, s],
             [b, s, s, s, w, b, s, s],
             [s, w, b, b, b, b, s, w],
             [s, b, b, w, b, s, s, s],
             [s, b, s, s, w, s, s, b],
             [b, s, w, b, w, w, w, s],
             [s, w, w, w, b, w, w, w]]
    print_board(board)

    ## B1: detect_rows test
    print("\nA2: detect_row test")
    print("Black results: ")
    for i in range(1, len(board[0])):
        print(f"\nLength {i}: ")
        detect_rows_test(board, "b", i)
    print("White results: ")
    for i in range(1, len(board[0])):
        print(f"\nLength {i}: ")
        detect_rows_test(board, "w", i)
    # Go to MS paint and check results manually

    ## B2: search_max test
    print("Black's best move:", search_max(board))
    # Unfortunately, black is winning too hard for this to matter much

    ## C1: 6-long check

    board = make_empty_board(10)
    put_seq_on_board(board, 0, 0, 1, 1, 6, "b")
    for i in range(1, 7):
        print(f"\nLength {i}: ")
        print(detect_rows(board, "b", i))
    print(is_win(board))