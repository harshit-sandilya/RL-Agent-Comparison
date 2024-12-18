import gymnasium as gym
from gymnasium import spaces
import numpy as np
from minesweeper import create, move, check_over


def fancy_print(grid, action):
    row_idx, col_idx = action

    for i, row in enumerate(grid):
        row_str = ""
        for j, value in enumerate(row):
            if grid[i][j] == -1:
                row_str += "   X  "
            elif grid[i][j] == -2:
                row_str += "   U  "
            elif i == row_idx and j == col_idx:
                row_str += f"**+{value}**" if value >= 0 else f"**{value}**"
            else:
                row_str += f"  +{value}  " if value >= 0 else f"  {value}  "
        print(row_str)


class Env(gym.Env):
    def __init__(self, n_grid, n_mines, debug=True):
        super().__init__()
        self.n = n_grid
        self.mines = n_mines
        self.debug = debug
        self.dict = [(i, j) for i in range(n_grid) for j in range(n_grid)]
        self.action_space = spaces.Discrete(n_grid * n_grid)
        # self.action_space = spaces.MultiDiscrete([n_grid, n_grid])
        low = np.full((n_grid, n_grid), -2, dtype=np.int32)
        high = np.full((n_grid, n_grid), 8, dtype=np.int32)
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.int32)
        self.queue = set()

    def _visited(self, action):
        return action in self.queue

    def reset(self, seed=None):
        super().reset(seed=seed)
        self.queue = set()
        self.grid, self.view = create(self.n, self.mines, self.queue, True)
        return np.array(self.view), {}

    def step(self, action):
        reward, over = self.calc_reward(self.dict[action])
        # reward, over = self.calc_reward(action)
        if self.debug:
            print("++++++++++++++++++++++++++REWARD+++++++++++++++++++++++++++++++")
            print(reward)
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        done = over
        info = {}
        return np.array(self.view), reward, done, False, info

    def calc_reward(self, action):
        visited = self._visited(action)
        if self.debug:
            print("++++++++++++++++++++++++++BEFORE(ACTUAL)+++++++++++++++++++++++")
            fancy_print(self.grid, action)
            print("+++++++++++++++++++++++++++VIEW++++++++++++++++++++++++++++++++")
            fancy_print(self.view, action)
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print(action)
            print("Visited", visited)

        over = move(action, self.grid, self.view, self.queue)

        if self.debug:
            print("++++++++++++++++++++++++++AFTER(ACTUAL)++++++++++++++++++++++++")
            fancy_print(self.grid, action)
            print("+++++++++++++++++++++++++++VIEW++++++++++++++++++++++++++++++++")
            fancy_print(self.view, action)
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

        if visited:
            return -1, False
        if over:
            return -1, False
        if check_over(self.view, self.mines):
            return 2, True
        return 1, False
