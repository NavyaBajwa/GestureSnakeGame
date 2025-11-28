import os
os.environ['OPENCV_AVFOUNDATION_SKIP_AUTH'] = '1'

import pygame
from webcamGestures import HandGestureTracker
from tile import Tile

pygame.init()
pygame.font.init()

font = pygame.font.SysFont(None, 24)

ROWS = 25
COLUMNS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE*COLUMNS
WINDOW_HEIGHT = TILE_SIZE*ROWS


# create the pygame window: need width and height
(width, height) = (WINDOW_WIDTH, WINDOW_HEIGHT) 
screen = pygame.display.set_mode((width, height)) # pygame window object
pygame.display.set_caption("Snakey's got Hands") # set window title
background = (245, 250, 195) 
#screen.fill(background) # set background colour

# set up initial snake
snake = Tile(5*TILE_SIZE, 5*TILE_SIZE)
vel = 8 # specify speed

# Draw initial frame
screen.fill(background)
pygame.draw.rect(screen, (255, 0, 0), (snake.x, snake.y, TILE_SIZE, TILE_SIZE))
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
    global running, waitingToStart, snake
    
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

    #keys = pygame.key.get_pressed()
    if gesture == "LEFT" and (snake.x > 0):
        snake.x -= vel
    if gesture == "RIGHT" and (snake.x < 500 - TILE_SIZE):
        snake.x += vel
    if gesture == "UP" and (snake.y > 0):
        snake.y -= vel
    if gesture == "DOWN" and (snake.y < 500 - TILE_SIZE):
        snake.y += vel

    screen.fill(background)
    pygame.draw.rect(screen, (255, 0, 0), (snake.x, snake.y, TILE_SIZE, TILE_SIZE))
    
    pos_text = font.render(f"X: {snake.x}  Y: {snake.y}", True, (255, 0, 255))
    screen.blit(pos_text, (10, 10))

    gesture_text = font.render(f"Gesture: {gesture}", True, (255, 0, 255))
    screen.blit(gesture_text, (10, 40))
    
    pygame.display.flip()
    return running

# Run camera loop with pygame updates integrated (both on main thread)
tracker.camera_loop(update_callback=update_game)

pygame.quit()






