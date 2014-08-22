from pygui import *

a = do(text, 'apple') + do(circle, (200, 100), 20)
b = do(text, 'banana') + do(circle, (500, 200), 50)

text('press a or b')
key('a', a)
key('b', b)
