import random


def set_mines(n, mines_no, numbers):
    count = 0
    while count < mines_no:
        val = random.randint(0, n * n - 1)
        r = val // n
        col = val % n
        if numbers[r][col] != -1:
            count = count + 1
            numbers[r][col] = -1


def neighbours(r, col, vis, numbers, mine_values, n):

    # If the cell already not visited
    if [r, col] not in vis:

        # Mark the cell visited
        vis.append([r, col])

        # If the cell is zero-valued
        if numbers[r][col] == 0:

            # Display it to the user
            mine_values[r][col] = numbers[r][col]

            # Recursive calls for the neighbouring cells
            if r > 0:
                neighbours(r - 1, col, vis, numbers, mine_values, n)
            if r < n - 1:
                neighbours(r + 1, col, vis, numbers, mine_values, n)
            if col > 0:
                neighbours(r, col - 1, vis, numbers, mine_values, n)
            if col < n - 1:
                neighbours(r, col + 1, vis, numbers, mine_values, n)
            if r > 0 and col > 0:
                neighbours(r - 1, col - 1, vis, numbers, mine_values, n)
            if r > 0 and col < n - 1:
                neighbours(r - 1, col + 1, vis, numbers, mine_values, n)
            if r < n - 1 and col > 0:
                neighbours(r + 1, col - 1, vis, numbers, mine_values, n)
            if r < n - 1 and col < n - 1:
                neighbours(r + 1, col + 1, vis, numbers, mine_values, n)

        # If the cell is not zero-valued
        if numbers[r][col] != 0:
            mine_values[r][col] = numbers[r][col]


def set_values(n, numbers):
    for r in range(n):
        for col in range(n):
            if numbers[r][col] == -1:
                continue

            # Check up
            if r > 0 and numbers[r - 1][col] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check down
            if r < n - 1 and numbers[r + 1][col] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check left
            if col > 0 and numbers[r][col - 1] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check right
            if col < n - 1 and numbers[r][col + 1] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check top-left
            if r > 0 and col > 0 and numbers[r - 1][col - 1] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check top-right
            if r > 0 and col < n - 1 and numbers[r - 1][col + 1] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check below-left
            if r < n - 1 and col > 0 and numbers[r + 1][col - 1] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check below-right
            if r < n - 1 and col < n - 1 and numbers[r + 1][col + 1] == -1:
                numbers[r][col] = numbers[r][col] + 1


def check_over(mine_values, mines_no):
    count = 0
    n = len(mine_values)

    for r in range(n):
        for col in range(n):
            if mine_values[r][col] != -1:
                count = count + 1

    if count == n * n - mines_no:
        return True
    else:
        return False


def create(n_grid, n_mines):
    grid = [[0 for y in range(n_grid)] for x in range(n_grid)]
    view = [[-1 for y in range(n_grid)] for x in range(n_grid)]

    set_mines(n_grid, n_mines, grid)
    set_values(n_grid, grid)

    return grid, view


def move(action, grid, view):
    row = action[0]
    col = action[1]

    if grid[row][col] == -1:
        return True
    elif grid[row][col] == 0:
        view[row][col] = 0
        neighbours(row, col, [], grid, view, len(grid))
        return False
    else:
        view[row][col] = grid[row][col]
        return False
