########################################
# one window

text('hi')

########################################
# two window
# one draw text, one draw circle

def drawA():
    text('hi')

def drawB():
    circle()

canvas(drawA)
canvas(drawB)

########################################
# one window
# left draw text, right draw cicle
# left is two times wider than right

def drawA():
    text('hi')

def drawB():
    circle()

canvas(drawA) * 2 | canvas(drawB)

########################################
# one window
# left draw text, right draw cicle
# left is two times wider than right
# when space is pressed, show/hide the right one

def drawA():
    text('hi')

def drawB():
    circle()

a = canvas(drawA) * 2
b = canvas('b', drawB).hide()
onkey(' ', canvas['b'].toggle)
