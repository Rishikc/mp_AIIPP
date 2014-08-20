'''
Created on Aug 20, 2014

@author: victorzhao
'''

# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import random
import simplegui
import math

# initialize global variables used in your code
secretnum = 0
# number of remaining guesses
numremgue = 0

# helper function to start and restart the game
def new_game(low, high):
    """ Reset the current game, and set secret number to """ 
    """ a new value within the range provided """
    global secretnum, numremgue
    print "New game. Range is from", low, "to", high
    secretnum = random.randrange(low, high)
    numremgue = int(math.ceil(math.log(high - low + 1, 2)))
    print "Number of remaining guesses is", numremgue 
    print ""
    
# define event handlers for control panel
def range100():
    # button that changes range to range [0,100) and restarts
    new_game(0, 100)

def range1000():
    # button that changes range to range [0,1000) and restarts
    new_game(0, 1000)
    
def input_guess(guess):
    # main game logic goes here    
    global numremgue
    print "Guess was", guess
    print "Number of remaining guesses is", numremgue
    # convert string into number
    guessnum = int(guess)
    # game logic
    if numremgue != 0:
        if guessnum > secretnum:
            print "Lower!"
            print ""
            numremgue = numremgue - 1
        elif guessnum < secretnum:
            print "Higher!"
            print ""
            numremgue = numremgue - 1
        else:
            # guessnum == secretnum
            print "Correct!"
            print ""
            new_game(0, 100)
    # ran out of guesses scenario
    else:
        if guessnum == secretnum:
            print "Correct!"
            print ""
        else:
            print "You ran out of guesses. The number was", secretnum
            print ""
        new_game(0, 100)   

# create frame
f = simplegui.create_frame("Guess the number!", 200, 200)

# register event handlers for control elements
f.add_button("Range: [0, 100)", range100, 200)
f.add_button("Range: [0, 1000)", range1000, 200)
f.add_input("Enter a guess", input_guess, 200)

# call new_game and start frame
f.start()
range100()

# always remember to check your completed program against the grading rubric
