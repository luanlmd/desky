import cairo
import rsvg
import gtk
from time import sleep
import xml.dom.minidom
import sys

def expose(win, event, dom):
	ctx = win.window.cairo_create()

	if win.is_composited() == False:
		ctx.set_source_rgb(1, 1, 1)
		print "no alpha mode available"
	else:
		ctx.set_source_rgba(1, 1, 1, 0)
		print "alpha mode enabled"

	for v in config.vars:
		e = dom.getElementById(v)
		e = e.getElementsByTagName("tspan")[0].childNodes[0]
		e.data = config.vars[v]
	
	print "rendering"
	
	open('/tmp/tmp.svg','w').write(dom.toxml())
	svg = rsvg.Handle(file="/tmp/tmp.svg")
	svg.render_cairo(ctx)
	
	return True

def main():
	theme = sys.argv[1]
	theme = theme[0].upper() + theme[1:]
		
	#win = gtk.Window(gtk.WINDOW_POPUP)
	win = gtk.Window()
	win.set_keep_below(True)
	win.connect("destroy", lambda w: gtk.main_quit())
	win.set_decorated(False)

	dom = xml.dom.minidom.parseString(open('theme%s.svg' % theme).read())
	for t in dom.getElementsByTagName('text'):
			t.setIdAttribute('id')
			
	svge = dom.getElementsByTagName('svg')[0]

	width = svge.attributes['width'].value
	height = svge.attributes['height'].value
	
	win.resize(int(width),int(height))
	win.move(config.x, config.y)
	#win.skip_taskbar_hint(True)

	win.connect("expose-event", expose, dom)
	win.show_all()
	gtk.main()

if __name__ == '__main__':
	theme = sys.argv[1]
	theme = theme[0].upper() + theme[1:]
	exec('import theme%s as config' % theme)
	main()
	
