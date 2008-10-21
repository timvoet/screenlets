#!/usr/bin/env python

# This application is released under the GNU General Public License 
# v3 (or, at your option, any later version). You can find the full 
# text of the license under http://www.gnu.org/licenses/gpl.txt. 
# By using, editing and/or distributing this software you agree to 
# the terms and conditions of this license. 
# Thank you for using free software!

#  TestScreenlet (c) RYX 2007 <ryx@ryxperience.com>
#
# INFO:
# - a testing-screenlet for experimental usage
# 
# TODO:
# - 

import screenlets
from screenlets.options import StringOption, AccountOption
from urllib import urlopen, urlencode
import cairo
import pango
import gtk
import gobject

class HudsonStatusScreenlet (screenlets.Screenlet):
	"""A testing Screenlet"""
	
	# default meta-info for Screenlets
	__name__	= 'HudsonStatusScreenlet'
	__version__	= '0.1'
	__author__	= 'Tim Voet'
	__desc__	= 'A screenlet to monitor hudson job statuses.'

	# internals
	__timeout = None

	# settings
	update_interval = 1
		
	# editable options
	hudson_url = ''
	job_name = 'Test Job'
	job_number = ''
	job_status = ''
	
	# constructor
	def __init__ (self, **keyword_args):
		#call super (width/height MUST match the size of graphics in the theme)
		screenlets.Screenlet.__init__(self, width=200, height=200, 
			uses_theme=True, **keyword_args)
		# set theme
		self.theme_name = "default"

		# add option group
		self.add_options_group('Hudson', 'This is settings for the hudson job to monitor')
		# add editable option
		self.add_option(StringOption('Hudson', # group name
			'hudson_url', 						# attribute-name
			self.hudson_url,						# default-value
			'Hudson URL', 						# widget-label
			'This is the URL for your hudson Server....'	# description
			)) 
		# test of new account-option
		self.add_option(StringOption('Hudson', 'job_name', 
			self.job_name, 'Job Name', 
			'Enter the job name you want to monitor here ...'))

		# init the timeout function
		self.update_interval = self.update_interval

	def on_init (self):
		print "HudsonStatusScreenlet has been initialized."
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
			# set size
			ctx.scale(self.scale, self.scale)
			# draw bg (if theme available)
			ctx.set_operator(cairo.OPERATOR_OVER)
			# render svg-file
			self.theme['background.svg'].render_cairo(ctx)
			# render png-file
			#ctx.set_source_surface(self.theme['example-test.png'], 0, 0)
			#ctx.paint()
			ctx.set_source_rgba(1, 1, 1, 0.9)
			text = '<small><small><small><small>' + self.job_name +'</small></small></small></small>\n'
			self.theme.draw_text(ctx,text, 15, 20, 'Free Sans', 25,  self.width,pango.ALIGN_LEFT)
			text2 = '\n<small><small><small><small>' + self.job_number + '   ' + self.job_status +'</small></small></small></small>\n'
			self.theme.draw_text(ctx,text2, 15, 20, 'Free Sans', 25,  self.width,pango.ALIGN_LEFT)
			# add the last layer
			self.theme['background-glass.svg'].render_cairo(ctx)
	
	def on_draw_shape (self, ctx):
		self.on_draw(ctx)
	
	def update(self):
		gobject.idle_add(self.get_hudson_status)
		self.redraw_canvas()
		return True

	def get_hudson_status(self):
		if ( self.hudson_url == '' ):
			return True
		elif ( self.job_name == '' ):
			return True

		url = ''
		if ( self.hudson_url.startswith('http')):
			url = self.hudson_url
		else:
			url = 'http://' + self.hudson_url
		print 'URL:' + url + '/job/' + self.job_name + '/rssAll' 
		data = urlopen( url + '/job/' + self.job_name.replace(' ', '%20') + '/rssAll' ).read()
		dcstart = data.find('<entry>')
		dcstart = data.find('<title>',dcstart)
		print dcstart
		dcend = data.find('</title>', dcstart)
		print dcend
		content = data[dcstart+7:dcend]
		print content
		numStart = content.find('#' );
		numEnd = content.find(' ', numStart)
		self.job_number = content[numStart:numEnd]
		print self.job_number
		statusStart = content.find('(', numStart)
		statusEnd = content.find(')', statusStart)
		self.job_status = content[statusStart:statusEnd+1]
		print self.job_status
	
# If the program is run directly or passed as an argument to the python
# interpreter then create a Screenlet instance and show it
if __name__ == "__main__":
	import screenlets.session
	screenlets.session.create_session(HudsonStatusScreenlet)

