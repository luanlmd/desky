from time import strftime
import os
x = 0
y = 200
vars = {}
vars['var1'] = strftime("%H:%M:%S")
vars['var2'] = 'Static'
vars['var3'] = os.popen('uname -onv').read()

	
