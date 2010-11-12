import rsvg
import gtk
import xml.dom.minidom
import sys
import time
from math import floor
import cairo
import gobject

import config
import widget

class Desky():

	def __init__(self):

		self.win = widget.Window()

		self.dom = xml.dom.minidom.parse('%s/theme.svg' % sys.path[0])
		
		# Make id be the id
		for t in self.dom.getElementsByTagName('text'):
			t.setIdAttribute('id')
				
		# Setting window size
		svge = self.dom.getElementsByTagName('svg')[0]
		width = svge.attributes['width'].value
		height = svge.attributes['height'].value
		
		# Setting window position
		self.win.resize(int(floor(float(width))),int(floor(float(height))))
		self.win.move(config.x, config.y)

		# Set the new draw function to the window
		self.win.draw = self.draw
		
		# Tell the window to update and draw
		self.update()
		gobject.timeout_add(config.updateInterval,self.update)
		
		self.win.show_all()
		gtk.main()
	
	def update(self):
		self.win.update()
		return True	
	
	def draw(self, cr):
		
		print "setting values"

		# Look for new values in the config
		for v in config.vars:
			e = self.dom.getElementById(v)
			e = e.getElementsByTagName("tspan")[0].childNodes[0]

			# Change the svg using the config value
			print "setting: %s = %s" % (v, config.vars[v])
			e.data = config.vars[v]
			

		# Clean up the config var. In the next loop only new values will be reset
		config.vars = {}
	
		cr.set_operator(cairo.OPERATOR_OVER) 
		svg = rsvg.Handle(data=self.dom.toxml())
		
		print "drawning"
		svg.render_cairo(cr)
				
if __name__ == '__main__':
	desky = Desky()
	
