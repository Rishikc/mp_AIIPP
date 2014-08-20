'''
Created on Aug 20, 2014

@author: victorzhao
'''

# implementation of card game - Memory

import simplegui
import random
l1 = range(8)
l2 = range(8)
l3 = l1 + l2
exposed = range(16)
state = 0
first_card = [0, 0]
second_card = [0, 0]
turns = 0

# helper function to initialize globals
def new_game():
    global l3, turns
    random.shuffle(l3)
    for i in range(len(l3)):
        exposed[i] = False
    turns = 0
    label.set_text('Turns = ' + str(turns))

     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    # print "The No. ", pos[0] // 50, "has been clicked!" 
    global state, first_card, second_card, turns
    if exposed[pos[0] // 50] == False:
        exposed[pos[0] // 50] = True
        if state == 0:
            state = 1
            first_card[1] = l3[pos[0] // 50]
            first_card[0] = pos[0] // 50
        elif state == 1:
            state = 2
            second_card[1] = l3[pos[0] // 50]
            second_card[0] = pos[0] // 50
        else: 
            if first_card[1] != second_card[1]:
                exposed[first_card[0]] = False
                exposed[second_card[0]] = False
                
            state = 1
            first_card[1] = l3[pos[0] // 50]
            first_card[0] = pos[0] // 50
            second_card = [0, 0]
            turns += 1
            label.set_text('Turns = ' + str(turns))
            
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(len(l3)):
        if exposed[i] == False:
            canvas.draw_polygon([[0 + i * 50, 0], 
                                 [50 + i * 50, 0], [50 + i * 50, 100], 
                                 [0 + i * 50, 100]], 1, 'Yellow', 'Green')
        else: 
            canvas.draw_text(str(l3[i]), [20 + 50 * i, 55], 20, 'White', 'serif')


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")


# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric