import cv2
import numpy as np

from screenshot import capture_board
from screenshot import crop_board

# Function: Tile Classifier
def match_tile(tile, templates):
    tile = tile.resize((15, 15))  # Resize to match template size
    tile = np.array(tile, dtype=np.uint8)

    best_label = None
    best_score = float('inf')  # Since lower is better for SQDIFF

    for label, template in templates.items():
        result = cv2.matchTemplate(tile, template, cv2.TM_SQDIFF_NORMED)
        score = result[0][0]

        if score < best_score:  # Lower is better
            best_score = score
            best_label = label

    return best_label, best_score

# Function: Turn classification output into matrix
def classify_board(tiles, templates):
    board_state = []
    for row in tiles:
        row_labels = []
        for tile in row:
            label, score = match_tile(tile, templates)
            row_labels.append(label)
        board_state.append(row_labels)
    return board_state

# Function: Print classification matrix
def print_board(board_state):
    for row in board_state:
        print(" ".join(row))


#Debugging
'''
# Saving the cropped tiles as pictures to debug
# def debug_save_tiles(tiles):
#     for row_idx, row in enumerate(tiles):
#         for col_idx, tile in enumerate(row):
#             tile.save(f"debug_tiles/tile_r{row_idx}_c{col_idx}.png")

# debug_save_tiles(tiles)
'''

'''
# Printing tile classification scores
# for row_idx, row in enumerate(tiles):
#     for col_idx, tile in enumerate(row):
#         label = match_tile(tile, classification_templates)
#         print(f"Tile at ({row_idx}, {col_idx}): {label}")
'''
        
