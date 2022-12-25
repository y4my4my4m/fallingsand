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

# The size of the character (in tiles)
CHARACTER_WIDTH = 2
CHARACTER_HEIGHT = 2

# The initial position of the character (in tiles)
character_x = 50
character_y = 0

# The vertical velocity of the character (in tiles per simulation step)
character_vy = 0

# The maximum vertical velocity of the character (in tiles per simulation step)
MAX_VY = 10

# The acceleration of the character when falling (in tiles per simulation step per simulation step)
GRAVITY = 0.5

# The friction of the character when sliding (in tiles per simulation step per simulation step)
FRICTION = 0.9

# The force applied to the character when jumping (in tiles per simulation step)
JUMP_FORCE = 4

# Set the character movement speed
MOVEMENT_SPEED = 2

floating_timer = 0

# Initialize Pygame
pygame.init()

# Set the window size and title
screen = pygame.display.set_mode((MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE))
pygame.display.set_caption('Falling Sand')

# Initialize the map a block of sand 
# map_array[50][0] = SAND

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
            if event.key == pygame.K_0:
                current_material = AIR
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
    # Check for key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        character_x -= MOVEMENT_SPEED
    if keys[pygame.K_d]:
        character_x += MOVEMENT_SPEED
    if keys[pygame.K_w]:
        character_y -= JUMP_FORCE
    if keys[pygame.K_s]:
        character_y += MOVEMENT_SPEED
    # Update the character position
    character_y += character_vy
    character_vy += GRAVITY
    character_vy = min(character_vy, MAX_VY)
    character_x = max(0, min(character_x, MAP_WIDTH - CHARACTER_WIDTH))

    # Make sure the character is not falling off the map
    character_y = max(0, min(character_y, MAP_HEIGHT - CHARACTER_HEIGHT))

    # Check if the character is standing on solid ground
    standing = False
    for i in range(CHARACTER_WIDTH):
        for j in range(CHARACTER_HEIGHT):
            x = int(character_x) + i
            y = int(character_y) + j
            if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT and map_array[x][y] in (WALL, SAND):
                standing = True
                break
    if standing:
        # Reset the floating timer if the character is standing on solid ground
        floating_timer = 0
        character_vy = 0
        character_y = int(character_y // CHARACTER_HEIGHT) * CHARACTER_HEIGHT
    else:
        # Check if the character is standing on water
        standing_on_water = False
        for i in range(CHARACTER_WIDTH):
            for j in range(CHARACTER_HEIGHT):
                x = int(character_x) + i
                y = int(character_y) + j
                if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT and map_array[x][y] == WATER:
                    standing_on_water = True
                    break
        if standing_on_water:
            # Float in water
            if character_vy > 0:
                character_vy = -0.025
                # Reset the floating timer if the character was moving upwards
            #     floating_timer = 30
            # if floating_timer > 0:
            #     # Float on top of the water
            #     character_vy = -0.05
            #     floating_timer -= 1
            # else:
            #     # Slowly sink in the water
            #     character_vy += 0.1
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

   # Draw the character
    for i in range(CHARACTER_WIDTH):
        for j in range(CHARACTER_HEIGHT):
            pygame.draw.rect(screen, (255, 0, 0), (character_x * TILE_SIZE + i * TILE_SIZE, character_y * TILE_SIZE + j * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Update the display
    pygame.display.flip()

# Clean up Pygame
pygame.quit()
