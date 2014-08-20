'''
Created on Aug 20, 2014

@author: victorzhao
'''

# template for "Stopwatch: The Game"
import simplegui
# define global variables
t = 0
x = 0
y = 0
timer_state = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    tenth_seconds = t % 10
    ones_seconds = (t / 10) % 60 % 10
    tens_seconds = (t / 10) % 60 / 10
    minutes = (t / 10) / 60
    return str(minutes) + ':' + str(tens_seconds) + str(ones_seconds) + '.' + str(tenth_seconds)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    """ start the timer and set the state to true"""
    global timer_state
    timer.start()
    timer_state = True
    
def stop():
    """ stop the timer when timer is running, determine the outcome """
    global x, y, timer_state
    if timer_state != False:
        timer.stop()
        timer_state = False
        if t % 10 == 0:
            x = x + 1
            y = y + 1
        else:
            y = y + 1
    
def reset():
    """ stops the timer and reset the current time to zero """
    global t, x, y
    if timer_state != False:
        timer.stop()
        timer.state = True
    t = 0
    x = 0
    y = 0

# define event handler for timer with 0.1 sec interval
def handler_for_timer():
    global t
    t = t + 1

# define draw handler
def draw(canvas):
    canvas.draw_text(format(t), [115, 100], 30, 'White')
    canvas.draw_text(str(x) + '/' + str(y), [250, 20], 20, 'Red')

# create frame
frame = simplegui.create_frame("Stopwatch", 300, 200)

# register event handlers
timer = simplegui.create_timer(100, handler_for_timer)
frame.set_draw_handler(draw)
frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)

# start frame
frame.start()

# Please remember to review the grading rubric
