import numpy as np
import pygame

# 定义颜色
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
piece_color_fill = (231, 173, 79)  ##e7ad4f
highlight_color = (0, 255, 0)  # 绿色，用于高亮可走位置


class ChineseChessEnv:
    ini_board = np.array(
        [
            [1, 2, 3, 4, 5, 4, 3, 2, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 6, 0, 0, 0, 0, 0, 6, 0],
            [7, 0, 7, 0, 7, 0, 7, 0, 7],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-7, 0, -7, 0, -7, 0, -7, 0, -7],
            [0, -6, 0, 0, 0, 0, 0, -6, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-1, -2, -3, -4, -5, -4, -3, -2, -1],
        ]
    )
    pieces_dict = {
        1: "车",
        2: "马",
        3: "象",
        4: "士",
        5: "帅",
        6: "炮",
        7: "兵",
        -1: "車",
        -2: "馬",
        -3: "相",
        -4: "仕",
        -5: "将",
        -6: "砲",
        -7: "卒",
    }

    def __init__(self):
        self.board = ChineseChessEnv.ini_board.copy()
        self.chess_player = 1  # 1红 -1黑
        self.reset()

    def reset(self):
        self.board = ChineseChessEnv.ini_board.copy()
        self.chess_player = 1
        return self.board

    def step(self, action):
        done = False
        reward = 0
        info = None
        observation = None
        chess_pieces_position = action[0]
        move_position = action[1]
        chess_pieces = self.board[chess_pieces_position]
        move_pieces = self.board[move_position]
        if chess_pieces * self.chess_player > 0:
            if chess_pieces * move_pieces > 0:
                info = 0
            else:
                info = int(self.get_do_position(chess_pieces_position, move_position))

            if info:
                if abs(self.board[move_position]) == 5:
                    done = True
                if self.board[move_position] * self.chess_player == 1:
                    reward = 1
                self.board[move_position] = chess_pieces
                self.board[chess_pieces_position] = 0
            else:
                reward = -1
            observation = self.board.copy()
        elif chess_pieces * self.chess_player == 0:
            observation = self.board.copy()
            reward = -1
            done = False
            info = 2
        else:
            observation = self.board.copy()
            reward = -1
            done = False
            info = 3
        if info == 1:
            self.chess_player = -1 * self.chess_player
        return observation, reward, done, info

    def get_do_position(self, chess_pieces_position, move_position):
        """
        传入位置已经经过
        1.是否将行棋子为空
        2.将行棋子是否是当前应执棋者
        3.将行棋子的位置和将行位置上的棋子是否属于同一方
        判断，然后

        首先根据chess_pieces_position确定棋子的种类
            根据棋子的种类和位置确定其在该位置下可行的
            黑红双方在各个种类中自己判断，因为有些棋子有通用规则

        :param chess_pieces_position: 棋子的位置
        :param move_position: 棋子将行的位置
        :return: 棋子到将行的位置是否可行 int(info)
        """

        assert type(chess_pieces_position) == tuple and type(move_position) == tuple
        info = None
        chess_pieces = ChineseChessEnv.pieces_dict[self.board[chess_pieces_position]]
        move_pieces = self.board[move_position]

        # 检查当前棋子是否为当前阵营的
        if self.board[chess_pieces_position] * self.chess_player <= 0:
            return False

        # 检查目标位置是否有己方棋子
        if move_pieces * self.chess_player > 0:
            return False

        if chess_pieces in ("车", "車"):  # 车
            move_row = move_position[0]
            move_column = move_position[1]
            if move_row == chess_pieces_position[0]:
                a = move_column - chess_pieces_position[1]
                if a != 0:
                    for i in range(
                        int(a / abs(a)), int(a), int(a / abs(a))
                    ):  # 去头去尾
                        position = (move_row, i + chess_pieces_position[1])
                        if self.board[position] != 0:
                            info = False
                            break
                    else:
                        info = True
                else:
                    info = False
            elif move_column == chess_pieces_position[1]:
                a = move_row - chess_pieces_position[0]
                if a != 0:
                    for i in range(
                        int(a / abs(a)), int(a), int(a / abs(a))
                    ):  # 去头去尾
                        position = (i + chess_pieces_position[0], move_column)
                        if self.board[position] != 0:
                            info = False
                            break
                    else:
                        info = True
                else:
                    info = False
            else:
                info = False

        elif chess_pieces in ("马", "馬"):  # 马
            row = chess_pieces_position[0]
            column = chess_pieces_position[1]
            do_position = [
                (row - 2, column + 1),
                (row - 2, column - 1),
                (row + 2, column + 1),
                (row + 2, column - 1),
                (row + 1, column - 2),
                (row - 1, column - 2),
                (row + 1, column + 2),
                (row - 1, column + 2),
            ]
            try:
                index = (
                    do_position.index(move_position) // 2
                )  # move_position可能不在里面，防止出错
                if index == 0:
                    if self.board[row - 1, column] != 0:
                        info = False
                    else:
                        info = True
                elif index == 1:
                    if self.board[row + 1, column] != 0:
                        info = False
                    else:
                        info = True
                elif index == 2:
                    if self.board[row, column - 1] != 0:
                        info = False
                    else:
                        info = True
                else:
                    if self.board[row, column + 1] != 0:
                        info = False
                    else:
                        info = True
            except ValueError:
                info = False

        elif chess_pieces in ("相", "象"):  # 相
            xiang_possible_position = {
                (0, 2): [(2, 0), (2, 4)],
                (0, 6): [(2, 4), (2, 8)],
                (2, 0): [(0, 2), (4, 2)],
                (2, 4): [(0, 2), (0, 6), (4, 2), (4, 6)],
                (2, 8): [(0, 6), (4, 6)],
                (4, 2): [(2, 0), (2, 4)],
                (4, 6): [(2, 4), (2, 8)],
                (9, 2): [(7, 0), (7, 4)],
                (9, 6): [(7, 4), (7, 8)],
                (7, 0): [(9, 2), (5, 2)],
                (7, 4): [(9, 2), (9, 6), (5, 2), (5, 6)],
                (7, 8): [(9, 6), (5, 6)],
                (5, 2): [(7, 0), (7, 4)],
                (5, 6): [(7, 4), (7, 8)],
            }
            do_position = xiang_possible_position.get(chess_pieces_position, [])
            if move_position not in do_position:
                info = False
            else:
                mid_row = int((chess_pieces_position[0] + move_position[0]) / 2)
                mid_column = int((chess_pieces_position[1] + move_position[1]) / 2)
                middle_position = (mid_row, mid_column)
                if self.board[middle_position] == 0:
                    info = True
                else:
                    info = False

        elif chess_pieces in ("仕", "士"):  # 仕
            shi_possible_position = {
                (0, 3): [(1, 4)],
                (0, 5): [(1, 4)],
                (1, 4): [(0, 3), (0, 5), (2, 3), (2, 5)],
                (2, 3): [(1, 4)],
                (2, 5): [(1, 4)],
                (9, 3): [(8, 4)],
                (9, 5): [(8, 4)],
                (8, 4): [(9, 3), (9, 5), (7, 3), (7, 5)],
                (7, 3): [(8, 4)],
                (7, 5): [(8, 4)],
            }
            try:
                do_position = shi_possible_position[chess_pieces_position]
            except KeyError:
                info = False
            else:
                if move_position not in do_position:
                    info = False
                else:
                    info = True

        elif chess_pieces in ("将", "帅"):  # 将
            move_row = move_position[0]
            move_column = move_position[1]
            if (2 < move_row < 7) or (move_column < 3 or move_column > 5):
                info = False
            else:
                judge = abs(chess_pieces_position[0] - move_row) + abs(
                    chess_pieces_position[1] - move_column
                )
                if judge == 1:
                    info = True
                else:
                    info = False

            if (
                abs(self.board[move_position]) == 5
                and chess_pieces_position[1] == move_column
            ):
                a = move_row - chess_pieces_position[0]
                if a != 0:
                    for i in range(
                        int(a / abs(a)), int(a), int(a / abs(a))
                    ):  # 去头去尾
                        position = (i + chess_pieces_position[0], move_column)
                        if self.board[position] != 0:
                            break
                    else:
                        info = True

        elif chess_pieces in ("炮", "砲"):  # 炮
            move_row = move_position[0]
            move_column = move_position[1]
            judge = (
                self.board[move_position] * self.board[chess_pieces_position] < 0
            )  # move_postion是否是敌方
            if move_row == chess_pieces_position[0]:
                a = move_column - chess_pieces_position[1]
                if a != 0:
                    pieces_num = 0
                    for i in range(int(a / abs(a)), int(a), int(a / abs(a))):
                        position = (move_row, i + chess_pieces_position[1])
                        if self.board[position] != 0:
                            pieces_num = pieces_num + 1

                    if judge and pieces_num == 1:
                        info = True
                    else:
                        if not judge and pieces_num == 0:
                            info = True
                        else:
                            info = False
                else:
                    info = False
            elif move_column == chess_pieces_position[1]:
                a = move_row - chess_pieces_position[0]
                if a != 0:
                    pieces_num = 0
                    for i in range(int(a / abs(a)), int(a), int(a / abs(a))):
                        position = (i + chess_pieces_position[0], move_column)
                        if self.board[position] != 0:
                            pieces_num = pieces_num + 1
                    if judge and pieces_num == 1:
                        info = True
                    else:
                        if not judge and pieces_num == 0:
                            info = True
                        else:
                            info = False
                else:
                    info = False
            else:
                info = False

        elif chess_pieces in ("兵", "卒"):  # 士
            boundary_dict = {1: 4, -1: 5}
            judge = abs(chess_pieces_position[0] - move_position[0]) + abs(
                chess_pieces_position[1] - move_position[1]
            )
            if judge > 1:
                info = False
            else:
                boundary = boundary_dict[self.chess_player]
                if (
                    self.chess_player * chess_pieces_position[0]
                    <= self.chess_player * boundary
                ):
                    do_position = (
                        chess_pieces_position[0] + self.chess_player,
                        chess_pieces_position[1],
                    )
                    if do_position == move_position:
                        info = True
                    else:
                        info = False
                else:
                    do_position = (
                        chess_pieces_position[0] - self.chess_player,
                        chess_pieces_position[1],
                    )
                    if do_position == move_position:
                        info = False
                    else:
                        info = True

        else:
            raise ValueError

        return info

    def render(self, screen, selected_piece=None):
        for i in range(10):
            for j in range(9):
                # 绘制棋盘线条
                if i < 9:
                    pygame.draw.line(
                        screen,
                        black,
                        (j * 60 + 30, i * 60 + 30),
                        (j * 60 + 30, (i + 1) * 60 + 30),
                        1,
                    )
                if j < 8:
                    pygame.draw.line(
                        screen,
                        black,
                        (j * 60 + 30, i * 60 + 30),
                        ((j + 1) * 60 + 30, i * 60 + 30),
                        1,
                    )
                # 绘制棋子
                if self.board[i, j] != 0:
                    piece = self.pieces_dict[self.board[i, j]]
                    piece_color = red if self.board[i, j] > 0 else black
                    font = pygame.font.SysFont("SimHei", 36)
                    text = font.render(piece, True, piece_color)
                    text_rect = text.get_rect(center=(j * 60 + 30, i * 60 + 30))
                    pygame.draw.circle(
                        screen, piece_color_fill, (j * 60 + 30, i * 60 + 30), 25
                    )
                    screen.blit(text, text_rect)

                    # 如果是选中的棋子，绘制方框
                    if selected_piece == (i, j):
                        pygame.draw.rect(
                            screen,
                            highlight_color,
                            pygame.Rect(j * 60 + 5, i * 60 + 5, 50, 50),
                            3,
                        )

        # 绘制可走位置
        if selected_piece:
            for i in range(10):
                for j in range(9):
                    if self.get_do_position(selected_piece, (i, j)):
                        pygame.draw.circle(
                            screen, highlight_color, (j * 60 + 30, i * 60 + 30), 5
                        )

    def close(self):
        pass

    def get_action(self, mouse_pos):
        x, y = mouse_pos
        for row in range(10):
            for col in range(9):
                center_x = col * 60 + 30
                center_y = row * 60 + 30
                if (x - center_x) ** 2 + (y - center_y) ** 2 <= 25**2:
                    return (row, col)
        return None

    def render_player_indicator(self, screen, width):
        player_text = "红方" if self.chess_player == 1 else "黑方"
        player_color = red if self.chess_player == 1 else black
        font = pygame.font.SysFont("Microsoft YaHei", 36, True)
        text = font.render(f"当前玩家: {player_text}", True, player_color)
        text_rect = text.get_rect(center=(width - 150, 50))
        screen.blit(text, text_rect)

    def render_winner(self, screen, width, height, winner):
        if winner:
            winner_font = pygame.font.SysFont("Microsoft YaHei", 72, True)
            winner_surface = winner_font.render(f"{winner} 获胜", True, red)
            winner_rect = winner_surface.get_rect(center=(width / 2, height / 2))
            screen.blit(winner_surface, winner_rect)

    def handle_click(self, mouse_pos, selected_piece, game_over):
        winner = None  # 初始化 winner 变量
        action = self.get_action(mouse_pos)
        if action and not game_over:
            if selected_piece:
                if (
                    self.board[action] * self.chess_player > 0
                    and action != selected_piece
                ):
                    # 切换当前举起的棋子
                    selected_piece = action
                else:
                    move_position = action
                    observation, reward, done, info = self.step(
                        (selected_piece, move_position)
                    )
                    selected_piece = None
                    if done:
                        game_over = True
                        winner = "黑棋" if self.chess_player == 1 else "红棋"
            else:
                # 检查选中的棋子是否属于当前玩家的阵营
                if self.board[action] * self.chess_player > 0:
                    selected_piece = action
        return selected_piece, game_over, winner


def render_chinese_chess(
    screen, chinese_chess_env, selected_piece, width, height, winner
):
    # 填充背景颜色
    screen.fill((254, 220, 162))  # 棋盘背景颜色

    # 绘制中国象棋棋盘
    render_board(screen, chinese_chess_env, selected_piece)
    render_player_indicator(screen, chinese_chess_env, width)

    # 显示胜利方
    render_winner(screen, width, height, winner)


def render_board(screen, chinese_chess_env, selected_piece):
    for i in range(10):
        for j in range(9):
            # 绘制棋盘线条
            if i < 9:
                pygame.draw.line(
                    screen,
                    black,
                    (j * 60 + 30, i * 60 + 30),
                    (j * 60 + 30, (i + 1) * 60 + 30),
                    1,
                )
            if j < 8:
                pygame.draw.line(
                    screen,
                    black,
                    (j * 60 + 30, i * 60 + 30),
                    ((j + 1) * 60 + 30, i * 60 + 30),
                    1,
                )
            # 绘制棋子
            if chinese_chess_env.board[i, j] != 0:
                piece = ChineseChessEnv.pieces_dict[chinese_chess_env.board[i, j]]
                piece_color = red if chinese_chess_env.board[i, j] > 0 else black
                font = pygame.font.SysFont("SimHei", 36)
                text = font.render(piece, True, piece_color)
                text_rect = text.get_rect(center=(j * 60 + 30, i * 60 + 30))
                pygame.draw.circle(
                    screen, piece_color_fill, (j * 60 + 30, i * 60 + 30), 25
                )
                screen.blit(text, text_rect)

                # 如果是选中的棋子，绘制方框
                if selected_piece == (i, j):
                    pygame.draw.rect(
                        screen,
                        highlight_color,
                        pygame.Rect(j * 60 + 5, i * 60 + 5, 50, 50),
                        3,
                    )

    # 绘制可走位置
    if selected_piece:
        for i in range(10):
            for j in range(9):
                if chinese_chess_env.get_do_position(selected_piece, (i, j)):
                    pygame.draw.circle(
                        screen, highlight_color, (j * 60 + 30, i * 60 + 30), 5
                    )


def render_player_indicator(screen, chinese_chess_env, width):
    player_text = "红方" if chinese_chess_env.chess_player == 1 else "黑方"
    player_color = red if chinese_chess_env.chess_player == 1 else black
    font = pygame.font.SysFont("Microsoft YaHei", 36, True)
    text = font.render(f"当前玩家: {player_text}", True, player_color)
    text_rect = text.get_rect(center=(width - 150, 50))
    screen.blit(text, text_rect)


def render_winner(screen, width, height, winner):
    if winner:
        winner_font = pygame.font.SysFont("Microsoft YaHei", 72, True)
        winner_surface = winner_font.render(f"{winner} 获胜", True, red)
        winner_rect = winner_surface.get_rect(center=(width / 2, height / 2))
        screen.blit(winner_surface, winner_rect)
