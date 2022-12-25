import random
import pygame

# The size of the map (in tiles)
MAP_WIDTH = 100
MAP_HEIGHT = 100

# The size of each tile (in pixels)
TILE_SIZE = 5

# The possible materials for each tile
AIR = 0
WALL = 1
WATER = 2
SAND = 3

# The delay before a tile can be updated again (in simulation steps)
UPDATE_DELAY = 0

# The array that stores the map
map_array = [[AIR for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

# The array that stores the update delays for each tile
update_delay_array = [[0 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

# Initialize Pygame
pygame.init()

# Set the window size and title
screen = pygame.display.set_mode((MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE))
pygame.display.set_caption('Falling Sand')

# Initialize the map with some walls and water
# for i in range(50):
#     map_array[i][0] = WALL

map_array[50][0] = WATER

# Set the colors for each material
colors = {
    AIR: (80, 80, 80),
    WALL: (0, 0, 0),
    WATER: (10, 10, 240),
    SAND: (225, 215, 40),
}

# The current material to place on the map
current_material = WATER
# The main simulation loop
running = True
mouse_down = False
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False
        elif event.type == pygame.KEYDOWN:
            # Change the current material based on the key pressed
            if event.key == pygame.K_1:
                current_material = WATER
            elif event.key == pygame.K_2:
                current_material = SAND
            elif event.key == pygame.K_3:
                current_material = WALL
    if mouse_down:
        # Get the mouse position in tiles
        mouse_x, mouse_y = pygame.mouse.get_pos()
        tile_x, tile_y = mouse_x // TILE_SIZE, mouse_y // TILE_SIZE
        # Place the current material on the map
        map_array[tile_x][tile_y] = current_material
    # Shuffle the order in which the tiles are processed
    tiles = [(i, j) for i in range(MAP_WIDTH) for j in range(MAP_HEIGHT)]
    random.shuffle(tiles)

    # Loop through all the tiles
    for i, j in tiles:
        # Skip tiles that are not affected by gravity
        if map_array[i][j] not in (WATER, SAND):
            continue

        # Skip tiles that are currently on update delay
        if update_delay_array[i][j] > 0:
            update_delay_array[i][j] -= 1
            continue

        # Try to move the tile down
        if j < MAP_HEIGHT - 1 and map_array[i][j + 1] == AIR:
            map_array[i][j + 1] = map_array[i][j]
            map_array[i][j] = AIR
            update_delay_array[i][j + 1] = UPDATE_DELAY
            continue

        # Try to move the tile down and to the left
        if i > 0 and j < MAP_HEIGHT - 1 and map_array[i - 1][j + 1] == AIR:
            map_array[i - 1][j + 1] = map_array[i][j]
            map_array[i][j] = AIR
            update_delay_array[i - 1][j + 1] = UPDATE_DELAY
            continue

        # Try to move the tile down and to the right
        if i < MAP_WIDTH - 1 and j < MAP_HEIGHT - 1 and map_array[i + 1][j + 1] == AIR:
            map_array[i + 1][j + 1] = map_array[i][j]
            map_array[i][j] = AIR
            update_delay_array[i + 1][j + 1] = UPDATE_DELAY
            continue

    # Draw the map
    for i in range(MAP_WIDTH):
        for j in range(MAP_HEIGHT):
            pygame.draw.rect(screen, colors[map_array[i][j]], pygame.Rect(i * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Update the display
    pygame.display.flip()

# Clean up Pygame
pygame.quit()
