import cairo
import rsvg
import gtk
from time import sleep
import xml.dom.minidom
import sys
import config
import random
import string
import gobject
import time

win = None
dom = None
ctx = None
r_id = None

def draw():
		
	print "drawning"
	
	for v in config.vars:
		e = dom.getElementById(v)
		e = e.getElementsByTagName("tspan")[0].childNodes[0]
		e.data = config.vars[v]

	config.vars = {}

	open('/tmp/%s.svg' % r_id,'w').write(dom.toxml())
	svg = rsvg.Handle(file="/tmp/%s.svg" % r_id)
	svg.render_cairo(ctx)
	
	while gtk.events_pending():
		gtk.main_iteration(False)
	
	#gobject.timeout_add(500,draw)

def expose(win, e, dom):

	global r_id
	r_id = ''.join(random.sample(string.letters, 5))

	global ctx
	ctx = win.window.cairo_create()
	
	if win.is_composited() == False:
		ctx.set_source_rgb(1, 1, 1)
		print "no alpha mode available"
	else:
		ctx.set_source_rgba(1, 1, 1, 0)
		print "alpha mode enabled"

	for t in dom.getElementsByTagName('text'):
		t.setIdAttribute('id')
	
	draw()	

	return True

def main():

	#win = gtk.Window(gtk.WINDOW_POPUP)
	
	# Creating window object and setting some configs
	global win
	win = gtk.Window()
	win.set_keep_below(True)
	win.set_decorated(False)
	win.set_property('skip-taskbar-hint', True)
	win.connect("destroy", lambda w: gtk.main_quit())

	# Open the SVG to look for some data
	global dom
	dom = xml.dom.minidom.parseString(open('theme.svg').read())
				
	# Setting window size
	svge = dom.getElementsByTagName('svg')[0]
	width = svge.attributes['width'].value
	height = svge.attributes['height'].value
	win.connect("expose-event", expose, dom)
	
	# Setting window position
	win.resize(int(width),int(height))
	win.move(config.x, config.y)

	# Opening window
	win.show_all()
	gtk.main()

if __name__ == '__main__':
	main()
	
