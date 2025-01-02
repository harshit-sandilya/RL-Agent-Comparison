import random
import numpy as np

mine_key = 12
unknown_key = 16


def set_mines(n, mines_no, numbers):
    count = 0
    while count < mines_no:
        val = random.randint(0, n * n - 1)
        r = val // n
        col = val % n
        if numbers[r][col] != mine_key:
            count += 1
            numbers[r][col] = mine_key


def neighbours(r, col, vis, numbers, mine_values, n):
    if (r, col) not in vis:
        vis.add((r, col))
        if numbers[r][col] == 0:
            mine_values[r][col] = numbers[r][col]
            for dr, dc in [
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1),
                (-1, -1),
                (-1, 1),
                (1, -1),
                (1, 1),
            ]:
                nr, nc = r + dr, col + dc
                if 0 <= nr < n and 0 <= nc < n:
                    neighbours(nr, nc, vis, numbers, mine_values, n)
        else:
            mine_values[r][col] = numbers[r][col]


def set_values(n, numbers):
    for r in range(n):
        for col in range(n):
            if numbers[r][col] == mine_key:
                continue
            for dr, dc in [
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1),
                (-1, -1),
                (-1, 1),
                (1, -1),
                (1, 1),
            ]:
                nr, nc = r + dr, col + dc
                if 0 <= nr < n and 0 <= nc < n and numbers[nr][nc] == mine_key:
                    numbers[r][col] += 1


def check_over(mine_values, mines_no):
    count = sum(cell == unknown_key for row in mine_values for cell in row)
    return count == mines_no


def move(action, grid, view, queue):
    row, col = action
    queue.add((row, col))
    view[row][col] = grid[row][col]
    if grid[row][col] == mine_key:
        return True
    elif grid[row][col] == 0:
        neighbours(row, col, queue, grid, view, len(grid))
        return False
    else:
        return False


def solve(grid, view, solve_tiles, queue):
    n = len(grid)
    count = 0
    safe_cells = []
    mine_cells = []

    for r in range(n):
        for c in range(n):
            if grid[r][c] != mine_key:
                safe_cells.append((r, c))
            else:
                mine_cells.append((r, c))

    hidden_safe_cell = random.choice(safe_cells)

    while count < solve_tiles:
        r = random.randint(0, n - 1)
        col = random.randint(0, n - 1)
        if (
            (r, col) not in queue
            and (r, col) != hidden_safe_cell
            and (r, col) not in mine_cells
        ):
            queue.add((r, col))
            view[r][col] = grid[r][col]
            count += 1


def create(n_grid, n_mines, queue, index, show=True):
    grid = [[0] * n_grid for _ in range(n_grid)]
    view = [[unknown_key] * n_grid for _ in range(n_grid)]

    set_mines(n_grid, n_mines, grid)
    set_values(n_grid, grid)

    if show:
        lst = list(range(n_grid * n_grid - n_mines - 1, 0, -1))
        solve(grid, view, lst[index], queue)

    return grid, view


def get_observation(view, action):
    grid = [[0] * len(view) for _ in range(len(view))]
    action_matrix = [[0] * len(view) for _ in range(len(view))]
    for i in range(len(view)):
        for j in range(len(view)):
            if view[i][j] == unknown_key:
                grid[i][j] = 1
            else:
                grid[i][j] = 0
            if np.array_equal((i, j), action):
                action_matrix[i][j] = 1
    observation = []
    observation.append(grid)
    observation.append(view)
    observation.append(action_matrix)
    observation = np.array(observation, dtype=np.uint8)
    observation = np.transpose(observation, (1, 2, 0))
    return observation
