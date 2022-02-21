import sys, pygame, random
from pygame.locals import *

clock = pygame.time.Clock()

pygame.display.set_caption("Pygame Window")

window_size = (400, 400)

screen = pygame.display.set_mode(window_size)

# create player img
player_img = pygame.image.load("halo_sprite.png")
player_location = [100,100]




# create block
block_surface = pygame.Surface((50, 50))
block_location = [75, 75]

player_rect = pygame.Rect(player_location[0], player_location[1], player_img.get_width(), player_img.get_height())
block_rect = pygame.Rect(block_location[0], block_location[1], block_surface.get_width(), block_surface.get_height())

moving_right = False
moving_left = False
player_y_momentum = 0
player_speed = 5


while True:
    # fill the screen and then blit the player/block
    screen.fill((200, 200, 200))
    screen.blit(block_surface, block_location)
    screen.blit(player_img,player_location)



    print(block_rect)

    if player_location[1] > window_size[1] - player_img.get_height():
        player_y_momentum = -player_y_momentum
    else:
        player_y_momentum += 0.2
    player_location[1] += player_y_momentum

    if moving_right == True:
        player_location[0] += player_speed
        player_img = pygame.image.load("halo_sprite.png")
    if moving_left == True:
        player_location[0] -= player_speed
        player_img = pygame.image.load("halo_sprite_left.png")

    # change x/y coords of player_rect, as the rect function is outside of the main loop.
    player_rect.x = player_location[0]
    player_rect.y = player_location[1]

    # if the player collides with the block, fill the block red
    if player_rect.colliderect(block_rect):
        block_surface.fill((255, 0, 0))
    else:
        block_surface.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False



    pygame.display.update()
    clock.tick(60)