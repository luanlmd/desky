import cairo
import rsvg
import gtk
from gtk import gdk
from time import sleep
import xml.dom.minidom
import sys
import config
import random
import string
import gobject
import time

class Desky(gtk.DrawingArea):

	def __init__(self):
		super(Desky, self).__init__()
		self.dom = None
		self.ctx = None
		self.win = None
		self.main()

	def draw(self, ctx):
		
		print "drawning"

		# Look for new values in the config
		for v in config.vars:
			e = self.dom.getElementById(v)
			e = e.getElementsByTagName("tspan")[0].childNodes[0]

			# Change the svg using the config value
			e.data = config.vars[v]

		# Clean up the config var. In the next loop only new values will be reset
		config.vars = {}
	
		svg = rsvg.Handle(data=self.dom.toxml())
		svg.render_cairo(ctx)

	def expose(self, win, event):
		ctx = win.window.cairo_create()
		self.draw(ctx)
		
		gobject.timeout_add(1000,self.update)
		return False
		
	def update(self):
		if self.window:
			alloc = self.get_allocation()
			rect = gdk.Rectangle(alloc.x, alloc.y, alloc.width, alloc.height)
			self.window.invalidate_rect(rect, True)
		return True

	def main(self):
	
		# Creating window object and setting some configs
		#win = gtk.Window()
		#self.win = win
		#win = gtk.Window(gtk.WINDOW_POPUP)
		#win.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("blue"))
		#win.set_keep_below(True)
		#win.set_decorated(False)
		#win.set_property('skip-taskbar-hint', True)
		#win.connect("destroy", lambda w: gtk.main_quit())
		#win.stick()

		# Open 
		self.dom = xml.dom.minidom.parse('%s/theme.svg' % sys.path[0])
		
		# Make id be the id
		for t in self.dom.getElementsByTagName('text'):
			t.setIdAttribute('id')
				
		# Setting window size
		svge = self.dom.getElementsByTagName('svg')[0]
		width = svge.attributes['width'].value
		height = svge.attributes['height'].value
		self.connect("expose_event", self.expose)
	
		# Setting window position
		#win.resize(int(width),int(height))
		#win.move(config.x, config.y)

		# Opening window
		#win.show_all()
		#gtk.main()

if __name__ == '__main__':
    win = gtk.Window()
    desky = Desky()

    win.add(desky)
    win.connect("destroy", gtk.main_quit)
    win.show_all()

    gtk.main()

	
	
