import gtk
import Widgets

if __name__ == "__main__":

	# register the class as a Gtk widget
	#gobject.type_register(StarHScale)
	
	def stampa(xx,yy,zz):
		print yy

	win = gtk.Window()
	win.resize(200,50)
	win.connect('delete-event', gtk.main_quit)
	
	x = Widgets.SingleEdgeSelector("")
	#x.connect('clicked', stampa)
	win.add(x)
	
	win.show_all()    
	gtk.main()
	
