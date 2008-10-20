#!/usr/bin/env python

# This application is released under the GNU General Public License 
# v3 (or, at your option, any later version). You can find the full 
# text of the license under http://www.gnu.org/licenses/gpl.txt. 
# By using, editing and/or distributing this software you agree to 
# the terms and conditions of this license. 
# Thank you for using free software!

#  TemplateScreenlet (c) Whise 2007 

import screenlets
from screenlets.options import StringOption , BoolOption , IntOption , FileOption , DirectoryOption , ListOption , AccountOption , TimeOption , FontOption, ColorOption , ImageOption
from screenlets import DefaultMenuItem
import pango
import gobject


class HudsonStatusScreenlet (screenlets.Screenlet):
	"""
	A simple example of how to create a Screenlet
	"""
	
	# default meta-info for Screenlets (should be removed and put into metainfo)
	__name__	= 'HudsonStatusScreenlet'
	__version__	= '0.1'
	__author__	= 'Tim Voet'
	__desc__	= __doc__	# set description to docstring of class
	
	# editable options (options that are editable through the UI)
	test_text = 'Hi.. im a screenlet'
	demo_text = ''
	demo_number = ''
	int_example = 1
	bool_example = True
	time_example =  (7, 30, 0)
	account_example =  ('','')
	color_example =(0.0, 0.0, 0.0, 1)
	font_example = "Sans Medium 5"
	image_example = ''
	file_example = ''
	directory_example = ''
	list_example = ('','')
	hover = False
	number = 0
	# constructor
	def __init__ (self, **keyword_args):
		#call super (width/height MUST match the size of graphics in the theme)
		screenlets.Screenlet.__init__(self, width=200, height=200, 
			uses_theme=True, **keyword_args)
		# set theme
		self.theme_name = "default"
		# add option group
		self.add_options_group('Example', 'This is an example of ' +\
			' editable options within an OptionGroup ...')
		# add editable option to the group
		self.add_option(StringOption('Example','test_text',			# attribute-name
			self.test_text,						# default-value
			'Test-Text', 						# widget-label
			'The Test-Text option for this Screenlet ...'	# description
			))

		self.add_option(BoolOption('Example','bool_example', 
			self.bool_example, 'Option group bool', 
			'Example options group using bool'))

		self.add_option(TimeOption('Example','time_example', self.time_example, 
 			'Option group time', 'Example options group using time'))

		self.add_option(IntOption('Example','int_example', 
			self.int_example, 'Option group integer', 
			'Example options group using integer', 
			min=0, max=5000))

		self.add_option(FontOption('Example','font_example', 
			self.font_example, 'Option group font', 
			'Example options group using font'))

		self.add_option(ColorOption('Example','color_example', 
			self.color_example, 'Option group color', 
			'Example options group using color'))

		self.add_option(AccountOption('Example','account_example',self.account_example,
			'Option group account','Using keyring encryption'))
		self.add_option(ImageOption('Example','image_example', self.image_example, 
			'Option group Image', 'Example options group using Image')) 

		self.add_option(FileOption('Example','file_example', self.file_example, 
			'Option group file', 'Example options group using file')) 

		self.add_option(DirectoryOption('Example','directory_example', self.directory_example, 
			'Option group directory', 'Example options group using directory')) 

		self.add_option(ListOption('Example','list_example', self.list_example, 
			'Option group list', 'Example options group using list')) 

		# ADD a 1 second (1000) TIMER
		self.timer = gobject.timeout_add( 1000, self.update)



	def update (self):
		
		self.redraw_canvas()
		return True # keep running this event	
	
	# ONLY FOR TESTING!!!!!!!!!
	def init_options_from_metadata (self):
		"""Try to load metadata-file with options. The file has to be named
		like the Screenlet, with the extension ".xml" and needs to be placed
		in the Screenlet's personal directory. 
		NOTE: This function always uses the metadata-file relative to the 
			  Screenlet's location, not the ones in SCREENLETS_PATH!!!"""
		print __file__
		p = __file__.rfind('/')
		mypath = __file__[:p]
		print mypath
		self.add_options_from_file( mypath + '/' + \
			self.__class__.__name__ + '.xml')	


	def on_after_set_atribute(self,name, value):
		"""Called after setting screenlet atributes"""
		
		pass

	def on_before_set_atribute(self,name, value):
		"""Called before setting screenlet atributes"""
		
		pass


	def on_create_drag_icon (self):
		"""Called when the screenlet's drag-icon is created. You can supply
		your own icon and mask by returning them as a 2-tuple."""
		return (None, None)

	def on_composite_changed(self):
		"""Called when composite state has changed"""
		pass

	def on_drag_begin (self, drag_context):
		"""Called when the Screenlet gets dragged."""
		pass
	
	def on_drag_enter (self, drag_context, x, y, timestamp):
		"""Called when something gets dragged into the Screenlets area."""
		pass
	
	def on_drag_leave (self, drag_context, timestamp):
		"""Called when something gets dragged out of the Screenlets area."""
		pass

	def on_drop (self, x, y, sel_data, timestamp):
		"""Called when a selection is dropped on this Screenlet."""
		return False
		
	def on_focus (self, event):
		"""Called when the Screenlet's window receives focus."""
		pass
	
	def on_hide (self):
		"""Called when the Screenlet gets hidden."""
		pass
	
	def on_init (self):
		"""Called when the Screenlet's options have been applied and the 
		screenlet finished its initialization. If you want to have your
		Screenlet do things on startup you should use this handler."""
		
		# add default menu items
		self.add_default_menuitems()


	def on_key_down(self, keycode, keyvalue, event):
		"""Called when a keypress-event occured in Screenlet's window."""
		key = gtk.gdk.keyval_name(event.keyval)
		
		pass
	
	def on_load_theme (self):
		"""Called when the theme is reloaded (after loading, before redraw)."""
		pass
	
	def on_menuitem_select (self, id):
		"""Called when a menuitem is selected."""
		
		pass
	
	def on_mouse_down (self, event):
		"""Called when a buttonpress-event occured in Screenlet's window. 
		Returning True causes the event to be not further propagated."""
	    
		return False
	
	def on_mouse_enter (self, event):
		"""Called when the mouse enters the Screenlet's window."""
		print 'mouse is over me'
		
	def on_mouse_leave (self, event):
		"""Called when the mouse leaves the Screenlet's window."""
		print 'mouse leave'

	def on_mouse_move(self, event):
		"""Called when the mouse moves in the Screenlet's window."""

		pass

	def on_mouse_up (self, event):
		"""Called when a buttonrelease-event occured in Screenlet's window. 
		Returning True causes the event to be not further propagated."""
		return False
	
	def on_quit (self):
		"""Callback for handling destroy-event. Perform your cleanup here!"""
		screenlets.show_question(self, 'Do you like screenlets?')
		return True
		
	def on_realize (self):
		""""Callback for handling the realize-event."""
	
	def on_scale (self):
		"""Called when Screenlet.scale is changed."""
		pass
	
	def on_scroll_up (self):
		"""Called when mousewheel is scrolled up (button4)."""
		pass

	def on_scroll_down (self):
		"""Called when mousewheel is scrolled down (button5)."""
		pass
	
	def on_show (self):
		"""Called when the Screenlet gets shown after being hidden."""
		pass
	
	def on_switch_widget_state (self, state):
		"""Called when the Screenlet enters/leaves "Widget"-state."""
		pass
	
	def on_unfocus (self, event):
		"""Called when the Screenlet's window loses focus."""
		pass
	
	def on_draw (self, ctx):
		"""In here we draw"""
				
	def on_draw_shape (self, ctx):
		self.on_draw(ctx)
	
# If the program is run directly or passed as an argument to the python
# interpreter then create a Screenlet instance and show it
if __name__ == "__main__":
	# create new session
	import screenlets.session
	screenlets.session.create_session(HudsonStatusScreenlet)

