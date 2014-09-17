from pygui import *

import record

class Model:

    def init(self):
        self.records = record.Records()
        self.spans = self.formatedSpans()

    def drawRecord(self):
        # setFont only has effect in THIS context
        setFont('Inconsolata', height() / 3)
        colors = config.spanColors
        for span, color in zip(self.spans, colors):
            # when called multipy times in the same context
            # it put multiple line
            drawText(span, config.color)

    def drawStatistics(self):
        spans = [r.totalSeconds() for r in self.records]
        maxSpan = config.expectedSpan.total_seconds()
        # drawHistogram(list, max=None) take a list of numbers
        # and draw a histogram
        # if bound is not specified, it will use the max of the list
        # Return a statistics object, see the usage below
        stat = drawHistogram(spans, bound=maxSpan)
        # stat.bound() return the bound used by drawHistogram()
        # it can be used to draw a line, or extract the data
        # like stat.bound().line().x() or float(stat.bound())
        drawLine(stat.bound())
        drawLine(stat.average())

    def update(self):
        self.records.update()
        spans = self.records.todayRecord().formatedSpans()
        if self.spans != spans:
            self.spans = spans
            return True
        else:
            return False

    def toggle(self):
        self.records.toggle()

m = Model()

# canvas(name, drawer) will return a canvas with that name
a = canvas('record', m.drawRecord)
# Canvas.hide() will hide the canvas
b = canvas('statistics', m.drawStatistics).hide()
# canvas composition is specified using `+` and `*`
#   a + b stack a and b horizontally
#   a * b stack a and b vertically
#   canvas[weight] specify the relative width/height weight in the stack
# e.g. the height(due to the `*`) ratio of a and b is 2:1
a[2] * b

# state(s1, s2, ..) will add a state group
# StateGroup.switch will iterate over the states,
# and by default it will change the application title
#   for more elavorated usage, StateGroup can be assigned a name
#   and its state too
#   then the StateGroup can be refered like this:
#   setTitle('MyApp @State in @EditMode')
# do(func) + do(func) is merely for lambda composition
onkey(' ', do(m.toggle) + do(state('Running', 'Stopped').switch))
# canvas[name] return the Canvas with that name
# Canvas.toggle will show/hide the canvas
onkey('s', canvas['statistics'].toggle)
onclose(m.toggle)
# ontick(seconds, func) will call the func every `seconds` seconds
ontick(0.1, m.update)
