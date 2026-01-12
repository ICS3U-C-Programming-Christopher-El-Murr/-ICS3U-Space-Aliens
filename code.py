#!/usr/bin/env python3
# Created By: Christopher El-Murr
# Date: 11 08, 2025
import ugame
import stage

    # define the main funciton
def game_scene():
    # image banks for circuit python
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")
    # sets up the background image to 0 
    #and the size (10/8 tiles of size 16x16)
    background = stage.Grid(image_bank_background, 10, 8)

    ship = stage.Sprite(image_bank_sprites, 5, 75, 66)
    #creates the stage for background
    #and sets the frame rate to 60fps
    game = stage.Stage(ugame.display, 60)
    #sets the layers in order
    game.layers = [ship] + [background]
    #renders the background and initial sprites
    game.render_block()

    #repeats forever, game loop
    while True:
        #get user input
        keys = ugame.buttons.get_pressed()
        if keys & ugame.K_X:
            print ("A")
            # if the X button is pressed, print "A"
        if keys & ugame.K_O:
            print("B")
            # if the O button is pressed, print "B"
        if keys & ugame.K_START:
            print("Start")
            # if the start button is pressed, print "Start"
        if keys & ugame.K_SELECT:
            print("Select")
            # if the select button is pressed, print "Select"
        if keys & ugame.K_RIGHT:
            ship.move(ship.x + 1 ship.y)
            # if the right button is pressed, move the ship right
        if keys & ugame.K_LEFT:
            ship.move(ship.x - 1 ship.y)
            # if the left button is pressed, move the ship left
        if keys & ugame.K_UP:
            ship.move(ship.x ship.y - 1)
            # if the up button is pressed, move the ship up
        if keys & ugame.K_DOWN:
            ship.move(ship.x ship.y + 1)
            # if the down button is pressed, move the ship down
        #update game logic
        #redraw Sprites
        game.render_sprites([ship])
        game.tick()
        pass
   
if __name__ == '__main__':
    game_scene()