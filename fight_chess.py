import pygame


class FightChess:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.initial_width = width
        self.initial_height = height

        # 加载飞行棋背景图片
        self.background_initial_image = pygame.image.load("res/background.svg")
        self.background_image = self.scale_background_image(
            self.background_initial_image, width, height
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

        # 加载并缩放蓝棋子图片
        self.blue_piece_initial_image = pygame.image.load("res/蓝棋子.svg")
        self.blue_piece_image_initial_width, self.blue_piece_image_initial_height = (
            self.blue_piece_initial_image.get_size()
        )
        self.blue_piece_image = pygame.transform.smoothscale(
            self.blue_piece_initial_image,
            (
                self.blue_piece_image_initial_width // 11,
                self.blue_piece_image_initial_height // 11,
            ),
        )
        self.blue_piece_rect = self.blue_piece_image.get_rect()

        # 加载系统字体
        self.id_font = pygame.font.SysFont(
            "Microsoft YaHei", 24, True
        )  # 使用系统自带的微软雅黑字体

    def scale_background_image(self, image, screen_width, screen_height):
        image_width, image_height = image.get_size()
        image_ratio = image_width / image_height
        screen_ratio = screen_width / screen_height

        if screen_ratio > image_ratio:
            # Screen is wider than image
            new_height = screen_height
            new_width = int(new_height * image_ratio)
        else:
            # Screen is taller than image
            new_width = screen_width
            new_height = int(new_width / image_ratio)

        return pygame.transform.smoothscale(image, (new_width, new_height))

    def handle_resize(self, width, height):
        self.width = width
        self.height = height
        self.background_image = self.scale_background_image(
            self.background_initial_image, width, height
        )
        self.pos_list = [
            (
                int(x * height / self.initial_height),
                int(y * height / self.initial_height),
            )
            for x, y in self.initial_pos_list
        ]
        self.blue_piece_image = pygame.transform.smoothscale(
            self.blue_piece_initial_image,
            (
                self.blue_piece_image_initial_width
                // 11
                * height
                / self.initial_height,
                self.blue_piece_image_initial_height
                // 11
                * height
                / self.initial_height,
            ),
        )
        self.blue_piece_rect = self.blue_piece_image.get_rect()

    def render(self):
        # 绘制飞行棋背景
        self.screen.fill("#9ed4f3")
        self.screen.blit(self.background_image, (0, 0))

        # 绘制蓝棋子到每个坐标
        for pos in self.pos_list:
            piece_rect = self.blue_piece_rect.copy()
            piece_rect.center = pos
            self.screen.blit(self.blue_piece_image, piece_rect)

        # 绘制点击位置编号
        for idx, pos in enumerate(self.pos_list):
            number_surface = self.id_font.render(str(idx), True, (0, 0, 0))
            number_rect = number_surface.get_rect(center=pos)
            self.screen.blit(number_surface, number_rect)
