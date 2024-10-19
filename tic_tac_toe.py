# tic_tac_toe.py

import pygame

# 定义颜色
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)

# 初始化井字棋游戏状态
tic_tac_toe_board = [[None, None, None], [None, None, None], [None, None, None]]
tic_tac_toe_turn = "X"


def draw_tic_tac_toe_board(screen, font, width, height, color):
    large_font = pygame.font.SysFont("Microsoft YaHei", 72, True)  # 使用更大的字体
    for i in range(3):
        for j in range(3):
            rect = pygame.Rect(
                width / 2 - 150 + j * 100, height / 2 - 150 + i * 100, 100, 100
            )
            pygame.draw.rect(screen, color, rect, 3)
            if tic_tac_toe_board[i][j] is not None:
                mark = large_font.render(tic_tac_toe_board[i][j], True, color)
                mark_rect = mark.get_rect(center=rect.center)
                screen.blit(mark, mark_rect)


def handle_tic_tac_toe_click(mouse_pos, width, height):
    global tic_tac_toe_turn
    for i in range(3):
        for j in range(3):
            rect = pygame.Rect(
                width / 2 - 150 + j * 100, height / 2 - 150 + i * 100, 100, 100
            )
            if rect.collidepoint(mouse_pos) and tic_tac_toe_board[i][j] is None:
                tic_tac_toe_board[i][j] = tic_tac_toe_turn
                tic_tac_toe_turn = "O" if tic_tac_toe_turn == "X" else "X"
                break


def check_winner():
    # 检查行
    for row in tic_tac_toe_board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]
    # 检查列
    for col in range(3):
        if (
            tic_tac_toe_board[0][col]
            == tic_tac_toe_board[1][col]
            == tic_tac_toe_board[2][col]
            and tic_tac_toe_board[0][col] is not None
        ):
            return tic_tac_toe_board[0][col]
    # 检查对角线
    if (
        tic_tac_toe_board[0][0] == tic_tac_toe_board[1][1] == tic_tac_toe_board[2][2]
        and tic_tac_toe_board[0][0] is not None
    ):
        return tic_tac_toe_board[0][0]
    if (
        tic_tac_toe_board[0][2] == tic_tac_toe_board[1][1] == tic_tac_toe_board[2][0]
        and tic_tac_toe_board[0][2] is not None
    ):
        return tic_tac_toe_board[0][2]
    return None


def reset_tic_tac_toe():
    global tic_tac_toe_board, tic_tac_toe_turn
    tic_tac_toe_board = [[None, None, None], [None, None, None], [None, None, None]]
    tic_tac_toe_turn = "X"


def render_tic_tac_toe(
    screen, font, width, height, current_player, game_over, winner, winner_font
):
    # 填充背景颜色
    screen.fill((254, 220, 162))  # 棋盘背景颜色

    # 绘制井字棋棋盘
    draw_tic_tac_toe_board(screen, font, width, height, black)

    # 显示当前玩家
    player_surface = font.render(f"当前玩家: {current_player}", True, black)
    player_rect = player_surface.get_rect(center=(width / 2, 50))
    screen.blit(player_surface, player_rect)

    # 显示胜利方
    if game_over and winner:
        winner_surface = winner_font.render(f"{winner} 获胜", True, (255, 0, 0))
        winner_rect = winner_surface.get_rect(center=(width / 2, height * 0.8))
        screen.blit(winner_surface, winner_rect)

    # 返回主页面的按钮
    back_surface = font.render("返回主页面", True, black)
    back_rect = back_surface.get_rect(bottomright=(width - 10, height - 10))
    screen.blit(back_surface, back_rect)

    return back_rect
