import sys

import pygame

import chinese_chess  # 引入中国象棋逻辑
import fight_chess  # 引入飞行棋逻辑
import gomoku  # 引入五子棋逻辑
import tic_tac_toe  # 引入井字棋逻辑

# 初始化 Pygame
pygame.init()

# 设置窗口大小和标题
size = width, height = 800, 600
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption("棋类游戏合集")
clock = pygame.time.Clock()

HALF_WIDTH = width / 2

# 定义颜色
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
background_color = (254, 220, 162)  # 棋盘背景颜色

# 加载系统字体
font = pygame.font.SysFont("Microsoft YaHei", 36, True)  # 使用系统自带的微软雅黑字体
title_font = pygame.font.SysFont("Microsoft YaHei", 48, True)  # 标题字体
winner_font = pygame.font.SysFont("Microsoft YaHei", 72, True)  # 胜利字体

# 定义游戏名称和位置
games = [
    ("五子棋", (HALF_WIDTH, 200)),
    ("中国象棋", (HALF_WIDTH, 300)),
    ("井字棋", (HALF_WIDTH, 400)),
    ("飞行棋", (HALF_WIDTH, 500)),
]

# 全屏标志
fullscreen = False

# 当前页面标志
current_page = "main"

# 实例化中国象棋类
chinese_chess_env = chinese_chess.ChineseChessEnv()

# 实例化飞行棋类
fight_chess_env = fight_chess.FightChess(screen, width, height)

# 游戏结束标志和胜利方
game_over = False
winner = None

# 当前玩家
current_player = "X"

# 主循环
selected_piece = None


def render_back_button(screen, font, width, height):
    back_surface = font.render("返回主页面", True, black)
    back_rect = back_surface.get_rect(bottomright=(width - 10, height - 10))
    screen.blit(back_surface, back_rect)
    return back_rect


def handle_back_button_click(mouse_pos, back_rect):
    global current_page, game_over, winner, current_player
    if back_rect.collidepoint(mouse_pos):
        current_page = "main"
        game_over = False
        winner = None
        current_player = "X"  # 重置当前玩家
        return True
    return False


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            size = width, height = event.size
            screen = pygame.display.set_mode(size, pygame.RESIZABLE)
            fight_chess_env.handle_resize(width, height)
            # 更新游戏名称的位置
            HALF_WIDTH = width / 2
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
                fight_chess_env.handle_resize(width, height)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if current_page == "main":
                for game in games:
                    text, pos = game
                    text_surface = font.render(text, True, white)
                    text_rect = text_surface.get_rect(center=pos)
                    if text_rect.collidepoint(mouse_pos):
                        current_page = text
                        game_over = False
                        winner = None
                        current_player = "X"  # 重置当前玩家
            elif current_page == "中国象棋" and not game_over:
                selected_piece, game_over, winner = chinese_chess_env.handle_click(
                    mouse_pos, selected_piece, game_over
                )
            elif current_page == "井字棋" and not game_over:
                tic_tac_toe.handle_tic_tac_toe_click(mouse_pos, width, height)
                winner = tic_tac_toe.check_winner()
                if winner:
                    game_over = True
                else:
                    current_player = "O" if current_player == "X" else "X"  # 切换玩家
            elif current_page == "五子棋" and not game_over:
                gomoku.handle_gomoku_click(mouse_pos, width, height)
                winner = gomoku.check_gomoku_winner()
                if winner:
                    game_over = True
            elif current_page == "飞行棋":
                fight_chess_env.handle_click(mouse_pos)

    if current_page == "main":
        # 填充背景颜色
        screen.fill(black)

        # 绘制标题
        title_surface = title_font.render("ChessGameCollection", True, white)
        title_rect = title_surface.get_rect(center=(width / 2, 100))
        screen.blit(title_surface, title_rect)

        # 获取鼠标位置
        mouse_pos = pygame.mouse.get_pos()

        # 绘制游戏名称
        for game in games:
            text, pos = game
            text_surface = font.render(
                text,
                True,
                (
                    yellow
                    if pygame.Rect(pos[0] - 100, pos[1] - 20, 200, 40).collidepoint(
                        mouse_pos
                    )
                    else white
                ),
            )
            text_rect = text_surface.get_rect(center=pos)
            screen.blit(text_surface, text_rect)
    elif current_page == "中国象棋":
        chinese_chess.render_chinese_chess(
            screen, chinese_chess_env, selected_piece, width, height, winner
        )
        # 渲染返回主页面按钮
        back_rect = render_back_button(screen, font, width, height)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if handle_back_button_click(mouse_pos, back_rect):
                chinese_chess_env.reset()
    elif current_page == "井字棋":
        back_rect = tic_tac_toe.render_tic_tac_toe(
            screen, font, width, height, current_player, game_over, winner, winner_font
        )
        # 渲染返回主页面按钮
        back_rect = render_back_button(screen, font, width, height)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if handle_back_button_click(mouse_pos, back_rect):
                tic_tac_toe.reset_tic_tac_toe()
    elif current_page == "五子棋":
        back_rect = gomoku.render_gomoku(
            screen, font, width, height, game_over, winner, winner_font
        )
        # 渲染返回主页面按钮
        back_rect = render_back_button(screen, font, width, height)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if handle_back_button_click(mouse_pos, back_rect):
                gomoku.reset_gomoku()
    elif current_page == "飞行棋":
        fight_chess_env.render()
        # 渲染返回主页面按钮
        back_rect = render_back_button(screen, font, width, height)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if handle_back_button_click(mouse_pos, back_rect):
                fight_chess_env.reset_game()

    # 更新显示
    pygame.display.flip()
    clock.tick(60)
