import rsvg
import gtk
import xml.dom.minidom
import sys
import time
from math import floor
import cairo
import gobject
import imp

#import config
import widget

class Desky():

	def __init__(self, theme):

		self.win = widget.Window()

		self.dom = xml.dom.minidom.parse('%s/themes/%s/theme.svg' % (sys.path[0], theme))
		self.config = imp.load_source('__main__', '%s/themes/%s/script.py' % (sys.path[0], theme))
		
		# Make id be the id
		for t in self.dom.getElementsByTagName('text'):
			t.setIdAttribute('id')
				
		# Setting window size
		svge = self.dom.getElementsByTagName('svg')[0]
		width = svge.attributes['width'].value
		height = svge.attributes['height'].value
		
		# Setting window position
		self.win.resize(int(floor(float(width))),int(floor(float(height))))
		self.win.move(self.config.x, self.config.y)

		# Set the new draw function to the window
		self.win.draw = self.draw
		
		# Tell the window to update and draw
		self.update()
		gobject.timeout_add(self.config.updateInterval,self.update)
		
		self.win.show_all()
		gtk.main()
	
	def update(self):
		self.win.update()
		return True	
	
	def draw(self, cr):
		
		print "setting values"

		# Look for new values in the self.config
		for v in self.config.vars:
			e = self.dom.getElementById(v)
			e = e.getElementsByTagName("tspan")[0].childNodes[0]

			# Change the svg using the self.config value
			print "setting: %s = %s" % (v, self.config.vars[v])
			e.data = self.config.vars[v]
			

		# Clean up the self.config var. In the next loop only new values will be reset
		self.config.vars = {}
	
		cr.set_operator(cairo.OPERATOR_OVER) 
		svg = rsvg.Handle(data=self.dom.toxml())
		
		print "drawning"
		svg.render_cairo(cr)
				
if __name__ == '__main__':	
	if sys.argv.__len__() > 1:
		theme = sys.argv[1]
	else:
		theme = 'default'
		
	desky = Desky(theme)
	
