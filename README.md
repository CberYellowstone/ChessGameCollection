# 棋类游戏合集

这是一个使用 Pygame 实现的棋类游戏合集，包括以下几种棋类游戏：
- 五子棋
- 中国象棋
- 井字棋
- 飞行棋


## 安装和运行

1. 克隆仓库到本地：
    ```sh
    git clone https://github.com/yourusername/ChessGameCollection.git
    cd ChessGameCollection
    ```

2. 安装依赖：
    ```sh
    pip install pygame numpy
    ```

3. 运行游戏：
    ```sh
    python main.py
    ```

## 游戏介绍

### 五子棋

五子棋的目标是将五个相同颜色的棋子连成一线。游戏逻辑在 [gomoku.py](gomoku.py) 中实现。

### 中国象棋

中国象棋是一种传统的棋类游戏，目标是将对方的将/帅将死。游戏逻辑在 [chinese_chess.py](chinese_chess.py) 中实现。

### 井字棋

井字棋的目标是将三个相同的符号连成一线。游戏逻辑在 [tic_tac_toe.py](tic_tac_toe.py) 中实现。

### 飞行棋

飞行棋是一种多人棋类游戏，目标是将所有棋子移动到终点。游戏逻辑在 [fight_chess.py](fight_chess.py) 中实现。

## 控制

- 使用鼠标点击棋盘进行操作。
- 在主菜单中点击游戏名称进入相应的游戏。
- 在游戏中点击“返回主页面”按钮返回主菜单。

## 贡献

欢迎提交问题和拉取请求来改进此项目。

## 许可证

此项目使用 [AGPLv3](LICENSE) 许可证。