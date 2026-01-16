#!/usr/bin/env python3
# Created By: Christopher El-Murr
# Date: 11 08, 2025
# this program is the "Space Aliens" game for the PyBadge

import ugame
import stage
import time
import random
import constants
import supervisor


def splash_scene():
    coin_sound = open("coin.wav", "rb")
    sound = ugame.audio
    sound.stop()
    sound.mute(False)
    sound.play(coin_sound)

    image_bank = stage.Bank.from_bmp16("mt_game_studio.bmp")
    background = stage.Grid(
        image_bank, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )

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

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = [background]
    game.render_block()

    time.sleep(2.0)
    menu_scene()


def menu_scene():
    image_bank = stage.Bank.from_bmp16("space_aliens_background.bmp")
    background = stage.Grid(
        image_bank, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )

    text = []

    text1 = stage.Text(width=29, height=14)
    text1.move(20, 20)
    text1.text("ALIEN HUNT")
    text.append(text1)

    text2 = stage.Text(width=29, height=14)
    text2.move(30, 60)
    text2.text("PRESS START")
    text.append(text2)

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = text + [background]
    game.render_block()

    while True:
        keys = ugame.buttons.get_pressed()
        if keys & ugame.K_START:
            game_scene()
        game.tick()


def game_scene():

    # helper function to place a new alien

    # for score
    score = 0

    score_text = stage.Text(width=29, height=14)
    score_text.clear()
    score_text.cursor(0, 0)
    score_text.move(1, 1)
    score_text.text("Score: {0}".format(score))

    def show_alien():
        for alien_number in range(len(aliens)):
            if aliens[alien_number].x < 0:
                aliens[alien_number].move(
                    random.randint(0, constants.SCREEN_X - constants.SPRITE_SIZE),
                    constants.OFF_TOP_SCREEN,
                )
                break

    # load image banks
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    # button states
    a_button = constants.button_state["button_up"]

    # sound setup
    pew_sound = open("pew.wav", "rb")
    sound = ugame.audio
    sound.stop()
    sound.mute(False)

    # background grid
    background = stage.Grid(
        image_bank_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )

    # random background tiles
    for x_location in range(constants.SCREEN_GRID_X):
        for y_location in range(constants.SCREEN_GRID_Y):
            tile_picked = random.randint(1, 3)
            background.tile(x_location, y_location, tile_picked)

    # player ship
    ship = stage.Sprite(
        image_bank_sprites, 5, 75, constants.SCREEN_Y - (2 * constants.SPRITE_SIZE)
    )

    # aliens list
    aliens = []
    for alien_number in range(constants.TOTAL_NUMBER_OF_ALIENS):
        a_single_alien = stage.Sprite(
            image_bank_sprites, 9, constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y
        )
        aliens.append(a_single_alien)
        show_alien()

    # lasers list
    lasers = []
    for laser_number in range(constants.TOTAL_NUMBER_OF_LASERS):
        laser = stage.Sprite(
            image_bank_sprites, 10, constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y
        )
        lasers.append(laser)

    # stage setup
    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = [score_text] + lasers + [ship] + aliens + [background]
    game.render_block()

    # main game loop
    while True:
        keys = ugame.buttons.get_pressed()

        # A button (PyBadge uses K_X)
        if keys & ugame.K_X:
            if a_button == constants.button_state["button_up"]:
                a_button = constants.button_state["button_just_pressed"]
        else:
            a_button = constants.button_state["button_up"]

        # move ship right
        if keys & ugame.K_RIGHT:
            if ship.x <= constants.SCREEN_X - constants.SPRITE_SIZE:
                ship.move(ship.x + 1, ship.y)

        # move ship left
        if keys & ugame.K_LEFT:
            if ship.x >= 0:
                ship.move(ship.x - 1, ship.y)

        # fire laser
        if a_button == constants.button_state["button_just_pressed"]:
            for laser in lasers:
                if laser.x < 0:
                    laser.move(ship.x, ship.y)
                    sound.play(pew_sound)
                    break

        # move lasers
        for laser in lasers:
            if laser.x > 0:
                laser.move(laser.x, laser.y - constants.LASER_SPEED)
                if laser.y < constants.OFF_TOP_SCREEN:
                    laser.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)

        # move aliens
        for alien_number in range(len(aliens)):
            if aliens[alien_number].x > 0:
                aliens[alien_number].move(
                    aliens[alien_number].x,
                    aliens[alien_number].y + constants.ALIEN_SPEED,
                )

                # alien off screen → respawn
                if aliens[alien_number].y > constants.SCREEN_Y:
                    aliens[alien_number].move(
                        constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y
                    )
                    show_alien()
                    score -= 1
                    if score < 0:
                        score = 0
                    score_text.clear()
                    score_text.cursor(0, 0)
                    score_text.move(1, 1)
                    score_text.text("Score: {0}".format(score))

                    for laser_number in range(len(lasers)):
                        for alien_number in range(len(aliens)):
                            if stage.collide(
                                lasers[laser_number].x + 6,
                                lasers[laser_number].y + 2,
                                lasers[laser_number].x + 11,
                                lasers[laser_number].y + 12,
                                aliens[alien_number].x + 1,
                                aliens[alien_number].y,
                                aliens[alien_number].x + 15,
                                aliens[alien_number].y + 15,
                            ):

                                # when laser hits alien
                                aliens[alien_number].move(
                                    constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y
                                )
                                lasers[laser_number].move(
                                    constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y
                                )
                                sound.stop()
                                sound.play(boom_sound)
                                show_alien()
                                show_alien()
                                score = score + 1
                                score_text.clear()
                                score_text.cursor(0, 0)
                                score_text.move(1, 1)
                                score_text.text("Score: {0}".format(score))

                                # each frame check  if any aliens are touching the space ship
                                for alien_number in range(len(aliens)):
                                    if [alien_number].x > 0:
                                        if stage.collide(
                                            aliens[alien_number].x + 1,
                                            aliens[alien_number].y,
                                            aliens[alien_number].x + 15,
                                            aliens[alien_number].y + 15,
                                            ship.x,
                                            ship.y,
                                            ship.x + 15,
                                            ship.y + 15,
                                        ):

                                            sound.play(crash_sound)
                                            time.sleep(3.0)
            game_over_scene(score)

            def game_over_scene(final_score):
                # this function handles the game over scene

                # image bank for circuit python
                image_bank_2 = stage.Bank.from_bmp16("mt_game_studio.bmp")

                # sets the background to image 0 in the bank
                background = stage.Grid(
                    image_bank_2, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
                )

                # add text objects
                text = []
                text1 = stage.Text(
                    width=29,
                    height=14,
                    font=None,
                    palette=constants.BLUE_PALETTE,
                    buffer=None,
                )
                text1.move(22, 20)
                text1.text("Final Score: {:0>2d}".format(final_score))
                text.append(text1)

                text2 = stage.Text(
                    width=29,
                    height=14,
                    font=None,
                    palette=constants.BLUE_PALETTE,
                    buffer=None,
                )
                text2.move(43, 60)
                text2.text("GAME OVER")
                text.append(text2)

                text3 = stage.Text(
                    width=29,
                    height=14,
                    font=None,
                    palette=constants.BLUE_PALETTE,
                    buffer=None,
                )
                text3.move(32, 110)
                text3.text("PRESS SELECT")
                text.append(text3)

                # create the stage for the game over scene
                game = stage.Stage(ugame.display, constants.FPS)
                # set the layers
                game.layers = text + [background]
                # render the background
                game.render_block()

                # repeat forever
                while True:
                    # get user input
                    keys = ugame.buttons.get_pressed()
                    # start button slected
                    if keys & ugame.K_SELECT:
                        supervisor.reload()

                    # update game logic
                    game.tick()


if __name__ == "__main__":
    splash_scene()
