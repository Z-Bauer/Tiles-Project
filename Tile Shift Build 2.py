import pygame
import sys
import random

# create screen
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
highscore = 0

my_font = pygame.font.SysFont('Bauhaus93', 25)
title_font = pygame.font.SysFont('Bauhaus93', 100)
enter_font = pygame.font.SysFont('Bauhaus93', 35)
score_surface = my_font.render(str(score), False, (0, 0, 0))

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
        screen.fill((255, 255, 255))
        title_surface1 = title_font.render("TILE", True, (0, 0, 0))
        title_surface2 = title_font.render("SHIFT", True, (0, 0, 0))
        title_surface3 = enter_font.render("-- press ENTER to start --", True, (0, 0, 0))
        screen.blit(title_surface1, (40, 40))
        screen.blit(title_surface2, (230, 120))
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

SE_Slide = Slide(-300, -300, -300, 300, 200, -300)
NW_Slide = Slide(800, 300, 800, 900, 300, 900)

def screen_close():
    SE_Slide = Slide(-300, -300, -300, 300, 200, -300)
    NW_Slide = Slide(800, 300, 800, 900, 300, 900)
    #pygame.time.wait(1200)
    for x in range(13):
        pygame.draw.polygon(screen, (255, 255, 255), [SE_Slide.coord_1, SE_Slide.coord_2, SE_Slide.coord_3])
        pygame.draw.polygon(screen, (255, 255, 255), [NW_Slide.coord_1, NW_Slide.coord_2, NW_Slide.coord_3])
        NW_Slide.move(int(-25))
        SE_Slide.move(int(25))
        pygame.display.flip()
        clock.tick(60)

external_active = True
while external_active:

    wait_screen()

    screen_close()
    
    print("LOOP START")
    screen.fill((255, 255, 255))
    pygame.display.flip()

    # Reset Score
    score = 0
    level = 1
    to_next_level = 10
    
    # Generate tiles
    x = 0
    y = 0
    tiles = []
    most_recent = ['', '']
    
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

    # Update the board based on tile position
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
                                print("Score:", score)
                                # LEVEL UP! Enemies start to get faster! 
                                if score >= to_next_level:
                                    level += 1
                                    print("LEVEL UP!")
                                    print("Level", level)
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
            print("YOU LOSE!")
            print("Final Score:", score)
            if highscore <= score:
                highscore = score
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

        score_text = "SCORE: " + str(score)
        level_text = "LEVEL: " + str(level)

        score_surface = my_font.render(score_text, True, (0, 0, 0))
        level_surface = my_font.render(level_text, True, (0, 0, 0))
        screen.blit(score_surface, (25, 25))
        screen.blit(level_surface, (25, 60))

        tile_update()
        
        clock.tick(60)

    pygame.time.wait(1200)

    screen_close()

    pygame.time.wait(1000)
    
    final_score = "FINAL SCORE: " + str(score)
    high_score = "HIGH SCORE: " + str(highscore)
    
    final_score_width, final_score_height = my_font.size(final_score)
    final_score_surface = my_font.render(final_score, True, (0, 0, 0))
    high_score_width, high_score_height = my_font.size(high_score)
    high_score_surface = my_font.render(high_score, True, (0, 0, 0))
    screen.blit(final_score_surface, (((500 - final_score_width) / 2), 150))
    pygame.display.flip()
    pygame.time.wait(1000)
    screen.blit(high_score_surface, (((500 - high_score_width) / 2), 300))
    pygame.display.flip()

    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            # Quits the game when window is closed
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting_for_restart = False

    


