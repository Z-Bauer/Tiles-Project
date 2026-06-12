import pygame
import sys
import random

#create screen
pygame.init()
pygame.font.init()
screen_width = 500
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Moveable Tiles")

#Set frame rate
clock = pygame.time.Clock()

# Tile settings (return to once art is made) 
tile_width = 80
tile_height = 80
tile_rows = 5
tile_cols = 5
tile_gap = 10
tile_wait = 4

# Store tiles
tiles = []
most_recent = ['', '']

# SCORE
score = 0
level = 1
to_next_level = 10

my_font = pygame.font.SysFont('Times New Roman', 18)
score_surface = my_font.render(str(score), False, (0, 0, 0))


# Generate tiles
x = 0
y = 0
for i in range(tile_rows):
    y = 0
    x += 1
    tileY = (i * (tile_height + tile_gap)) + 25
    for j in range(tile_cols):
        y += 1
        tileX = (j * (tile_width + tile_gap)) + 125
        # Add the tile to storage, storing its X and Y in a list
        tiles.append([pygame.Rect(tileY, tileX, tile_width, tile_height), x, y, "blank"])
        # [hitbox, tile x, tile y, container]
        print(x, y)

    # Remove the tile in the center, set tile as player
    blank_x = 3
    blank_y = 3
    for tile in tiles:
        if tile[1] == blank_x and tile[2] == blank_y:
            tiles.remove(tile)
        if tile[1] == 3 and tile[2] == 2:
            tile[3] = "player"
    

# Update the board based on tile position
def tile_update():
    for tile in tiles:
        if tile[3] == "blank":
            pygame.draw.rect(screen, (145, 145, 145), tile[0])
        if tile[1] == most_recent[0] and tile[2] == most_recent[1]:
            pygame.draw.rect(screen, (120, 120, 120), tile[0])
        if tile[3] == "player":
            pygame.draw.rect(screen, (25, 109, 212), tile[0])
        if tile[3] == "enemy":
            pygame.draw.rect(screen, (235, 64, 52), tile[0])
    pygame.display.flip()

enemy_timer = 0
enemy_wait_time = 3000
enemy_min_time = 1200

active = True

# MAIN GAME LOOP
while active:
    for event in pygame.event.get():
        # Quits the game when window is closed
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Basic movement protocol
        if event.type == pygame.KEYDOWN:
            # Move the blank LEFT
            if event.key == pygame.K_LEFT:
                if blank_x < 5:
                    for tile in tiles:
                        if tile[1] == blank_x + 1 and tile[2] == blank_y:
                            tile[1] = blank_x
                            for x in range(10):
                                tile[0].x -= ((tile_width + tile_gap) / 10)
                                pygame.time.wait(tile_wait)
                                tile_update()
                            most_recent = [tile[1], tile[2]]
                            break
                    blank_x += 1
            # Move the blank RIGHT
            if event.key == pygame.K_RIGHT:
                if blank_x > 1:
                    for tile in tiles:
                        if tile[1] == blank_x - 1 and tile[2] == blank_y:
                            tile[1] = blank_x
                            for x in range(10):
                                tile[0].x += ((tile_width + tile_gap) / 10)
                                pygame.time.wait(tile_wait)
                                tile_update()
                            most_recent = [tile[1], tile[2]]
                            break
                    blank_x -= 1
            # Move the blank UP
            if event.key == pygame.K_UP:
                if blank_y < 5:
                    for tile in tiles:
                        if tile[2] == blank_y + 1 and tile[1] == blank_x:
                            tile[2] = blank_y
                            for x in range(10):
                                tile[0].y -= ((tile_width + tile_gap) / 10)
                                pygame.time.wait(tile_wait)
                                tile_update()
                            most_recent = [tile[1], tile[2]]
                            break
                    blank_y += 1
            # Move the blank DOWN
            if event.key == pygame.K_DOWN:
                if blank_y > 1:
                    for tile in tiles:
                        if tile[2] == blank_y - 1 and tile[1] == blank_x:
                            tile[2] = blank_y
                            for x in range(10):
                                tile[0].y += ((tile_width + tile_gap) / 10)
                                pygame.time.wait(tile_wait)
                                tile_update()
                            most_recent = [tile[1], tile[2]]
                            break
                    blank_y -= 1
            # Attack! 
            if event.key == pygame.K_SPACE:
                for tile in tiles:
                    if tile[3] == "player":
                        tile[3] = "blank"
                    if tile[1] == most_recent[0] and tile[2] == most_recent[1]:
                        if tile[3] == "enemy":
                            score += 1
                            print("Score:", score)
                            # LEVEL UP! Enemies start to get faster! 
                            if score >= to_next_level:
                                level += 1
                                print("LEVEL UP!")
                                print("Level", level)
                                to_next_level = to_next_level + (5 * level)
                                if enemy_min_time > 300:
                                    enemy_min_time -= 100
                        tile[3] = "player"


    # Check for Game Loss
    enemy_count = 0
    for tile in tiles:
        if tile[3] == "enemy":
            enemy_count += 1
    if enemy_count >= 13:
        print("YOU LOSE!")
        print("Final Score:", score)
        active = False
            

    # Spawn Enemies
    current_time = pygame.time.get_ticks()
    if current_time - enemy_timer > enemy_wait_time:
        # Choose a random tile, if it ISN'T the player, make it an enemy
        while True:
            next_enemy = random.randint(0, 23)
            if tiles[next_enemy][3] != "player":
                tiles[next_enemy][3] = "enemy"
                break
        # Reset the enemy timer
        enemy_timer = current_time
        # The enemy spawning rate gets quicker
        if enemy_wait_time >= enemy_min_time:
            enemy_wait_time -= random.randint(50, 150)
        if enemy_wait_time < enemy_min_time:
            enemy_wait_time = enemy_min_time
    
    screen.fill((255, 255, 255))

    score_surface = my_font.render(str(score), False, (0, 0, 0))
    level_surface = my_font.render(str(level), False, (0, 0, 0))
    screen.blit(score_surface, (0,0))
    screen.blit(level_surface, (0, 25))

    tile_update()

    clock.tick(60)

while True:
    for event in pygame.event.get():
        # Quits the game when window is closed
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    


