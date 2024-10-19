import random

import pygame


class FightChess:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.initial_width = width
        self.initial_height = height

        # 加载飞行棋背景图片
        self.bg_initial_image = pygame.image.load("res/background.svg")
        self.background_image = self.scale_background_image(
            self.bg_initial_image, width, height
        )

        # 初始棋子坐标
        self.initial_pos_list = [
            (38, 38),
            (102, 40),
            (39, 100),
            (102, 100),
            (496, 39),
            (560, 40),
            (497, 99),
            (562, 100),
            (41, 495),
            (100, 495),
            (41, 553),
            (103, 553),
            (496, 495),
            (561, 495),
            (497, 554),
            (562, 555),
            (22, 162),
            (432, 24),
            (163, 577),
            (436, 576),
            (47, 189),
            (87, 176),
            (124, 177),
            (161, 190),
            (190, 164),
            (177, 124),
            (177, 89),
            (190, 52),
            (229, 38),
            (263, 37),
            (299, 37),
            (331, 36),
            (367, 36),
            (405, 53),
            (419, 90),
            (418, 124),
            (405, 168),
            (429, 193),
            (472, 177),
            (506, 177),
            (544, 193),
            (558, 231),
            (557, 264),
            (555, 302),
            (558, 334),
            (558, 368),
            (545, 409),
            (507, 420),
            (470, 420),
            (432, 406),
            (404, 435),
            (420, 474),
            (419, 509),
            (405, 547),
            (366, 560),
            (331, 559),
            (296, 561),
            (260, 560),
            (227, 559),
            (188, 550),
            (173, 506),
            (174, 473),
            (189, 434),
            (158, 407),
            (122, 420),
            (86, 420),
            (51, 408),
            (36, 369),
            (35, 333),
            (36, 298),
            (36, 264),
            (35, 229),
            (297, 96),
            (296, 129),
            (297, 164),
            (296, 198),
            (296, 232),
            (297, 266),
            (503, 301),
            (468, 301),
            (434, 303),
            (400, 302),
            (366, 302),
            (331, 302),
            (296, 509),
            (296, 473),
            (297, 441),
            (298, 406),
            (297, 373),
            (297, 338),
            (90, 299),
            (125, 300),
            (159, 298),
            (192, 298),
            (227, 299),
            (262, 298),
        ]

        self.pos_list = [
            (int(x * width / self.initial_width), int(y * height / self.initial_height))
            for x, y in self.initial_pos_list
        ]

        # 加载并缩放棋子图片
        self.blue_piece_initial_image = pygame.image.load("res/蓝棋子.svg")
        self.blue_piece_image = self.scale_piece_img(self.blue_piece_initial_image)

        self.red_piece_initial_image = pygame.image.load("res/红棋子.svg")
        self.red_piece_image = self.scale_piece_img(self.red_piece_initial_image)

        self.green_piece_initial_image = pygame.image.load("res/绿棋子.svg")
        self.green_piece_image = self.scale_piece_img(self.green_piece_initial_image)

        self.yellow_piece_initial_image = pygame.image.load("res/黄棋子.svg")
        self.yellow_piece_image = self.scale_piece_img(self.yellow_piece_initial_image)

        self.piece_initial_image = {
            "green": self.green_piece_image,
            "red": self.red_piece_image,
            "blue": self.blue_piece_image,
            "yellow": self.yellow_piece_image,
        }

        self.piece_image = {
            "green": self.green_piece_image,
            "red": self.red_piece_image,
            "blue": self.blue_piece_image,
            "yellow": self.yellow_piece_image,
        }

        self.airports_index = {
            "green": (0, 1, 2, 3),
            "red": (4, 5, 6, 7),
            "blue": (8, 9, 10, 11),
            "yellow": (12, 13, 14, 15),
        }

        self.paths = {
            "green": [16] + list(range(20, 70)) + list(range(90, 96)),
            "red": [17]
            + list(range(33, 72))
            + list(range(20, 31))
            + list(range(72, 78)),
            "blue": [18]
            + list(range(59, 72))
            + list(range(20, 57))
            + list(range(84, 90)),
            "yellow": [19]
            + list(range(53, 72))
            + list(range(20, 44))
            + list(range(78, 84)),
        }

        # 加载系统字体
        self.id_font = pygame.font.SysFont("Microsoft YaHei", 24, True)

        # 初始化游戏状态
        self.reset_game()

    def scale_background_image(self, image, screen_width, screen_height):
        image_width, image_height = image.get_size()
        image_ratio = image_width / image_height
        screen_ratio = screen_width / screen_height

        if screen_ratio > image_ratio:
            new_height = screen_height
            new_width = int(new_height * image_ratio)
        else:
            new_width = screen_width
            new_height = int(new_width / image_ratio)

        return pygame.transform.smoothscale(image, (new_width, new_height))

    def scale_piece_img(self, image):
        image_width, image_height = image.get_size()
        radius = self.height / self.initial_height
        return pygame.transform.smoothscale(
            image, (int(image_width * radius / 11), int(image_height * radius / 11))
        )

    def handle_resize(self, width, height):
        self.width = width
        self.height = height
        self.background_image = self.scale_background_image(
            self.bg_initial_image, width, height
        )
        self.pos_list = [
            (
                int(x * height / self.initial_height),
                int(y * height / self.initial_height),
            )
            for x, y in self.initial_pos_list
        ]
        blue_piece_image = self.scale_piece_img(self.blue_piece_initial_image)
        red_piece_image = self.scale_piece_img(self.red_piece_initial_image)
        green_piece_image = self.scale_piece_img(self.green_piece_initial_image)
        yellow_piece_image = self.scale_piece_img(self.yellow_piece_initial_image)

        self.piece_image = {
            "green": green_piece_image,
            "red": red_piece_image,
            "blue": blue_piece_image,
            "yellow": yellow_piece_image,
        }

    def reset_game(self):
        self.already_rolled = False
        self.current_player = "green"
        self.dice_value = 0
        self.pieces = {
            "green": [0, 1, 2, 3],
            "red": [4, 5, 6, 7],
            "blue": [8, 9, 10, 11],
            "yellow": [12, 13, 14, 15],
        }
        self.positions = {i: None for i in range(96)}
        for color, indices in self.airports_index.items():
            for index in indices:
                self.positions[index] = [color, 1]
        self.winner = None

    def roll_dice(self):
        self.dice_value = random.randint(1, 6)
        self.already_rolled = True
        return self.dice_value

    def move_piece(self, piece_index):
        # 判断是否在机场
        if piece_index in self.airports_index[self.current_player]:
            if self.dice_value > 0:
                self.pieces[self.current_player].remove(piece_index)
                waiting_area = self.paths[self.current_player][0]
                self.pieces[self.current_player].append(waiting_area)
                # 判断待起飞区域是否有其他棋子
                if self.positions[waiting_area]:
                    # print(self.positions[waiting_area])
                    self.positions[waiting_area][1] += 1
                else:
                    self.positions[waiting_area] = [self.current_player, 1]
            else:
                pass
        else:
            # 如果在路径上
            # 获取当前棋子在路径上的位置
            current_index = self.paths[self.current_player].index(piece_index)
            print(current_index)
            new_index = current_index + self.dice_value
            # 判断是否超出路径
            if new_index >= len(self.paths[self.current_player]):
                # 超出路径的步数会倒退走
                new_index = 2 * len(self.paths[self.current_player]) - new_index
            new_position = self.paths[self.current_player][new_index]
            # 判断目标位置是否有其他棋子
            if self.positions[new_position]:
                # 判断是否是自己的棋子
                if self.positions[new_position][0] == self.current_player:
                    self.positions[new_position][1] += 1
                else:
                    # 把对方的棋子送回等待区
                    opponent = self.positions[new_position]
                    self.positions[new_position] = [self.current_player, 1]
                    for _ in range(opponent[1]):
                        self.pieces[opponent[0]].remove(new_position)
                        self.pieces[opponent[0]].append(self.paths[opponent[0]][0])
            else:
                self.positions[new_position] = [self.current_player, 1]
            # 原位置有一颗棋子
            if self.positions[piece_index][1] == 1:
                self.positions[piece_index] = None
            else:
                self.positions[piece_index][1] -= 1

            self.pieces[self.current_player].remove(piece_index)
            self.pieces[self.current_player].append(new_position)

        self.already_rolled = False

        # 检查是否获胜
        if all(
            self.positions[piece] == len(self.paths[self.current_player]) - 1
            for piece in self.pieces[self.current_player]
        ):
            self.winner = self.current_player

        # 切换玩家
        self.current_player = {
            "green": "red",
            "red": "blue",
            "blue": "yellow",
            "yellow": "green",
        }[self.current_player]

        return True

    def handle_click(self, mouse_pos):
        if self.winner:
            return

        if not self.already_rolled:
            dice_rect = self.get_dice_rect()
            if dice_rect.collidepoint(mouse_pos):
                self.roll_dice()
            return

        for piece_index in self.pieces[self.current_player]:
            piece_rect = self.get_piece_rect(piece_index)
            if piece_rect.collidepoint(mouse_pos):
                if self.move_piece(piece_index):
                    break
        print(self.positions)
        print(self.pieces)

    def get_piece_rect(self, piece_index):
        piece_image = self.piece_image[self.current_player]
        piece_rect = piece_image.get_rect()
        piece_rect.center = self.pos_list[piece_index]
        return piece_rect

    def get_dice_rect(self):
        dice_surface = self.id_font.render(f"掷骰子", True, (0, 0, 0))
        dice_rect = dice_surface.get_rect(bottomright=(self.width - 10, 100))
        return dice_rect

    def render(self):
        # 绘制飞行棋背景
        self.screen.fill("#9ed4f3")
        self.screen.blit(self.background_image, (0, 0))

        # 绘制棋子
        for player, pieces in self.pieces.items():
            for piece_index in pieces:
                piece_image = self.piece_image[player]
                piece_rect = self.get_piece_rect(piece_index)
                self.screen.blit(piece_image, piece_rect)

        # 绘制角标，用于叠棋
        for pos, piece in self.positions.items():
            if piece:
                _, count = piece
                if count > 1:
                    number_surface = self.id_font.render(str(count), True, (0, 0, 0))
                    number_rect = number_surface.get_rect(bottomleft=self.pos_list[pos])
                    self.screen.blit(number_surface, number_rect)

        # 绘制编号
        for idx, pos in enumerate(self.pos_list):
            number_surface = self.id_font.render(str(idx), True, (0, 0, 0))
            number_rect = number_surface.get_rect(center=pos)
            self.screen.blit(number_surface, number_rect)

        # 显示当前玩家和骰子值
        player_surface = self.id_font.render(
            f"当前玩家: {self.current_player}", True, (0, 0, 0)
        )
        player_rect = player_surface.get_rect(bottomright=(self.width - 10, 30))
        self.screen.blit(player_surface, player_rect)

        dice_surface = self.id_font.render(
            f"骰子值: {self.dice_value}", True, (0, 0, 0)
        )
        dice_rect = dice_surface.get_rect(bottomright=(self.width - 10, 60))
        self.screen.blit(dice_surface, dice_rect)

        # 显示掷骰子按钮
        dice_button_surface = self.id_font.render(f"掷骰子", True, (0, 0, 0))
        dice_button_rect = self.get_dice_rect()
        self.screen.blit(dice_button_surface, dice_button_rect)

        # 显示提示信息
        if self.already_rolled:
            hint_surface = self.id_font.render(f"←请选择棋子", True, (255, 0, 0))
        else:
            hint_surface = self.id_font.render(f"请先掷骰子↑", True, (255, 0, 0))
        hint_rect = hint_surface.get_rect(
            topright=(self.width - 10, dice_button_rect.bottom + 10)
        )
        self.screen.blit(hint_surface, hint_rect)

        # 显示胜利者
        if self.winner:
            winner_surface = self.id_font.render(
                f"{self.winner} 获胜", True, (255, 0, 0)
            )
            winner_rect = winner_surface.get_rect(
                center=(self.width / 2, self.height / 2)
            )
            self.screen.blit(winner_surface, winner_rect)
