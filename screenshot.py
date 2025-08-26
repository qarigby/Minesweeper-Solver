import pyautogui
import mss
from PIL import Image
import global_variables

#Function: Capture the game board (minesweeper tiles)
def capture_board():
    width = global_variables.COLS * global_variables.TILE_SIZE
    height = global_variables.ROWS * global_variables.TILE_SIZE
    game_board = {"left": global_variables.TOP_LEFT_X, "top": global_variables.TOP_LEFT_Y, "width": width, "height": height}

    with mss.mss() as sct:
        screenshot = sct.grab(game_board)
        image = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        return image
    
# Debug: Test that the game board is captured correctly
'''
img = capture_board()
img.save("game_board_test.png")
'''


# Function: Board Cropping
def crop_board(board_img):
    tiles = []
    for row in range(global_variables.ROWS):
        row_tiles = []
        for col in range(global_variables.COLS):
            left = col * global_variables.TILE_SIZE + 1
            top = row * global_variables.TILE_SIZE + 1
            right = (col + 1) * global_variables.TILE_SIZE - 1
            bottom = (row + 1) * global_variables.TILE_SIZE - 1

            tile = board_img.crop((left, top, right, bottom))
            row_tiles.append(tile)
        tiles.append(row_tiles)
    return tiles

