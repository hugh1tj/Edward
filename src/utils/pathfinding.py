import math
import heapq
import csv

#import player
from . import spritesheet
from ..data import local_data


class Cell:
    def __init__(self):
        # Parent cell's row index
        self.parent_i = 0
        # Parent cell's column index
        self.parent_j = 0
        # Total cost of the cell (g + h)
        self.f = float('inf')
        # Cost from start to this cell
        self.g = float('inf')
        # Heuristic cost from this cell to destination
        self.h = 0


# Define the size of the grid
# ROW = 62
ROW = 60
COL = 82


# Check if a cell is valid (within the grid)


def is_valid(row, col):
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)


# Check if a cell is unblocked


def is_unblocked(grid, row, col):

    #print ('row', row, 'col', col)
    # print('example',grid[59][81] )
    # print('lenrow',len(grid[row]))
    x = int(grid[row][col])

    # if (x == -1) or (x == 3) or (x == 5) or (x == 6) or (x == 7) or(x == 8)  : # these are the values that shows unblocked
    if (x == 3) or (x == 5) or (x == 6) or (x == 7) or (x == 8):  # these are the values that shows unblocked
        i = True
        # print ('says', row,col,grid[row][col],True)
    else:
        i = False  # blocked

    return i


# Check if a cell is the destination


def is_destination(row, col, dest):
    return row == dest[1] and col == dest[0]  # rows before columns


# Calculate the heuristic value of a cell (Euclidean distance to destination)


def calculate_h_value(row, col, dest):
    return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5


# Trace the path from source to destination


def trace_path(cell_details, dest):
    # print("The Path is ")
    path = []
    row = dest[1]  # row before col
    col = dest[0]

    # Trace the path from destination to source using parent cells
    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        path.append((row, col))
        temp_row = cell_details[row][col].parent_i
        temp_col = cell_details[row][col].parent_j
        row = temp_row
        col = temp_col

    # Add the source cell to the path
    path.append((row, col))
    # Reverse the path to get the path from source to destination
    path.reverse()

    # Print the path
    # for i in path:
    # print("->", i, end=" ")
    # print()
    local_data.path_local = path


# Implement the A* search algorithm


def a_star_search(grid, src, dest):
    # Check if the source and destination are valid
    if not is_valid(src[1], src[0]) or not is_valid(dest[1], dest[0]):  # rows before colums
        print('invalid at', src[1], src[0], dest[1], dest[0])
        print("Source or destination is invalid")
        return

    # Check if the source and destination are unblocked
    x = is_unblocked(grid, src[1], src[0])
    y = is_unblocked(grid, dest[1], dest[0])  # rows before columns
    # print('xy', x, y)

    if not is_unblocked(grid, src[1], src[0]) or not is_unblocked(grid, dest[1], dest[0]):  # rows before columns

        print("Source or the destination is blocked")
        return

    # Check if we are already at the destination
    if is_destination(src[1], src[0], dest):  # rows before columns
        print("We are already at the destination")
        return

    # Initialize the closed list (visited cells)
    closed_list = [[False for _ in range(COL)] for _ in range(ROW)]
    # Initialize the details of each cell
    cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

    # Initialize the start cell details
    i = src[1]  # rows before columns
    j = src[0]
    cell_details[i][j].f = 0
    cell_details[i][j].g = 0
    cell_details[i][j].h = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    # Initialize the open list (cells to be visited) with the start cell
    open_list = []
    heapq.heappush(open_list, (0.0, i, j))

    # Initialize the flag for whether destination is found
    found_dest = False

    # Main loop of A* search algorithm
    while len(open_list) > 0:
        # Pop the cell with the smallest f value from the open list
        p = heapq.heappop(open_list)

        # Mark the cell as visited
        i = p[1]
        j = p[2]
        closed_list[i][j] = True

        # For each direction, check the successors
        #directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0) ] # to avoid diagonals
        for dir in directions:
            # print ('dir',dir[0],dir[1])
            # print('i',i,'j',j,'grid',grid[i][j])

            new_i = i + dir[0]
            new_j = j + dir[1]
            if (abs(dir[0]) == abs(dir[1])):  # trevors addition
                diagonal = 'True'
                weight = 1.4  # longer distance to go diagonal
            else:
                diagonal = 'False'
                weight = 1.0
            # if (int(grid[i][j]) == 3):
            # print ( 'calm')

            if (int(grid[i][j]) == 5) and dir[0] > 0:  # going south in a northwester
                # print('dir', dir[0], 'going south in a northsouther')
                weight = 0.1 * weight
            if (int(grid[i][j]) == 5) and dir[0] < 0:  # going north in a northwester
                # print('dir', dir[0], 'going north in a northsouther')
                weight = 10 * weight
            if (int(grid[i][j]) == 6) and dir[0] > 0:  # going south in gulf
                # print('dir', dir[0], 'going south in a gulf stream')
                weight = 10 * weight
            if (int(grid[i][j] == 6)) and dir[0] < 0:  # north in gulf
                # print('dir', dir, 'going north in gulf stream')
                weight = 0.001 * weight
            if (int(grid[i][j]) == 7) and dir[1] > 0:  # 
                # print('dir', dir[1], 'going east in a east west')
                weight = 0.1 * weight
            if (int(grid[i][j]) == 7) and dir[1] < 0:  # 
                # print('dir', dir[1], 'going west in east west')
                weight = 10 * weight
            if (int(grid[i][j]) == 8) and dir[1] > 0:  # 
                # print('dir', dir[1], 'going east in a west east')
                weight = 10 * weight

            if (grid[i][j] == 8) and dir[1] < 0:  # 
                # print('dir', dir[1], 'going west in a west east')
                weight = 0.1 * weight
            # If the successor is valid, unblocked, and not visited
            # print ('outgoing weight',weight)
            if is_valid(new_i, new_j) and is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
                # If the successor is the destination
                if is_destination(new_i, new_j, dest):
                    # Set the parent of the destination cell
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    # print("The destination cell is found")
                    # Trace and print the path from source to destination
                    trace_path(cell_details, dest)
                    found_dest = True
                    return
                else:
                    # Calculate the new f, g, and h values
                    # g_new = cell_details[i][j].g + 1.0
                    g_new = cell_details[i][j].g + weight

                    # h_new = calculate_h_value(new_i, new_j, dest)

                    # f_new = g_new + h_new
                    f_new = g_new  # reduces to dijkstra
                    # If the cell is not in the open list or the new f value is smaller
                    if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                        # Add the cell to the open list
                        heapq.heappush(open_list, (f_new, new_i, new_j))
                        # Update the cell details
                        cell_details[new_i][new_j].f = f_new
                        cell_details[new_i][new_j].g = g_new
                        # cell_details[new_i][new_j].h = h_new # reducint to dijkstra
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j

    # If the destination is not found after visiting all cells
    if not found_dest:
        print("Failed to find the destination cell")


# Driver Code

def main_astar(srcx, srcy, destx, desty):
    # Define the grid (1 for unblocked, 0 for blocked)
    grid = local_data.mapx
    #print ('grid in astar',grid)
    # print ('lengrid',len(grid))
    # print (' cell', grid[59][81]) # grid has rows first cols second
    src = [srcx, srcy]
    dest = [destx, desty]  # not cols before ro

    a_star_search(grid, src, dest)

