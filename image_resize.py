import sys, pygame
from pygame.locals import *

# load in image to be resized
player = pygame.image.load("halo_sprite.png")
player_left = pygame.image.load("halo_sprite_left.png")

# scale the player img to 10 x 10
new_img = pygame.transform.scale(player, (10, 10))
new_img_left = pygame.transform.scale(player_left, (10, 10))
# save img
pygame.image.save(new_img, "halo_sprite_resized.png")
pygame.image.save(new_img_left, "halo_sprite_left_resized.png")