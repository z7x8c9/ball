import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up game window
window_size = (1200, 900)  # Double the size of the window
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Sword Interaction Game')

# Set up colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Game objects
rect_size = (800, 600)  # Double the rectangle size
rect_pos = (200, 200)
image1_pos = [rect_pos[0] + 100, rect_pos[1] + 100]
image2_pos = [rect_pos[0] + rect_size[0] - 200, rect_pos[1] + rect_size[1] - 200]
image1_velocity = [4, 4]
image2_velocity = [4, 4]
sword_attached_to = None
image_health = [100, 100]

# Load images and sword
image1 = pygame.image.load('image1.png')
image1 = pygame.transform.scale(image1, (100, 100))  # Double the size
image2 = pygame.image.load('image2.png')
image2 = pygame.transform.scale(image2, (100, 100))  # Double the size
sword = pygame.image.load('sword.png')
sword = pygame.transform.scale(sword, (40, 120))  # Double the size

# Function to draw health bars
def draw_health_bar(screen, x, y, health, color):
    pygame.draw.rect(screen, color, (x, y, health * 2, 20))  # Double the width and height

# Function to draw outlines
def draw_outline(screen, rect, color, thickness=5):
    pygame.draw.rect(screen, color, rect, thickness)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move images diagonally
    image1_pos[0] += image1_velocity[0]
    image1_pos[1] += image1_velocity[1]
    image2_pos[0] += image2_velocity[0]
    image2_pos[1] += image2_velocity[1]

    # Bounce off rectangle edges
    if image1_pos[0] <= rect_pos[0] or image1_pos[0] >= rect_pos[0] + rect_size[0] - 100:
        image1_velocity[0] *= -1
    if image1_pos[1] <= rect_pos[1] or image1_pos[1] >= rect_pos[1] + rect_size[1] - 100:
        image1_velocity[1] *= -1

    if image2_pos[0] <= rect_pos[0] or image2_pos[0] >= rect_pos[0] + rect_size[0] - 100:
        image2_velocity[0] *= -1
    if image2_pos[1] <= rect_pos[1] or image2_pos[1] >= rect_pos[1] + rect_size[1] - 100:
        image2_velocity[1] *= -1

    # Bounce off each other
    image1_rect = pygame.Rect(image1_pos, (100, 100))
    image2_rect = pygame.Rect(image2_pos, (100, 100))
    if image1_rect.colliderect(image2_rect):
        image1_velocity[0] *= -1
        image1_velocity[1] *= -1
        image2_velocity[0] *= -1
        image2_velocity[1] *= -1

    # Define the rectangle
    rect = pygame.Rect(rect_pos, rect_size)

    # Sword interaction
    if sword_attached_to is None:
        sword_rect = sword.get_rect(topleft=(200, 200))  # Spawn the sword at (200, 200)
        if image1_rect.colliderect(sword_rect):
            sword_attached_to = 0
        elif image2_rect.colliderect(sword_rect):
            sword_attached_to = 1
    else:
        if sword_attached_to == 0:
            sword_rect.center = image1_rect.center
        else:
            sword_rect.center = image2_rect.center

        # Check for collision between images with sword interaction
        if image1_rect.colliderect(image2_rect):
            if sword_attached_to is not None:
                if sword_attached_to == 0:
                    sword_rect.topleft = image1_rect.topleft
                    image_health[1] -= 10
                else:
                    sword_rect.topleft = image2_rect.topleft
                    image_health[0] -= 10
                sword_attached_to = None

    # Check if any image's health reaches 0
    if image_health[0] <= 0 or image_health[1] <= 0:
        running = False  # Stop the game loop

    # Drawing
    screen.fill(WHITE)
    pygame.draw.rect(screen, (0, 0, 0), rect, 2)
    screen.blit(image1, image1_pos)
    screen.blit(image2, image2_pos)
    if sword_attached_to is None:
        screen.blit(sword, sword_rect.topleft)  # Draw sword only when it's not attached to an image
    else:
        screen.blit(sword, sword_rect.topleft)

    # Draw outlines
    draw_outline(screen, image1_rect, RED)
    draw_outline(screen, image2_rect, BLUE)
    
    # Draw health bars
    draw_health_bar(screen, rect_pos[0], rect_pos[1] - 40, image_health[0], RED)
    draw_health_bar(screen, rect_pos[0] + rect_size[0] - 200, rect_pos[1] - 40, image_health[1], BLUE)
    
    pygame.display.flip()
    pygame.time.delay(10)

pygame.quit()
sys.exit()

#hello
