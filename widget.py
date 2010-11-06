import gtk
import cairo
import gobject

class Window(gtk.Window):

	def expose(self, widget, event):
		
		# Making the window transparent
		cr = widget.window.cairo_create()
		cr.set_operator(cairo.OPERATOR_CLEAR)
		region = gtk.gdk.region_rectangle(event.area)
		cr.region(region)	
		cr.fill()
		
		self.draw(cr)
			
	def setDraw(self, function):
		self.draw = function
	
	def update(self):
	
		# Cleaning up the window so it will call expose-event again
		if self.window:
			alloc = self.get_allocation()
			rect = gtk.gdk.Rectangle(alloc.x, alloc.y, alloc.width, alloc.height)
			self.window.invalidate_rect(rect, True)
		return True

	def __init__(self, *args):
	
		self.draw = lambda:False
	
		gtk.Window.__init__(self, *args)
		self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DOCK)
		self.set_keep_below(True)
		self.stick()
		
		screen = self.get_screen()
		rgba = screen.get_rgba_colormap()
		self.set_colormap(rgba)
		self.set_app_paintable(True)

		self.connect("expose-event", self.expose)
		
		# Keep the window Updating every second
		gobject.timeout_add(1000,self.update)
	
