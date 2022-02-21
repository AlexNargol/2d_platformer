import sys, pygame, random
from pygame.locals import *

clock = pygame.time.Clock()

pygame.display.set_caption("Pygame Window")

window_size = (600, 400)

screen = pygame.display.set_mode(window_size, 0, 32)

display = pygame.Surface((480, 208)) # used as the surface for rendering, which gets scaled

# create player img
player = pygame.image.load("halo_sprite_resized.png")
player_img = pygame.transform.smoothscale(player, (10,10))
player_location = [100, 100]

# load grass and dirt vectors
grass_img = pygame.image.load("grass.png")
TILE_SIZE = grass_img.get_width()
dirt_img = pygame.image.load("dirt.png")


# load the map file
# open the map file, split by line spaces, convert each row to a list of individual string numbers
def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

true_scroll = [0, 0]


print(TILE_SIZE)
game_map = load_map('map')

''' Printing width, to determine suitable size of pygame display surface.
    Take the TILE_SIZE, which works out the size of the grassy/dirt blocks
'''
width = TILE_SIZE * len(game_map[0])
print(width)

height = TILE_SIZE * len(game_map)
print(height)


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


player_rect = pygame.Rect(50, 50, player_img.get_width(), player_img.get_height())

moving_right = False
moving_left = False
player_y_momentum = 0
player_speed = 5

while True:
    # fill the screen and then blit the player/block
    display.fill((200, 180, 255))

    true_scroll[0] += (player_rect.x-true_scroll[0] - 152) / 20
    true_scroll[1] += (player_rect.y-true_scroll[1] - 106) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(dirt_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile == '2':
                display.blit(grass_img, (x * 16 - scroll[0] , y * 16 - scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
            x += 1
        y += 1

    player_location[1] += player_y_momentum

    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 5
        player_img = pygame.image.load("halo_sprite_resized.png")
    if moving_left:
        player_movement[0] -= 5
        player_img = pygame.image.load("halo_sprite_left_resized.png")
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3
    player_location[1] += player_y_momentum

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player_y_momentum = 1

    display.blit(player_img, (player_rect.x, player_rect.y))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                player_y_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    screen.blit(pygame.transform.scale(display, window_size), (0, 0))
    pygame.display.update()
    clock.tick(60)
