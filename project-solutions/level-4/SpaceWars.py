"""Runs the Init.py file and imports the libraries"""
from init import *
import random
import pygame

def update(delta_time):
    """The Update method checks for all the key presses and button clicks"""
    for event in pygame.event.get():
        #Checks if you closed the window
        if event.type == pygame.QUIT:
            stop()
        #Fires the two ships' weapons        
        elif event.type == pygame.KEYDOWN and event.key == ord(" "):
            sound_laser[random.randint(0, len(sound_laser) - 1)].play()
            fire_bullet(1)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            sound_laser[random.randint(0, len(sound_laser) - 1)].play()
            fire_bullet(2)
        #Checks if you click the Replay button to play again
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if MY.restart_button.collides_with_point(pygame.math.Vector2(pos[0], pos[1])):
                Manager.current = 0
                MY.state = 0                

    #Rotates the Player 1 ship
    if pygame.key.get_pressed()[ord("a")]:
        MY.player1.add_rotation(ship_rotate * delta_time)
    #TODO: Copy the code here for the Player 1 ship to rotate clockwise
    elif pygame.key.get_pressed()[ord("d")]:
        MY.player1.add_rotation(-ship_rotate * delta_time)

    #Moves the Player 1 ship forward and backward
    if pygame.key.get_pressed()[ord("w")]:
        MY.player1.add_velocity(MY.player1.rotation, ship_accel, ship_max_speed)
    #TODO: Copy the code here for the Player 1 ship to move backward
    elif pygame.key.get_pressed()[ord("s")]:
        MY.player1.add_velocity(MY.player1.rotation, -ship_accel, ship_max_speed)

    #Rotates the Player 2 ship
    #TODO: Write the code here to rotate the Player 2 ship
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        MY.player2.add_rotation(ship_rotate * delta_time)
    elif pygame.key.get_pressed()[pygame.K_RIGHT]:
        MY.player2.add_rotation(-ship_rotate * delta_time)

    #TODO: Write the code here to move the Player 2 ship
    if pygame.key.get_pressed()[pygame.K_UP]:
        MY.player2.add_velocity(MY.player2.rotation, ship_accel, ship_max_speed)
    elif pygame.key.get_pressed()[pygame.K_DOWN]:
        MY.player2.add_velocity(MY.player2.rotation, -ship_accel, ship_max_speed)

    MY.player1.update(delta_time)
    MY.player2.update(delta_time)

    for i in range(len(MY.asteroids)):
        if MY.asteroids[i].active:
            MY.asteroids[i].update(delta_time)
            screen_wrap(MY.asteroids[i], MY.window)

    # Checks if players are outside of the screen
    screen_wrap(MY.player1, MY.window)
    screen_wrap(MY.player2, MY.window)

    # Update bullets
    for i in range(len(MY.bullets)):
        # ignore if not active
        if MY.bullets[i].active:
            MY.bullets[i].update(delta_time)
            # Destroy bullets that hit the screen edge.
            if screen_wrap(MY.bullets[i], MY.window):
                MY.bullets[i].active = False
                continue

            for j in range(len(MY.asteroids)):
                if MY.bullets[i].collides_with(MY.asteroids[j]):
                    MY.bullets[i].active = False
            
            #check collisions
            check_collision(i)

    for asteroid in MY.asteroids:
        if MY.player1.collides_with(asteroid):
            MY.player1.velocity = pygame.math.Vector2(0, 0)

        if MY.player2.collides_with(asteroid):
            MY.player2.velocity = pygame.math.Vector2(0, 0)

    # Check win condition
    check_win()


# states
import SpaceWars
Manager.register(SpaceWars)
Manager.register(restarter_player1)
Manager.register(restarter_player2)

# run the game!
Manager.run(SCREEN, WINDOW, BLACK)
