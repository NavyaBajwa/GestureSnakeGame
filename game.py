import os
os.environ['OPENCV_AVFOUNDATION_SKIP_AUTH'] = '1'

import pygame
from webcamGestures import HandGestureTracker
from tile import Tile
import random

pygame.init()
pygame.font.init()

font = pygame.font.SysFont(None, 24)

ROWS = 25
COLUMNS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE*COLUMNS
WINDOW_HEIGHT = TILE_SIZE*ROWS

STEP_DELAY = 150

SNAKE_COLOURS = [(223, 175, 233), (137, 134, 213)]

last_move_time = pygame.time.get_ticks()

# create the pygame window: need width and height
(width, height) = (WINDOW_WIDTH, WINDOW_HEIGHT) 
screen = pygame.display.set_mode((width, height)) # pygame window object
pygame.display.set_caption("Snakey's got Hands") # set window title
background = (245, 250, 195) 
#screen.fill(background) # set background colour

# set up initial snake
snake = Tile(5*TILE_SIZE, 5*TILE_SIZE)
snake_body = [] # lots of Tile objects
food = Tile(10*TILE_SIZE, 10*TILE_SIZE)
velocityX = 0
velocityY = 0

score = 0


# Draw initial frame
screen.fill(background)
#pygame.draw.rect(screen, (110, 86, 245), (snake.x, snake.y, TILE_SIZE, TILE_SIZE)) # draw snake
#pygame.draw.rect(screen, (245, 0, 0), (food.x, food.y, TILE_SIZE, TILE_SIZE)) # draw food
pygame.display.flip()

# create tracker object
tracker = HandGestureTracker()
tracker.start()

# once flip() is called, the end of the program is reached --> so the program ends
# we want the window to persist until the user chooses to close it
# Monitor user events using pygame.event.get()
# This returns a list of events that we can loop through until we get to the QUIT type
running = True
waitingToStart = True

def update_game():
    global running, waitingToStart, snake, velocityY, velocityX, last_move_time, snake_body, score
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            return False

    gesture = tracker.get_gesture()

    if waitingToStart:
        screen.fill(background)

        text = font.render("Show open hand to start!", True, (0, 0, 0))
        screen.blit(text, (120, 220))
        pygame.display.update()

        if gesture == "OPEN_HAND":
            waitingToStart = False
        return True

    # Update velocity based on gesture (don't check boundaries here)
    if gesture == "LEFT" and velocityX != 1:  # Can't go left if moving right
        velocityX = -1
        velocityY = 0
    if gesture == "RIGHT" and velocityX != -1:  # Can't go right if moving left
        velocityX = 1
        velocityY = 0
    if gesture == "UP" and velocityY != 1:  # Can't go up if moving down
        velocityX = 0
        velocityY = -1
    if gesture == "DOWN" and velocityY != -1:  # Can't go down if moving up
        velocityX = 0
        velocityY = 1

    # Move the snake at regular intervals
    current_time = pygame.time.get_ticks()
    if current_time - last_move_time > STEP_DELAY:
        # before moving the head
        prev_x = snake.x
        prev_y = snake.y

        # Calculate new position
        new_x = snake.x + velocityX * TILE_SIZE
        new_y = snake.y + velocityY * TILE_SIZE
        
        # Check boundaries before moving
        if 0 <= new_x < WINDOW_WIDTH and 0 <= new_y < WINDOW_HEIGHT:
            snake.x = new_x
            snake.y = new_y

        # update body
        px, py = prev_x, prev_y
        for tile in snake_body:
            tile.x, px = px, tile.x
            tile.y, py = py, tile.y

        #collision
        if snake.x == food.x and snake.y == food.y:
            snake_body.append(Tile(px, py, (137, 134, 213)))
            score += 1

            food.x = random.randint(0, COLUMNS-1) * TILE_SIZE
            food.y = random.randint(0, ROWS-1) * TILE_SIZE
        
        last_move_time = current_time



    screen.fill(background)
    pygame.draw.rect(screen, (30, 30, 36), (food.x, food.y, TILE_SIZE, TILE_SIZE))
    
    pygame.draw.rect(screen, (137, 134, 213), (snake.x, snake.y, TILE_SIZE, TILE_SIZE))
    pygame.draw.rect(screen, (0, 0, 0), (snake.x, snake.y, TILE_SIZE, TILE_SIZE), 2)  # Black border

    for tile in snake_body:
        pygame.draw.rect(screen, (137, 134, 213), (tile.x, tile.y, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(screen, (0, 0, 0), (tile.x, tile.y, TILE_SIZE, TILE_SIZE), 1) 
    
    pos_text = font.render(f"X: {snake.x}  Y: {snake.y}", True, (255, 0, 255))
    screen.blit(pos_text, (10, 10))

    gesture_text = font.render(f"Gesture: {gesture}", True, (255, 0, 255))
    screen.blit(gesture_text, (10, 40))

    score_text = font.render(f"Score: {score}", True, (255, 0, 255))
    screen.blit(score_text, (10,70))
    
    pygame.display.flip()
    return running

# Run camera loop with pygame updates integrated (both on main thread)
tracker.camera_loop(update_callback=update_game)

pygame.quit()






