import rsvg
import gtk
import xml.dom.minidom
import sys
import time
from math import floor
import cairo

import config
import widget

class Desky():

	def __init__(self):

		win = widget.Window()

		self.dom = xml.dom.minidom.parse('%s/theme.svg' % sys.path[0])
		
		# Make id be the id
		for t in self.dom.getElementsByTagName('text'):
			t.setIdAttribute('id')
				
		# Setting window size
		svge = self.dom.getElementsByTagName('svg')[0]
		width = svge.attributes['width'].value
		height = svge.attributes['height'].value
		
		# Setting window position
		win.resize(int(floor(float(width))),int(floor(float(height))))
		win.move(config.x, config.y)

		# Tell the window to draw when it run expose
		win.setDraw(self.draw)
		
		win.show_all()
		gtk.main()
		
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
	
