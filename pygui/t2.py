# when do we need canvas() ?

# to open multiple window for draw
canvas(drawerA)
canvas(drawerB)

# to split one window into multiple region
canvas(drawerA) * 2 | canvas(drawerB)

########################################

# when do we need a name ?

# to refer
canvas['name']

########################################

# must have a drawer
canvas(drawer)

# optionally have a name
canvas('name', drawer)
# then can be refered using the name
canvas['name']
