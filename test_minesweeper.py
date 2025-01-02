from minesweeper import create, move, check_over, get_observation


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


def _visited(queue, action):
    return tuple(action) in queue


queue = set()
grid, view = create(8, 10, queue, 0, True)

fancy_print(view, (0, 0))
print(sorted(queue))
print(get_observation(view).shape)

row, col = input("Enter row and column: ").split()
row, col = int(row), int(col)
if _visited(queue, (row, col)):
    print("Already visited this cell")
move((row, col), grid, view, queue)
fancy_print(view, (row, col))
print(sorted(queue))

print(check_over(view, 10))
