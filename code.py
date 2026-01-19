#!/usr/bin/env python3
# Created By: Christopher El-Murr
# Date: 11 08, 2025
# Space Aliens game for the PyBadge

import ugame  # PyBadge game library for buttons and audio
import stage  # PyBadge library for graphics
import time  # used for delays
import random  # used for random alien positions
import constants  # game constants like screen size, speeds, etc.
import supervisor  # used to reload the game after game over


# -----------------------------
# SPLASH SCENE
# -----------------------------
def splash_scene():
    # Play coin sound at start
    coin_sound = open("coin.wav", "rb")
    sound = ugame.audio
    sound.stop()
    sound.mute(False)
    coin_sound.seek(0)  # rewind file before playing
    sound.play(coin_sound)

    # Load splash screen background
    image_bank = stage.Bank.from_bmp16("mt_game_studio.bmp")
    background = stage.Grid(
        image_bank, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )

    # Place tiles for splash screen layout
    background.tile(2, 2, 0)
    background.tile(3, 2, 1)
    background.tile(4, 2, 2)
    background.tile(5, 2, 3)
    background.tile(6, 2, 4)
    background.tile(7, 2, 0)
    background.tile(2, 3, 0)
    background.tile(3, 3, 5)
    background.tile(4, 3, 6)
    background.tile(5, 3, 7)
    background.tile(6, 3, 8)
    background.tile(7, 3, 0)
    background.tile(2, 4, 0)
    background.tile(3, 4, 9)
    background.tile(4, 4, 10)
    background.tile(5, 4, 11)
    background.tile(6, 4, 12)
    background.tile(7, 4, 0)
    background.tile(2, 5, 0)
    background.tile(3, 5, 0)
    background.tile(4, 5, 13)
    background.tile(5, 5, 14)
    background.tile(6, 5, 0)
    background.tile(7, 5, 0)

    # Create game stage and render
    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = [background]
    game.render_block()

    time.sleep(2.0)  # show splash screen for 2 seconds
    menu_scene()  # move to main menu


# -----------------------------
# MENU SCENE
# -----------------------------
def menu_scene():
    # Load menu background
    image_bank = stage.Bank.from_bmp16("space_aliens_background.bmp")
    background = stage.Grid(
        image_bank, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )

    text = []

    # Display title
    title = stage.Text(width=29, height=14)
    title.move(20, 20)
    title.text("SPACE ALIENS")
    text.append(title)

    # Display "PRESS START"
    start = stage.Text(width=29, height=14)
    start.move(30, 60)
    start.text("PRESS START")
    text.append(start)

    # Create game stage
    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = text + [background]
    game.render_block()

    # Wait for player to press START
    while True:
        keys = ugame.buttons.get_pressed()
        if keys & ugame.K_START:
            game_scene()
        game.tick()


# -----------------------------
# GAME OVER SCENE
# -----------------------------
def game_over_scene(final_score):
    # Load background
    image_bank = stage.Bank.from_bmp16("mt_game_studio.bmp")
    background = stage.Grid(
        image_bank, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )

    text = []

    # Display "GAME OVER"
    game_over = stage.Text(width=29, height=14)
    game_over.move(30, 30)
    game_over.text("GAME OVER")
    text.append(game_over)

    # Display final score
    score_text = stage.Text(width=29, height=14)
    score_text.move(10, 60)
    score_text.text("FINAL SCORE: {}".format(final_score))
    text.append(score_text)

    # Prompt to restart
    restart = stage.Text(width=29, height=14)
    restart.move(10, 100)
    restart.text("PRESS SELECT")
    text.append(restart)

    # Create stage
    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = text + [background]
    game.render_block()

    # Wait for SELECT button to restart
    while True:
        keys = ugame.buttons.get_pressed()
        if keys & ugame.K_SELECT:
            supervisor.reload()  # reload entire game
        game.tick()


# -----------------------------
# MAIN GAME SCENE
# -----------------------------
def game_scene():
    score = 0
    sound_muted = False

    # Score display
    score_text = stage.Text(width=29, height=14)
    score_text.move(1, 1)

    # Function to show an alien on screen
    def show_alien():
        for alien in aliens:
            if alien.x < 0:  # find an off-screen alien
                alien.move(
                    random.randint(0, constants.SCREEN_X - constants.SPRITE_SIZE),
                    constants.OFF_TOP_SCREEN,
                )
                break

    # Load images
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    # Track fire button state
    a_button = constants.button_state["button_up"]

    # Load sounds
    pew_sound = open("pew.wav", "rb")  # laser
    boom_sound = open("boom.wav", "rb")  # explosion
    sound = ugame.audio
    sound.stop()
    sound.mute(False)

    # Setup background grid
    background = stage.Grid(
        image_bank_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )
    for x in range(constants.SCREEN_GRID_X):
        for y in range(constants.SCREEN_GRID_Y):
            background.tile(x, y, random.randint(1, 3))

    # Setup player ship
    ship = stage.Sprite(
        image_bank_sprites, 5, 75, constants.SCREEN_Y - (2 * constants.SPRITE_SIZE)
    )

    # Setup aliens
    aliens = []
    for _ in range(constants.TOTAL_NUMBER_OF_ALIENS):
        alien = stage.Sprite(
            image_bank_sprites, 9, constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y
        )
        aliens.append(alien)
        show_alien()

    # Setup lasers
    lasers = []
    for _ in range(constants.TOTAL_NUMBER_OF_LASERS):
        laser = stage.Sprite(
            image_bank_sprites, 10, constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y
        )
        lasers.append(laser)

    # Setup game stage layers
    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = [score_text] + lasers + [ship] + aliens + [background]
    game.render_block()

    # -----------------------------
    # GAME LOOP
    # -----------------------------
    while True:
        keys = ugame.buttons.get_pressed()

        # B button toggles mute
        if keys & ugame.K_O:
            sound_muted = not sound_muted
            sound.mute(sound_muted)
            # wait until button is released to avoid multiple toggles
            while ugame.buttons.get_pressed() & ugame.K_O:
                game.tick()

        # Fire button handling
        if keys & ugame.K_X:
            if a_button == constants.button_state["button_up"]:
                a_button = constants.button_state["button_just_pressed"]
        else:
            a_button = constants.button_state["button_up"]

        # Move ship left/right
        if keys & ugame.K_RIGHT and ship.x < constants.SCREEN_X - constants.SPRITE_SIZE:
            ship.move(ship.x + 2, ship.y)
        if keys & ugame.K_LEFT and ship.x > 0:
            ship.move(ship.x - 2, ship.y)

        # Fire laser
        if a_button == constants.button_state["button_just_pressed"]:
            for laser in lasers:
                if laser.x < 0:  # find an off-screen laser
                    laser.move(ship.x, ship.y)
                    pew_sound.seek(0)  # rewind laser sound
                    sound.play(pew_sound)  # play laser sound
                    break

        # Move lasers upwards
        for laser in lasers:
            if laser.x >= 0:
                laser.move(laser.x, laser.y - constants.LASER_SPEED)
                if laser.y < constants.OFF_TOP_SCREEN:
                    laser.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)

        # Move aliens downward
        for alien in aliens:
            if alien.x >= 0:
                alien.move(alien.x, alien.y + constants.ALIEN_SPEED)

                # Alien escaped → lose 1 point
                if alien.y > constants.SCREEN_Y:
                    alien.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                    show_alien()
                    score = max(0, score - 1)

                # Alien hit player → GAME OVER
                if stage.collide(
                    ship.x,
                    ship.y,
                    ship.x + constants.SPRITE_SIZE,
                    ship.y + constants.SPRITE_SIZE,
                    alien.x,
                    alien.y,
                    alien.x + constants.SPRITE_SIZE,
                    alien.y + constants.SPRITE_SIZE,
                ):
                    game_over_scene(score)
                    return

        # Laser–alien collisions
        for laser in lasers:
            if laser.x < 0:
                continue
            for alien in aliens:
                if alien.x < 0:
                    continue
                if stage.collide(
                    laser.x + 6,
                    laser.y + 2,
                    laser.x + 11,
                    laser.y + 12,
                    alien.x + 1,
                    alien.y,
                    alien.x + 15,
                    alien.y + 15,
                ):
                    alien.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                    laser.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                    boom_sound.seek(0)  # rewind explosion sound
                    sound.play(boom_sound)
                    show_alien()
                    score += 1
                    break

        # -----------------------------
        # Update score every frame
        # -----------------------------
        score_text.clear()
        score_text.cursor(0, 0)
        score_text.text("Score: {}".format(score))

        # Render sprites
        game.render_sprites(lasers + [ship] + aliens)
        game.tick()


if __name__ == "__main__":
    splash_scene()
