import math


def initialize():
    global coords_list, opponent_pos, my_pos, my_speed, last_best_angle
    coords_list = [[0, 0], [0, 0], [0, 0]]
    opponent_pos = [0, 0, 0]
    my_pos = [-1, -1]
    my_speed = 1
    last_best_angle = [[0, -1], [0, -1]]


def return_trajectory(paddle_x, paddle_y, paddle_width, paddle_height, other_x, other_y, ball_size, table_size):
    global last_best_angle
    max_angle = math.pi / 4
    target, impact_angle, t_x, velocity = calculate_path(paddle_x, other_x, paddle_width, table_size[1], table_size[0], ball_size)
    board_height = table_size[1]
    board_width = table_size[0]
    x_distance = board_width - 2 * min(paddle_x, other_x) - paddle_width
    # If moving away, set target to the opponent's target location within 1/4 of the height each way
    if t_x > 0:
        last_best_angle = [[0, -1], [0, -1]];

        op_velocity = (opponent_pos[-1] - opponent_pos[0]) / (len(opponent_pos) - 1)


        # If opponent move has been locked in
        if abs(op_velocity) <= 0.5:
            target = calculate_opponent_path(paddle_x, other_x, other_y, table_size, ball_size, target, impact_angle, paddle_height, paddle_width, max_angle)
            if target > board_height / 2:
                return paddle_y > max(board_height / 2, target - board_width / (velocity * 2) * my_speed)
            else:
                return paddle_y > min(board_height / 2, target + board_width / (velocity * 2) * my_speed)

        # If opponent will barely make the target (available time < time needed to get to ball)
        if t_x < paddle_height or t_x < (abs(target - other_y) - paddle_height / 2) / abs(op_velocity) + paddle_height:
            op_max_position = other_y + op_velocity * t_x
            if target > other_y:
                if op_max_position < target - paddle_height / 2 - 5:
                    return paddle_y > board_height / 2
                elif op_max_position < target  - paddle_height / 8:
                    target = calculate_opponent_path(paddle_x, other_x, op_max_position, table_size, ball_size, target, impact_angle, paddle_height, paddle_width, max_angle)
                    return paddle_y > target
            else:
                if op_max_position > target + paddle_height / 2 + 5:
                    return paddle_y > board_height / 2
                elif op_max_position > target + paddle_height / 8:
                    target = calculate_opponent_path(paddle_x, other_x, op_max_position, table_size, ball_size, target, impact_angle, paddle_height, paddle_width, max_angle)
                    return paddle_y > target



        # Otherwise, default to where the ball is going (max deviation of 1/4 of the space each way)

        return paddle_y > board_height / 2

    t_x *= -1

    if abs(impact_angle) > math.pi / 3:
        return paddle_y > target

    if t_x < paddle_height / 1.5:
        if last_best_angle[0][1] > last_best_angle[1][1]:
            return paddle_y > target + last_best_angle[0][0]
        else:
            return paddle_y > target + last_best_angle[1][0]


    best_angle = [[0, -1], [0, -1]]
    good_enough(best_angle, 0, impact_angle, target, paddle_y, other_y, paddle_height, board_height, board_width, t_x, impact_angle, max_angle, ball_size, x_distance)
    # Angle needed to hit the top corner straight
    target_angle = math.atan((board_height - ball_size / 2 - target) / x_distance)
    rel_angle = (target_angle - impact_angle) / 2
    offset = - rel_angle / max_angle * paddle_height
    good_enough(best_angle, offset, target_angle, target, paddle_y, other_y, paddle_height, board_height, board_width, t_x, impact_angle, max_angle, ball_size, x_distance)
    # Angle needed to hit the bottom corner straight
    target_angle = math.atan((ball_size / 2 - target) / x_distance)
    rel_angle = (target_angle - impact_angle) / 2
    offset = - rel_angle / max_angle * paddle_height
    good_enough(best_angle, offset, target_angle, target, paddle_y, other_y, paddle_height, board_height, board_width, t_x, impact_angle, max_angle, ball_size, x_distance)

    # Angle needed to hit top after one bounce on the bottom
    target_angle = math.atan((2 * board_height - 3 * ball_size / 2 - target) / x_distance)
    rel_angle = (target_angle - impact_angle) / 2
    offset = - rel_angle / max_angle * paddle_height
    good_enough(best_angle, offset, target_angle, target, paddle_y, other_y, paddle_height, board_height, board_width, t_x, impact_angle, max_angle, ball_size, x_distance)
    # Angle needed to hit bottom after one bounce on the top
    target_angle = math.atan((-3 * ball_size / 2 - target - board_height) / x_distance)
    rel_angle = (target_angle - impact_angle) / 2
    offset = - rel_angle / max_angle * paddle_height
    good_enough(best_angle, offset, target_angle, target, paddle_y, other_y, paddle_height, board_height, board_width, t_x, impact_angle, max_angle, ball_size, x_distance)

    last_best_angle = best_angle
    if last_best_angle[0][1] < last_best_angle[1][1]:
        return paddle_y > target + last_best_angle[0][0]
    else:
        return paddle_y > target + last_best_angle[1][0]

def good_enough(best_angle, offset, target_angle, target, paddle_y, other_y, paddle_height, board_height, board_width, t_x, impact_angle, max_angle, ball_size, x_distance):
    # Offset is not too big, final position is not below the board, final position is not above the board, and available time is bigger than time needed to move into position

    if abs(offset) <= paddle_height / 2 and target + offset + paddle_height / 2 < board_height and target + offset - paddle_height / 2 > 0 and t_x > (target + offset - paddle_y) / my_speed:
        resulting_target = get_resulting_target(target, target_angle, ball_size, board_width, board_height, x_distance)
        direction = resulting_target > board_height / 2
        if direction and abs(other_y - resulting_target) > best_angle[0][1]:
            best_angle[0] = (offset, abs(other_y - resulting_target))
        elif not direction and abs(other_y - resulting_target) > best_angle[1][1]:
            best_angle[1] = (offset, abs(other_y - resulting_target))

def get_resulting_target(target, target_angle, ball_size, board_width, board_height, dx):
    dy = math.tan(target_angle) * dx

    # Get final location
    target_y = dy + target

    #Adjust for bounces
    num_bounces = abs((target_y - ball_size / 2) // (board_height - ball_size))
    if num_bounces == 0:
        return target_y
    offset = abs(target_y - ball_size / 2) % (board_height - ball_size)
    # If final bounce is from top
    if dy * ((-1) ** (int(num_bounces) % 2)) > 0:
        return offset + ball_size / 2
    # If final bounce is from bottom
    else:
        return board_height - ball_size / 2 - offset

def calculate_opponent_path(paddle_x, other_x, other_y, table_size, ball_size, target, impact_angle, paddle_height, paddle_width, max_angle):

    # Calculate target angle
    paddle_offset = other_y - target
    rel_angle = - paddle_offset * max_angle / paddle_height
    target_angle = 2 * rel_angle + impact_angle * 0.632076052 #???????


    # Extract into dx and dy
    dx = table_size[0] - paddle_width - 2*min(other_x, paddle_x)
    dy = math.tan(target_angle) * dx

    # Get final location
    target_y = dy + target

    #Adjust for bounces
    num_bounces = abs((target_y - ball_size / 2) // (table_size[1] - ball_size))
    if num_bounces == 0:
        return target_y
    offset = abs(target_y - ball_size / 2) % (table_size[1] - ball_size)

    # If final bounce is from top
    if dy * ((-1) ** (int(num_bounces) % 2)) > 0:
        return offset + ball_size / 2
    # If final bounce is from bottom
    else:
        return table_size[1] - ball_size / 2 - offset

def calculate_path(paddle_x, other_x, paddle_width, height, width, ball_size):
    # Estimate of average velocity
    dx, dy = get_ball_velocity()

    velocity = math.sqrt(dx ** 2 + dy ** 2)
    if dx == 0:
        return height / 2, 0, -1, velocity

    # Determining positive vs negative displacement and adjusting for the paddle width
    if paddle_x > width / 2:
        paddle_x -= paddle_width
    else:
        paddle_x += paddle_width

    # If ball is moving away from paddle
    if (paddle_x - coords_list[0][0]) * dx < 0:
        x_dist = other_x - coords_list[-1][0]
        x_dist -= abs(x_dist) / x_dist * ball_size / 2

        t_x = abs(x_dist / dx)
    # If ball is moving towards paddle
    else:
        x_dist = paddle_x - coords_list[-1][0]
        x_dist -= abs(x_dist) / x_dist * ball_size / 2
        t_x = -abs(x_dist / dx)
        if abs(dy / dx) > 2:
            x_dist += abs(x_dist) / x_dist * ball_size

    # Get final y-position
    target_y = x_dist / dx * dy + coords_list[-1][1]

    # Correct for bouncing
    num_bounces = abs((target_y - ball_size / 2) // (height - ball_size * 0.8743115181904614))
    if num_bounces == 0:
        return target_y, math.atan(dy / abs(dx)), t_x, velocity
    offset = abs(target_y - ball_size / 2) % (height - ball_size * 0.8743115181904614)

    # If final bounce is from top
    if dy * ((-1) ** (int(num_bounces) % 2)) > 0:
        return offset + ball_size / 2, abs(math.atan(dy / dx)), t_x, velocity
    # If final bounce is from bottom
    else:
        return height - ball_size / 2 - offset, -abs(math.atan(dy/dx)), t_x, velocity

def get_ball_velocity():
    dx = [coords_list[i+1][0] - coords_list[i][0] for i in range(len(coords_list) - 1)]
    dx = sum(dx) / len(dx)
    dy = [coords_list[i+1][1] - coords_list[i][1] for i in range(len(coords_list) - 1)]
    dy = sum(dy) / len(dy)
    return dx, dy

def read_board(ball_frect, other_frect, paddle_frect):
    global coords_list, opponent_pos, my_pos, my_speed
    coords_list.pop(0)
    coords_list.append([ball_frect.pos[0] + ball_frect.size[0] / 2, ball_frect.pos[1] + ball_frect.size[1] / 2])
    opponent_pos.pop(0)
    opponent_pos.append(other_frect.pos[1])
    my_pos.pop(0)
    my_pos.append(paddle_frect.pos[1])
    if my_pos[0] != -1:
        speed = my_pos[1] - my_pos[0]
        if speed != 0:
            my_speed = abs(speed)

def pong_ai(paddle_frect, other_paddle_frect, ball_frect, table_size):
    '''return "up" or "down", depending on which way the paddle should go to
    align its centre with the centre of the ball, assuming the ball will
    not be moving

    Arguments:
    paddle_frect: a rectangle representing the coordinates of the paddle
                  paddle_frect.pos[0], paddle_frect.pos[1] is the top-left
                  corner of the rectangle.
                  paddle_frect.size[0], paddle_frect.size[1] are the dimensions
                  of the paddle along the x and y axis, respectively

    other_paddle_frect:
                  a rectangle representing the opponent paddle. It is formatted
                  in the same way as paddle_frect
    ball_frect:   a rectangle representing the ball. It is formatted in the
                  same way as paddle_frect
    table_size:   table_size[0], table_size[1] are the dimensions of the table,
                  along the x and the y axis respectively

    The coordinates look as follows:

     0             x
     |------------->
     |
     |
     |
 y   v
    '''
    pong_ai.team_name = "Rusty_Gusty"


    read_board(ball_frect, other_paddle_frect, paddle_frect)
    direction = return_trajectory(paddle_frect.pos[0] + paddle_frect.size[0] / 2, paddle_frect.pos[1] + paddle_frect.size[1] / 2, paddle_frect.size[0], paddle_frect.size[1], other_paddle_frect.pos[0] + other_paddle_frect.size[0] / 2, other_paddle_frect.pos[1] + other_paddle_frect.size[1] / 2, ball_frect.size[1], table_size)

    if direction:
     return "up"
    else:
     return "down"

initialize()