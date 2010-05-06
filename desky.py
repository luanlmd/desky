import cairo
import rsvg
import gtk
from time import sleep
from time import strftime
import xml.dom.minidom

def expose(win, event, dom):
	cr = win.window.cairo_create()
	cr.set_source_color(win.style.fg[win.state])

	e = dom.getElementById("var1")
	e = dom.getElementsByTagName("tspan")[0].childNodes[0]
	e.data = strftime("%H:%M:%S")
	print "renderizou" + e.data
	open('/tmp/test.svg','w').write(dom.toxml())
	
	svg = rsvg.Handle(file="/tmp/test.svg")
	svg.render_cairo(cr)
	
	return True

def main():

	win = gtk.Window()
	win.connect("destroy", lambda w: gtk.main_quit())

	dom = xml.dom.minidom.parseString(open('test.svg').read())

	win.connect("expose-event", expose, dom)
	win.show_all()
	gtk.main()

	"""while True:
		print "true"
		sleep(1)
	"""

if __name__ == '__main__':
    main()
