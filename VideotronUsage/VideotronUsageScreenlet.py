#!/usr/bin/env python

# This application is released under the GNU General Public License 
# v3 (or, at your option, any later version). You can find the full 
# text of the license under http://www.gnu.org/licenses/gpl.txt. 
# By using, editing and/or distributing this software you agree to 
# the terms and conditions of this license. 
# Thank you for using free software!

#  VideotronUsageScreenlet (c) Tim Voet 2008 <tim.voet@gmail.com>
#
# INFO:
# - A screenlet that lets you monitor a hudson CI job.
# 
# TODO:
# - Add icons for statuses.  And see if there is a way to get Hudson warnings.

import screenlets
from screenlets.options import StringOption, AccountOption
from urllib import urlopen, urlencode
import cairo
import pango
import gtk
import gobject

class VideotronUsageScreenlet (screenlets.Screenlet):
	"""Videotron Usage Screenlet"""
	
	# default meta-info for Screenlets
	__name__	= 'VideotronUsageScreenlet'
	__version__	= '0.1'
	__author__	= 'Tim Voet'
	__desc__	= 'A screenlet to monitor your bandwidth usage for videotron users.'

	# internals
	__timeout = None

	# settings
	update_interval = 3600
		
	# editable options
	url = ''
	account = ''
	
	# constructor
	def __init__ (self, **keyword_args):
		#call super (width/height MUST match the size of graphics in the theme)
		screenlets.Screenlet.__init__(self, width=200, height=100, 
			uses_theme=True, **keyword_args)
		# set theme
		self.theme_name = "thingrey"

		# add option group
		self.add_options_group('ISP', 'This is settings for ISP information ')
		# add editable option
		self.add_option(StringOption('ISP', # group name
			'account', 						# attribute-name
			self.account,						# default-value
			'Account information', 						# widget-label
			'This is your account string (usually begins with vlxxxxx)....'	# description
			)) 

		# init the timeout function
		self.update_interval = self.update_interval

	def on_init (self):
		print "VideotronUsageScreenlet has been initialized."
		# add default menuitems
		self.add_default_menuitems()

	# attribute-"setter", handles setting of attributes
	def __setattr__(self, name, value):
		# call Screenlet.__setattr__ in baseclass (ESSENTIAL!!!!)
		screenlets.Screenlet.__setattr__(self, name, value)
		# check for this Screenlet's attributes, we are interested in:
		if name == "update_interval":
			if value > 0:
				self.__dict__['update_interval'] = value
				if self.__timeout:
					gobject.source_remove(self.__timeout)
				self.__timeout = gobject.timeout_add(int(value * 1000), self.update)
			else:
				# TODO: raise exception!!!
				self.__dict__['update_interval'] = 1
				pass

	def on_draw (self, ctx):
		# if theme is loaded
		if self.theme:
			# set scale rel. to scale-attribute
			ctx.scale(self.scale, self.scale)
			# draw bg (if theme available)
			ctx.set_operator(cairo.OPERATOR_OVER)
			# render svg-file
			self.theme['background.svg'].render_cairo(ctx)
			# render png-file
			ctx.save()

	
	def on_draw_shape (self, ctx):
		self.on_draw(ctx)
	
	def update(self):
		gobject.idle_add(self.callback)
		self.redraw_canvas()
		return True

	
# If the program is run directly or passed as an argument to the python
# interpreter then create a Screenlet instance and show it
if __name__ == "__main__":
	import screenlets.session
	screenlets.session.create_session(VideotronUsageScreenlet)

