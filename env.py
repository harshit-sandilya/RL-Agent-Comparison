import gymnasium as gym
from gymnasium import spaces
import numpy as np
from minesweeper import create, move, check_over, get_observation, mine_key, unknown_key


class Env(gym.Env):
    def __init__(self, n_grid, n_mines):
        super().__init__()
        self.n = n_grid
        self.mines = n_mines

        # self.dict = [(i, j) for i in range(n_grid) for j in range(n_grid)]
        # self.action_space = spaces.Discrete(n_grid * n_grid)
        self.action_space = spaces.MultiDiscrete([n_grid, n_grid])
        low = np.full(
            (n_grid, n_grid, 3), min(unknown_key, mine_key, 0), dtype=np.uint8
        )
        high = np.full(
            (n_grid, n_grid, 3), max(unknown_key, mine_key, 8), dtype=np.uint8
        )
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.uint8)

        self.queue = set()
        self.index = 0
        self.wonLast = False
        self.wonTwoLast = False
        self.reward = 0
        self.action = None

    def _update_index(self):
        if self.index == self.n * self.n - self.mines - 1:
            self.index = 0
        else:
            self.index = self.index + 1

    def _visited(self, action):
        return tuple(action) in self.queue

    def reset(self, seed=None):
        super().reset(seed=seed)
        self.queue = set()
        self.grid, self.view = create(self.n, self.mines, self.queue, self.index, True)
        if self.wonTwoLast:
            self._update_index()
            self.wonTwoLast = False
            self.wonLast = False
        return get_observation(self.view, self.action), {}

    def step(self, action):
        # reward, over = self.calc_reward(self.dict[action])
        reward, done = self.calc_reward(action)
        self.action = action
        self.reward = reward
        info = {}
        return get_observation(self.view, self.action), reward, done, False, info

    def render(self):
        print(self.view)

    def calc_reward(self, action):
        visited = self._visited(action)
        over = move(action, self.grid, self.view, self.queue)
        self.visited_same = 1 if visited else 0
        self.on_mine = 1 if self.grid[action[0]][action[1]] == mine_key else 0
        self.won_game = 1 if check_over(self.view, self.mines) else 0

        if self.action is not None and np.array_equal(action, self.action):
            return -100, False
        if visited:
            return -50, False
        if over:
            return -10, True
        if check_over(self.view, self.mines):
            if self.wonLast:
                self.wonTwoLast = True
            self.wonLast = True
            return 100, True
        return 50, False
