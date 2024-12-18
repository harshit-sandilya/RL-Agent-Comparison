import random


def set_mines(n, mines_no, numbers):
    count = 0
    while count < mines_no:
        val = random.randint(0, n * n - 1)
        r = val // n
        col = val % n
        if numbers[r][col] != -1:
            count += 1
            numbers[r][col] = -1


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
            if numbers[r][col] == -1:
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
                if 0 <= nr < n and 0 <= nc < n and numbers[nr][nc] == -1:
                    numbers[r][col] += 1


def check_over(mine_values, mines_no):
    count = sum(cell != -1 for row in mine_values for cell in row)
    return count == len(mine_values) * len(mine_values) - mines_no


def move(action, grid, view):
    row, col = action
    if grid[row][col] == -1:
        return True
    elif grid[row][col] == 0:
        view[row][col] = 0
        neighbours(row, col, set(), grid, view, len(grid))
        return False
    else:
        view[row][col] = grid[row][col]
        return False


def solve(grid, view, solve_tiles):
    n = len(grid)
    count = 0
    while count < solve_tiles:
        r = random.randint(0, n - 1)
        col = random.randint(0, n - 1)
        if view[r][col] == -1:
            move([r, col], grid, view)
            count += 1


def create(n_grid, n_mines, show=True):
    grid = [[0] * n_grid for _ in range(n_grid)]
    view = [[-1] * n_grid for _ in range(n_grid)]

    set_mines(n_grid, n_mines, grid)
    set_values(n_grid, grid)

    if show:
        solve_fraction = random.randint(0, n_grid * n_grid - 1)
        solve(grid, view, solve_fraction)

    return grid, view
