from time import strftime
import os
import gobject

# X position of the window
x = 0

# Y position of the window
y = 250

# Config vars used to change the svg content.
vars = {}
vars['var2'] = 'Static'
vars['var3'] = os.popen('uname -onv').read()

# In order to keep values changing, use this scructure. Create as many as you need

def update():
	vars['var1'] = strftime("%H:%M:%S")
	print 'update'	
	return True


update()

# Calling update() again, 1 second after its been called
gobject.timeout_add(1000,update)
