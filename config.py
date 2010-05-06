from time import strftime
import os
import gobject
x = 0
y = 250
vars = {}
vars['var2'] = 'Static'
vars['var3'] = os.popen('uname -onv').read()

def update():
	vars['var1'] = strftime("%H:%M:%S")
	gobject.timeout_add(1000,update)

update()

# Update 

