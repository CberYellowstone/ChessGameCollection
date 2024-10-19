# gomoku.py

import pygame

# 定义颜色
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)

# 初始化五子棋游戏状态
gomoku_board = [[None for _ in range(19)] for _ in range(19)]
gomoku_turn = "黑子"


def draw_gomoku_board(screen, width, height):
    # 绘制棋盘
    for i in range(19):
        pygame.draw.line(
            screen,
            black,
            (width / 2 - 270 + i * 30, height / 2 - 270),
            (width / 2 - 270 + i * 30, height / 2 + 270),
        )
        pygame.draw.line(
            screen,
            black,
            (width / 2 - 270, height / 2 - 270 + i * 30),
            (width / 2 + 270, height / 2 - 270 + i * 30),
        )

    # 绘制棋子
    for i in range(19):
        for j in range(19):
            if gomoku_board[i][j] is not None:
                color = black if gomoku_board[i][j] == "黑子" else white
                pygame.draw.circle(
                    screen,
                    color,
                    (width / 2 - 270 + j * 30, height / 2 - 270 + i * 30),
                    12,
                )

    # 绘制当前玩家提示
    font = pygame.font.SysFont("Microsoft YaHei", 36, True)
    player_color = black if gomoku_turn == "黑子" else white
    player_text = f"当前玩家: {gomoku_turn}"
    text = font.render(player_text, True, player_color)
    text_rect = text.get_rect(center=(width - 150, 50))
    screen.blit(text, text_rect)


def handle_gomoku_click(mouse_pos, width, height):
    global gomoku_turn
    for i in range(19):
        for j in range(19):
            rect = pygame.Rect(
                width / 2 - 285 + j * 30, height / 2 - 285 + i * 30, 30, 30
            )
            if rect.collidepoint(mouse_pos) and gomoku_board[i][j] is None:
                gomoku_board[i][j] = gomoku_turn
                gomoku_turn = "白子" if gomoku_turn == "黑子" else "黑子"
                break


def check_gomoku_winner():
    # 检查横向、纵向和斜向的胜利条件
    for i in range(19):
        for j in range(19):
            if gomoku_board[i][j] is not None:
                # 检查横向
                if j <= 14 and all(
                    gomoku_board[i][j + k] == gomoku_board[i][j] for k in range(5)
                ):
                    return gomoku_board[i][j]
                # 检查纵向
                if i <= 14 and all(
                    gomoku_board[i + k][j] == gomoku_board[i][j] for k in range(5)
                ):
                    return gomoku_board[i][j]
                # 检查斜向（左上到右下）
                if (
                    i <= 14
                    and j <= 14
                    and all(
                        gomoku_board[i + k][j + k] == gomoku_board[i][j]
                        for k in range(5)
                    )
                ):
                    return gomoku_board[i][j]
                # 检查斜向（右上到左下）
                if (
                    i <= 14
                    and j >= 4
                    and all(
                        gomoku_board[i + k][j - k] == gomoku_board[i][j]
                        for k in range(5)
                    )
                ):
                    return gomoku_board[i][j]
    return None


def reset_gomoku():
    global gomoku_board, gomoku_turn
    gomoku_board = [[None for _ in range(19)] for _ in range(19)]
    gomoku_turn = "黑子"


def render_gomoku(screen, font, width, height, game_over, winner, winner_font):
    # 填充背景颜色
    screen.fill((254, 220, 162))  # 棋盘背景颜色

    # 绘制五子棋棋盘
    draw_gomoku_board(screen, width, height)

    # 显示胜利方
    if game_over and winner:
        winner_surface = winner_font.render(f"{winner} 获胜", True, (255, 0, 0))
        winner_rect = winner_surface.get_rect(center=(width / 2, height / 2))
        screen.blit(winner_surface, winner_rect)

    # 返回主页面的按钮
    back_surface = font.render("返回主页面", True, black)
    back_rect = back_surface.get_rect(bottomright=(width - 10, height - 10))
    screen.blit(back_surface, back_rect)

    return back_rect
