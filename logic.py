import pyautogui
import cv2

import global_variables

from classification import capture_board
from classification import crop_board
from classification import classify_board

classification_templates = {
    "1": cv2.cvtColor(cv2.imread("assets/1.png"), cv2.COLOR_BGR2RGB),
    "2": cv2.cvtColor(cv2.imread("assets/2.png"), cv2.COLOR_BGR2RGB),
    "3": cv2.cvtColor(cv2.imread("assets/3.png"), cv2.COLOR_BGR2RGB),
    "4": cv2.cvtColor(cv2.imread("assets/4.png"), cv2.COLOR_BGR2RGB),
    "5": cv2.cvtColor(cv2.imread("assets/5.png"), cv2.COLOR_BGR2RGB),
    "6": cv2.cvtColor(cv2.imread("assets/6.png"), cv2.COLOR_BGR2RGB),
    "7": cv2.cvtColor(cv2.imread("assets/7.png"), cv2.COLOR_BGR2RGB),
    "8": cv2.cvtColor(cv2.imread("assets/8.png"), cv2.COLOR_BGR2RGB),
    "empty": cv2.cvtColor(cv2.imread("assets/empty.png"), cv2.COLOR_BGR2RGB),
    "hidden": cv2.cvtColor(cv2.imread("assets/hidden.png"), cv2.COLOR_BGR2RGB),
    "flag": cv2.cvtColor(cv2.imread("assets/flag.png"), cv2.COLOR_BGR2RGB)
}

''' Helper Functions '''
# Function: Return True if the tile is a number
def is_number_tile(tile):
    return tile in {"1", "2", "3", "4", "5", "6", "7", "8"}

# Function: Check for board boundaries
def in_bounds(x, y, rows, cols):
    return 0 <= x < cols and 0 <= y < rows

# Function: Get coordinates of all valid neighbours
def get_neighbors(x, y, rows, cols):
    neighbors = []
    # Loop through all relative positions around the current tile
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]: 
            if dx == 0 and dy == 0:
                continue  # Skip self
            nx, ny = x + dx, y + dy # Calculates neighbour coordinates
            if in_bounds(nx,ny,rows,cols):
                neighbors.append((nx, ny))
    return neighbors

# Function: Counts the number of hidden nieghbours
def count_hidden_neighbors(x, y, board):
    hidden_count = 0
    for nx, ny in get_neighbors(x, y, len(board), len(board[0])): # Get coordinates of neighbours
        if board[ny][nx] == "hidden": # If the neighbour is a hidden tile
            hidden_count += 1
    return hidden_count

# Function: Counts the number of flagged neighbours
def count_flagged_neighbors(x, y, board):
    flag_count = 0
    for nx, ny in get_neighbors(x, y, len(board), len(board[0])):
        if board[ny][nx] == "flag": # If the neighbour is a flag tile
            flag_count += 1
    return flag_count

# Function: Return coordinates of all hidden neighbours
def get_hidden_neighbors(x, y, board):
    hidden = []
    for nx, ny in get_neighbors(x, y, len(board), len(board[0])):
        if board[ny][nx] == "hidden":
            hidden.append((nx, ny))
    return hidden

# Function: Convert matrix coordinates to on screen coordinates
def convert_coords(x,y):
    screen_x = global_variables.TOP_LEFT_X + x * global_variables.TILE_SIZE + global_variables.TILE_SIZE // 2
    screen_y = global_variables.TOP_LEFT_Y + y * global_variables.TILE_SIZE + global_variables.TILE_SIZE // 2
    return screen_x, screen_y


''' Mouse Movements '''
# Function: Click Tile
def click_tile(x, y):
    screen_x, screen_y = convert_coords(x, y)
    pyautogui.moveTo(screen_x, screen_y)
    pyautogui.click()  # Left click

# Function: Flag Tile
def flag_tile(x, y):
    screen_x, screen_y = convert_coords(x, y)
    pyautogui.moveTo(screen_x, screen_y)
    pyautogui.rightClick()  # Right click

''' Problem Solving Logic '''

# Automation:
ah = 5
while ah != 0:
    board_image = capture_board() #Screenshot board
    tiles = crop_board(board_image) #Crop Tiles
    board_state = classify_board(tiles, classification_templates) #Classify Board

    for y, row in enumerate(board_state):         # y = row index
        for x, tile in enumerate(row):            # x = column index
            if is_number_tile(tile):
                if count_hidden_neighbors(x, y, board_state) + count_flagged_neighbors(x, y, board_state) == int(tile):
                    for nx, ny in get_hidden_neighbors(x, y, board_state):
                        flag_tile(nx, ny)

                elif count_flagged_neighbors(x, y, board_state) == int(tile):
                    for nx, ny in get_hidden_neighbors(x, y, board_state):
                        click_tile(nx, ny)
    ah = ah -1