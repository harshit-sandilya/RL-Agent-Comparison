import gymnasium as gym
from gymnasium import spaces
import numpy as np
from minesweeper import create, move, check_over


def fancy_print(grid, action):
    row_idx, col_idx = action

    for i, row in enumerate(grid):
        row_str = ""
        for j, value in enumerate(row):
            if i == row_idx and j == col_idx:
                row_str += f"**+{value}**" if value >= 0 else f"**{value}**"
            else:
                row_str += f"  +{value}  " if value >= 0 else f"  {value}  "
        print(row_str.strip())


class Env(gym.Env):
    def __init__(self, n_grid, n_mines):
        super().__init__()
        self.n = n_grid
        self.mines = n_mines
        self.dict = [(i, j) for i in range(n_grid) for j in range(n_grid)]
        self.action_space = spaces.Discrete(n_grid * n_grid)
        # self.action_space = spaces.MultiDiscrete([n_grid, n_grid])
        low = np.full((n_grid, n_grid), -1, dtype=np.int32)
        high = np.full((n_grid, n_grid), 10, dtype=np.int32)
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.int32)

    def _visited(self, action):
        return self.view[action[0]][action[1]] != -1

    def reset(self, seed=None):
        super().reset(seed=seed)
        self.grid, self.view = create(self.n, self.mines)
        return self.grid, {}

    def step(self, action):
        reward, over = self.calc_reward(self.dict[action])
        # reward, over = self.calc_reward(action)
        done = over
        info = {}
        return self.grid, reward, done, False, info

    def calc_reward(self, action):
        print("++++++++++++++++++++++++++BEFORE+++++++++++++++++++++++++++++++")
        fancy_print(self.grid, action)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        fancy_print(self.view, action)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(action)
        over = move(action, self.grid, self.view)
        print("++++++++++++++++++++++++++AFTER++++++++++++++++++++++++++++++++")
        fancy_print(self.grid, action)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        fancy_print(self.view, action)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        if self._visited(action):
            return -10, False
        if over:
            return -1, True
        if check_over(self.view, self.mines):
            return 2, True
        return 1, False
