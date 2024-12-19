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
    count = sum(cell != -2 and cell != -1 for row in mine_values for cell in row)
    return count == len(mine_values) * len(mine_values) - mines_no


def move(action, grid, view, queue):
    row, col = action
    queue.add((row, col))
    view[row][col] = grid[row][col]
    if grid[row][col] == -1:
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
            if grid[r][c] != -1:
                safe_cells.append((r, c))
            else:
                mine_cells.append((r, c))

    hidden_safe_cell = random.choice(safe_cells)
    hidden_mine_cell = random.choice(mine_cells)

    while count < solve_tiles:
        r = random.randint(0, n - 1)
        col = random.randint(0, n - 1)
        if (
            (r, col) not in queue
            and (r, col) != hidden_safe_cell
            and (r, col) != hidden_mine_cell
        ):
            queue.add((r, col))
            view[r][col] = grid[r][col]
            count += 1


def create(n_grid, n_mines, queue, index, show=True):
    grid = [[0] * n_grid for _ in range(n_grid)]
    view = [[-2] * n_grid for _ in range(n_grid)]

    set_mines(n_grid, n_mines, grid)
    set_values(n_grid, grid)

    if show:
        lst = list(range(n_grid * n_grid - 2, 0, -1))
        solve(grid, view, lst[index], queue)

    return grid, view
