from time import strftime
import os
import gobject
import socket
import gtk

# X position of the window
# left side of screen would be '0'
x = gtk.gdk.display_get_default().get_default_screen().get_width() - 250 #right side of the screen, 250 if the svg width

# Y position of the window
y = 100

# Run shell command and clean up line breakers
def run(command):
	return os.popen(command).read().replace('\n','')

# Config vars used to change the svg content.
vars = {}

# This one won't change with time, so it will be kept out of a loop
vars['system'] = run('whoami') + '@' + run('uname -n')

def cpu():
	return run("free -m | grep buffers/cache: | awk '{ print $3 }'")

def ram():
	used = run("free -m | grep buffers/cache: | awk '{ print $3 }'")
	total = run("free -mo | grep Mem: | awk '{ print $2 }'")
	return used + "/" + total + "mb"

def swap():
	used = run("free -mo | grep Swap: | awk '{ print $3 }'")
	total = run("free -mo | grep Swap: | awk '{ print $2 }'")
	return used + "/" + total + "mb"

# In order to keep values changing, use this scructure. Create as many as you need
def update():
	vars['time'] = strftime("%H:%M:%S")
	vars['ram'] = ram()
	vars['swap'] = swap()
	#vars['cpu'] = cpu()
	
	# Keep gobject running
	return True

def slowerUpdate():
	vars['uptime'] = run("uptime | awk '{ print $3 }' | sed 's/,//g'")
	vars['localIp'] = socket.gethostbyname_ex(socket.gethostname())[2][0]
	vars['date'] = run('date +%Y-%m-%d')
	
	# Keep gobject running
	return True

# First loop
update()
slowerUpdate()

# Run update functions over and over again
gobject.timeout_add(1000,update) #run every second
gobject.timeout_add(1000*60,slowerUpdate) #run every minute
