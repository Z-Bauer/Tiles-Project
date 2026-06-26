from game import Tile, Slide
import pygame

pygame.init()

# Tile Test
def test_tile_initialization():
    rect = pygame.Rect(0, 0, 80, 80)
    tile = Tile(rect, 2, 3, "blank")

    assert tile.x == 2
    assert tile.y == 3
    assert tile.container == "blank"
    assert tile.hitbox == rect
    
# Slide Test
def test_slide_move():
    s = Slide(0, 0, 10, 10, 20, 20)
    s.move(5)

    assert s.coord_1 == [5, 5]
    assert s.coord_2 == [15, 15]
    assert s.coord_3 == [25, 25]
    
# Grid Logic Test
def test_grid_generation_logic():
    tile_rows = 5
    tile_cols = 5

    tiles = []
    for i in range(tile_rows):
        for j in range(tile_cols):
            tiles.append((i, j))

    assert len(tiles) == 25
    assert (0, 0) in tiles
    assert (4, 4) in tiles
    
# Enemy Rule Validation
def is_valid_enemy_tile(tile):
    return tile.container not in ["player", "enemy"]


def test_enemy_spawn_rule():
    assert is_valid_enemy_tile(Tile(None, 1, 1, "blank")) is True
    assert is_valid_enemy_tile(Tile(None, 1, 1, "player")) is False
    assert is_valid_enemy_tile(Tile(None, 1, 1, "enemy")) is False
    
# Attack/Score Logic
def resolve_attack(tile, score):
    if tile.container == "enemy":
        tile.container = "blank"
        return score + 1
    return score


def test_attack_enemy():
    tile = Tile(None, 1, 1, "enemy")

    new_score = resolve_attack(tile, 0)

    assert new_score == 1
    assert tile.container == "blank"


def test_attack_non_enemy():
    tile = Tile(None, 1, 1, "blank")

    new_score = resolve_attack(tile, 0)

    assert new_score == 0
    assert tile.container == "blank"
    
# Level Up Logic
def update_level(score, to_next_level, level):
    if score >= to_next_level:
        level += 1
        to_next_level += 5 * level
    return level, to_next_level


def test_level_up():
    level, req = update_level(10, 10, 1)

    assert level == 2
    assert req > 10


def test_no_level_up():
    level, req = update_level(5, 10, 1)

    assert level == 1
    assert req == 10