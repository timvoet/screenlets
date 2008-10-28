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
	stats = {
		'upload' : 10,
		'download' : 20}
	
	# constructor
	def __init__ (self, **keyword_args):
		#call super (width/height MUST match the size of graphics in the theme)
		screenlets.Screenlet.__init__(self, width=250, height=100, 
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
		self.get_isp_info()
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
			uploadValue = self.stats['upload']
			downloadValue = self.stats['download']
			self.theme['background.svg'].render_cairo(ctx)
			ctx.set_source_rgba(1,1,1,0.8)
			self.theme.draw_text(ctx, 'Up',6,4, 'Free Sans', 10,  self.width,pango.ALIGN_LEFT)
			size = (uploadValue/10)*200
			self.theme.draw_text(ctx, str(uploadValue),80,4,'Free Sans', 10, self.width, pango.ALIGN_LEFT)
			ctx.translate(0,20)
			self.theme['background.svg'].render_cairo(ctx)
			self.theme.draw_text(ctx, 'Down',6,4, 'Free Sans', 10,  self.width,pango.ALIGN_LEFT)
			self.theme.draw_text(ctx, str(downloadValue),80,4, 'Free Sans', 10,  self.width,pango.ALIGN_LEFT)
			# render png-file
			ctx.save()

	
	def on_draw_shape (self, ctx):
		self.on_draw(ctx)
	
	def update(self):
		gobject.idle_add(self.get_isp_info)
		self.redraw_canvas()
		return True

	def get_isp_info(self):
                self.stats['upload'] = 5
		self.stats['download'] = 10
		pass
	
# If the program is run directly or passed as an argument to the python
# interpreter then create a Screenlet instance and show it
if __name__ == "__main__":
	import screenlets.session
	screenlets.session.create_session(VideotronUsageScreenlet)

