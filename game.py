OPENCV_AVFOUNDATION_SKIP_AUTH=1

import pygame
from webcamGestures import HandGestureTracker

pygame.init()
pygame.font.init()

font = pygame.font.SysFont(None, 24)

# create tracker object
tracker = HandGestureTracker()
tracker.start()

# create the pygame window: need width and height
(width, height) = (500, 500) 
screen = pygame.display.set_mode((width, height)) # pygame window object

pygame.display.set_caption("Snakey's got Hands") # set window title
background = (245, 250, 195) 
screen.fill(background) # set background colour

pygame.display.flip() # to dispay the screen

# set up initial snake
(x, y) = (200,200) # specify position of initial square
(sWidth, sHeight) = (20,20) # specify size
vel = 7 # specify speed

# once flip() is called, the end of the program is reached --> so the program ends
# we want the window to persist until the user chooses to close it
# Monitor user events using pygame.event.get()
# This returns a list of events that we can loop through until we get to the QUIT type
running = True
while running:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    gesture = tracker.get_gesture()

    keys = pygame.key.get_pressed() # returns a list of boolean values of the current state of every key
    if keys[pygame.K_LEFT] and (x > 0): # later you'll do if gesture = left
        x -= vel
    if keys[pygame.K_RIGHT] and (x < 500 - width):
        x += vel
    if keys[pygame.K_UP] and (y > 0):
        y -= vel
    if keys[pygame.K_DOWN] and (y < 500 - height):
        y += vel

    screen.fill(background) # this will refill the background so the previous square isn't shown
    pygame.draw.rect(screen, (255, 0, 0), (x, y, sWidth, sHeight))
    
    pos_text = font.render(f"X: {x}  Y: {y}", True, (255, 0, 255))
    screen.blit(pos_text, (10, 10))

    gesture_text = font.render(f"Gesture: {gesture}", True, (255, 0, 255))
    screen.blit(gesture_text, (50, 50))
    
    pygame.display.update()

tracker.stop()






