# Import libraries
import pygame
import sys
import random

# Create screen
pygame.init()
pygame.font.init()
screen_width = 500
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Moveable Tiles")

# Set frame rate
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
try:
    # Look at 'highscore' file, read highscore
    with open("highscore.txt") as f:
        highscore = int(f.read())
except:
    # If no 'highscore' file exists, create one and save first score as 0
    f = open("highscore.txt", "w")
    f.write("0")
    highscore = 0

# Initialize fonts
my_font = pygame.font.SysFont('Bauhaus93', 25)
title_font = pygame.font.SysFont('Bauhaus93', 100)
enter_font = pygame.font.SysFont('Bauhaus93', 35)
score_surface = my_font.render(str(score), False, (0, 0, 0))

# Class definitions
class Tile:

    def __init__(self, hitbox, x, y, container):
        self.hitbox = hitbox
        self.x = x
        self.y = y
        self.container = container

class Slide:

    def __init__(self, x1, y1, x2, y2, x3, y3):
        self.coord_1 = [x1, y1]
        self.coord_2 = [x2, y2]
        self.coord_3 = [x3, y3]

    def move(self, amount):
        self.coord_1[0] += amount
        self.coord_1[1] += amount
        self.coord_2[0] += amount
        self.coord_2[1] += amount
        self.coord_3[0] += amount
        self.coord_3[1] += amount

# Title Screen -- waiting for ENTER to be pressed
def wait_screen():
    screen.fill((255, 255, 255))
    title_timer = 0
    title1x = -60
    title2x = 330
    for i in range(10):
        # Title screen animation
        screen.fill((255, 255, 255))
        title_surface1 = title_font.render("TILE", True, (0, 0, 0))
        title_surface2 = title_font.render("SHIFT", True, (0, 0, 0))
        screen.blit(title_surface1, (title1x, 40))
        screen.blit(title_surface2, (title2x, 120))
        title1x += 10
        title2x -= 10
        pygame.display.flip()
        clock.tick(60)
    waiting = True
    while waiting:
        # Blinking ENTER button
        screen.fill((255, 255, 255))
        title_surface1 = title_font.render("TILE", True, (0, 0, 0))
        title_surface2 = title_font.render("SHIFT", True, (0, 0, 0))
        title_surface3 = enter_font.render("-- press ENTER to start --", True, (0, 0, 0))
        screen.blit(title_surface1, (40, 40))
        screen.blit(title_surface2, (230, 120))
        # Timing for ENTER button, blinks on and off every second or so
        title_timer += 1
        if title_timer <= 30:
            screen.blit(title_surface3, (75, 450))
        if title_timer >= 60:
            title_timer = 0
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(60)

# Initialize two halves of 'sliding' animation
# (Coords are built to take up exactly half of the screen)
SE_Slide = Slide(-300, -300, -300, 300, 200, -300)
NW_Slide = Slide(800, 300, 800, 900, 300, 900)

# Function for screen transitions
def screen_close():
    SE_Slide = Slide(-300, -300, -300, 300, 200, -300)
    NW_Slide = Slide(800, 300, 800, 900, 300, 900)
    for x in range(13):
        pygame.draw.polygon(screen, (255, 255, 255), [SE_Slide.coord_1, SE_Slide.coord_2, SE_Slide.coord_3])
        pygame.draw.polygon(screen, (255, 255, 255), [NW_Slide.coord_1, NW_Slide.coord_2, NW_Slide.coord_3])
        NW_Slide.move(int(-25))
        SE_Slide.move(int(25))
        pygame.display.flip()
        clock.tick(60)

# Credits
for x in range(200):
    screen.fill((0, 0, 0))
    
    credits_width, credits_height = enter_font.size("A GAME BY:")
    zach_width, zach_height = enter_font.size("Zachary Bauer")
    sam_width, sam_height = enter_font.size("Sam Sikorski")
    will_width, will_height = enter_font.size("William Wen")
    
    credits_surface = enter_font.render("A GAME BY:", True, (255, 255, 255))
    zach_surface = enter_font.render("Zachary Bauer", True, (255, 255, 255))
    sam_surface = enter_font.render("Sam Sikorski", True, (255, 255, 255))
    will_surface = enter_font.render("William Wen", True, (255, 255, 255))
    
    screen.blit(credits_surface, (((500 - credits_width) / 2), 200))
    screen.blit(zach_surface, (((500 - zach_width) / 2), 250))
    screen.blit(sam_surface, (((500 - sam_width) / 2), 300))
    screen.blit(will_surface, (((500 - will_width) / 2), 350))
    
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    clock.tick(60)
    
screen_close()

# Beginning of EXTERNAL LOOP
external_active = True
while external_active:

    # Loop until ENTER is pressed
    wait_screen()

    # Screen transition
    screen_close()
    
    screen.fill((255, 255, 255))
    pygame.display.flip()

    # Reset SCORE
    score = 0
    level = 1
    to_next_level = 10
    
    # Generate empty list of tiles
    x = 0
    y = 0
    tiles = []
    most_recent = ['', '']

    # Generate all tiles
    for i in range(tile_rows):
        y = 0
        x += 1
        tileY = (i * (tile_height + tile_gap)) + 25
        for j in range(tile_cols):
            y += 1
            tileX = (j * (tile_width + tile_gap)) + 125
            # Add the tile to storage, storing its X and Y in a list
            tile_box = pygame.Rect(tileY, tileX, tile_width, tile_height)
            tiles.append(Tile(tile_box, x, y, "blank"))
            # [hitbox, tile x, tile y, container]

        # Remove the tile in the center, set tile as player
        blank_x = 3
        blank_y = 3
        for tile in tiles:
            if tile.x == blank_x and tile.y == blank_y:
                tiles.remove(tile)
            if tile.x == 3 and tile.y == 2:
                tile.container = "player"

    # Function to update the board based on tile position
    def tile_update():
        for tile in tiles:
            if tile.container == "blank":
                pygame.draw.rect(screen, (145, 145, 145), tile.hitbox)
            if tile.x == most_recent[0] and tile.y == most_recent[1]:
                pygame.draw.rect(screen, (120, 120, 120), tile.hitbox)
            if tile.container == "player":
                pygame.draw.rect(screen, (25, 109, 212), tile.hitbox)
            if tile.container == "enemy":
                pygame.draw.rect(screen, (235, 64, 52), tile.hitbox)
        pygame.display.flip()

    def screen_open():
        for x in range(13):
            pygame.draw.polygon(screen, (255, 255, 255), [SE_Slide.coord_1, SE_Slide.coord_2, SE_Slide.coord_3])
            pygame.draw.polygon(screen, (255, 255, 255), [NW_Slide.coord_1, NW_Slide.coord_2, NW_Slide.coord_3])
            NW_Slide.move(int(25))
            SE_Slide.move(int(-25))
            pygame.display.flip()
            clock.tick(60)

    # Timer for enemy spawning    
    enemy_timer = 0
    enemy_wait_time = 3000
    enemy_min_time = 1200

    active = True

    # Beginning of MAIN GAME LOOP
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
                            if tile.x == blank_x + 1 and tile.y == blank_y:
                                tile.x = blank_x
                                for i in range(10):
                                    tile.hitbox.x -= ((tile_width + tile_gap) / 10)
                                    pygame.time.wait(tile_wait)
                                    tile_update()
                                most_recent = [tile.x, tile.y]
                                break
                        blank_x += 1
                # Move the blank RIGHT
                if event.key == pygame.K_RIGHT:
                    if blank_x > 1:
                        for tile in tiles:
                            if tile.x == blank_x - 1 and tile.y == blank_y:
                                tile.x = blank_x
                                for i in range(10):
                                    tile.hitbox.x += ((tile_width + tile_gap) / 10)
                                    pygame.time.wait(tile_wait)
                                    tile_update()
                                most_recent = [tile.x, tile.y]
                                break
                        blank_x -= 1
                # Move the blank UP
                if event.key == pygame.K_UP:
                    if blank_y < 5:
                        for tile in tiles:
                            if tile.y == blank_y + 1 and tile.x == blank_x:
                                tile.y = blank_y
                                for i in range(10):
                                    tile.hitbox.y -= ((tile_width + tile_gap) / 10)
                                    pygame.time.wait(tile_wait)
                                    tile_update()
                                most_recent = [tile.x, tile.y]
                                break
                        blank_y += 1
                # Move the blank DOWN
                if event.key == pygame.K_DOWN:
                    if blank_y > 1:
                        for tile in tiles:
                            if tile.y == blank_y - 1 and tile.x == blank_x:
                                tile.y = blank_y
                                for i in range(10):
                                    tile.hitbox.y += ((tile_width + tile_gap) / 10)
                                    pygame.time.wait(tile_wait)
                                    tile_update()
                                most_recent = [tile.x, tile.y]
                                break
                        blank_y -= 1
                # Attack! 
                if event.key == pygame.K_SPACE:
                    for tile in tiles:
                        if tile.container == "player":
                            tile.container = "blank"
                        if tile.x == most_recent[0] and tile.y == most_recent[1]:
                            if tile.container == "enemy":
                                score += 1
                                # LEVEL UP! Enemies start to get faster! 
                                if score >= to_next_level:
                                    level += 1
                                    to_next_level = to_next_level + (5 * level)
                                    if enemy_min_time > 300:
                                        enemy_min_time -= 100
                            tile.container = "player"


        # Check for Game Loss
        enemy_count = 0
        for tile in tiles:
            if tile.container == "enemy":
                enemy_count += 1
        if enemy_count >= 13:
            # If the score is bigger than highscore, change highscore
            if highscore <= score:
                highscore = score
                # Change value of highscore file
                with open("highscore.txt", "w") as f:
                    f.write(str(highscore))
            # End internal MAIN
            active = False
                

        # Spawn Enemies
        current_time = pygame.time.get_ticks()
        if current_time - enemy_timer > enemy_wait_time:
            # Choose a random tile, if it ISN'T the player, make it an enemy
            while True:
                next_enemy = random.randint(0, 23)
                if tiles[next_enemy].container != "player" and tiles[next_enemy].container != "enemy":
                    tiles[next_enemy].container = "enemy"
                    break
            # Reset the enemy timer
            enemy_timer = current_time
            # The enemy spawning rate gets quicker
            if enemy_wait_time >= enemy_min_time:
                enemy_wait_time -= random.randint(50, 150)
            if enemy_wait_time < enemy_min_time:
                enemy_wait_time = enemy_min_time
        
        screen.fill((255, 255, 255))

        # Create stat text
        score_text = "SCORE: " + str(score)
        level_text = "LEVEL: " + str(level)
        enemies_text = "ENEMIES:"
        enemies_number = str(enemy_count)

        # Display stat text at top of screen
        score_surface = my_font.render(score_text, True, (0, 0, 0))
        level_surface = my_font.render(level_text, True, (0, 0, 0))
        enemies_surface = my_font.render(enemies_text, True, (0, 0, 0))
        if enemy_count < 10:
            enemies_number_surface = my_font.render(enemies_number, True, (0, 0, 0))
        else:
            enemies_number_surface = my_font.render(enemies_number, True, (235, 64, 52))

        # Push all text to screen
        screen.blit(score_surface, (25, 25))
        screen.blit(level_surface, (25, 60))
        screen.blit(enemies_surface, (370, 25))
        screen.blit(enemies_number_surface, (370, 60))

        # Display tiles, update screen
        tile_update()

        # Frame tick
        clock.tick(60)

    pygame.time.wait(1200)

    # Screen transition
    screen_close()

    pygame.time.wait(1000)

    # Create strings for FINAL SCORE and HIGH SCORE
    final_score = "FINAL SCORE: " + str(score)
    high_score = "HIGH SCORE: " + str(highscore)

    # Display ending text, with a second-long buffer between each one
    # Get width of each text box, in order to center it regardless of number length
    final_score_width, final_score_height = my_font.size(final_score)
    final_score_surface = my_font.render(final_score, True, (0, 0, 0))
    high_score_width, high_score_height = my_font.size(high_score)
    high_score_surface = my_font.render(high_score, True, (0, 0, 0))
    restart_width, restart_height = my_font.size("- press ENTER to restart -")
    screen.blit(final_score_surface, (((500 - final_score_width) / 2), 135))
    pygame.display.flip()
    pygame.time.wait(1000)
    screen.blit(high_score_surface, (((500 - high_score_width) / 2), 270))
    pygame.display.flip()
    pygame.time.wait(1000)
    restart_surface = my_font.render("- press ENTER to restart -", True, (0, 0, 0))
    screen.blit(restart_surface, (((500 - restart_width) / 2), 405))
    # Update screen
    pygame.display.flip()

    waiting_for_restart = True
    restart_timer = 0
    while waiting_for_restart:

        screen.fill((255, 255, 255))
        final_score_surface = my_font.render(final_score, True, (0, 0, 0))
        high_score_surface = my_font.render(high_score, True, (0, 0, 0))
        screen.blit(final_score_surface, (((500 - final_score_width) / 2), 135))
        screen.blit(high_score_surface, (((500 - high_score_width) / 2), 270))
        restart_surface = my_font.render("- press ENTER to restart -", True, (0, 0, 0))
        if restart_timer <= 30:
            screen.blit(restart_surface, (((500 - restart_width) / 2), 405))
        if restart_timer == 60:
            restart_timer = 0
        # Update screen
        pygame.display.flip()
        restart_timer += 1
        
        for event in pygame.event.get():
            # Quits the game when window is closed
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting_for_restart = False
        clock.tick(60)

    


