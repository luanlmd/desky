from time import strftime
import os
import gobject

# X position of the window
x = 0

# Y position of the window
y = 250

# Config vars used to change the svg content.
vars = {}
vars['system'] = os.popen('uname -on').read()

# In order to keep values changing, use this scructure. Create as many as you need

def update():
	vars['time'] = strftime("%H:%M:%S")
	vars['ram'] = ram()
	vars['swap'] = swap()

	# Keep it running
	return True

def ram():
	used = os.popen("free -mo | grep Mem: | awk '{ print $3 }'").read().replace('\n','')
	total = os.popen("free -mo | grep Mem: | awk '{ print $2 }'").read().replace('\n','')
	return used + "/" + total + "mb"

def swap():
	used = os.popen("free -mo | grep Swap: | awk '{ print $3 }'").read().replace('\n','')
	total = os.popen("free -mo | grep Swap: | awk '{ print $2 }'").read().replace('\n','')
	return used + "/" + total + "mb"

update()

# Calling update() again, 1 second after its been called
gobject.timeout_add(1000,update)
