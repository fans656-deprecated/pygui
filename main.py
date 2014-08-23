from pygui import *

# [update on 2014-08-23 16:53:55]
# this is not universally appliable
# the semantics of text() or circle() could
# magically mean two different things:
#   1. do it now
#   2. as a callback
# but if the user define his own function,
# due to Python's eager evaluation strategy, f(1, 2) in
#   key('a', f(1, 2))
# will be called and what passed to key() is the returned value
# you can only change this by extra explicit machanism (e.g. decorator)
# but that would lose the meaning of text() being magical
#
# SO, the CONCLUSION is: we can't omit the do() notation
#

# try to implement this:
# when called as standalone, text() append to draw
# when used as Do, it deferred

a = text('apple') + circle((200, 100), 20) 
b = text('banana') + circle((500, 200), 50)

text('press a or b')
text('to draw things') # this will draw two lines of text

key('a', a) # draw when press a
key('b', b) # draw when press b

circle((50, 50), 10)
circle((50, 80), 10) # this will draw two circles
