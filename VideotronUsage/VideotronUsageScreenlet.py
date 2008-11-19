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
from screenlets.options import StringOption, IntOption
from urllib import urlopen, urlencode
from isp.parser import AccountUsage
import cairo
import pango
import gtk
import logging
import gobject

class VideotronUsageScreenlet (screenlets.Screenlet):
	"""Videotron Usage Screenlet"""
	
	# default meta-info for Screenlets
	__name__	= 'VideotronUsageScreenlet'
	__version__	= '0.4'
	__author__	= 'Tim Voet'
	__desc__	= 'A screenlet to monitor your bandwidth usage for videotron users.'

	# internals
	__timeout = None

	# settings
	update_interval = 1
		
	# editable options
	url = ''
	account = ''
	upload_limit = 10
	download_limit = 20
	account_usage = None 
	
	# constructor
	def __init__ (self, **keyword_args):
		print "VideotronUsageScreenlet is initializing."
		#call super (width/height MUST match the size of graphics in the theme)
		screenlets.Screenlet.__init__(self, width=300, height=150, 
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
		self.add_option(IntOption('ISP',
			'update_interval',
			self.update_interval,
			'Update interval ( in hours )',
			'The amount of time between checks.  Videotron updates the usage page only once a day',
			min=0, max=23
			))
		self.add_option(IntOption('ISP',
			'upload_limit',
			self.upload_limit,
			'Upload Limit',
			'The amount of GB you are allowed to upload.',
			min=1,
			max=500,
			increment=1
			))
		self.add_option(IntOption('ISP',
			'download_limit',
			self.download_limit,
			'Download limit',
			'The amount of GB you are allowed to download.',
			min=1,
			max=500,
			increment=1
			))


	def on_init (self):
		print "VideotronUsageScreenlet has been initialized."
		# add default menuitems
		self.account_usage = AccountUsage(self.account)
		self.account_usage.update()
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
				self.__timeout = gobject.timeout_add(int(value * 60 * 60 * 1000), self.update)
			else:
				# TODO: raise exception!!!
				self.__dict__['update_interval'] = 1
				pass
		elif name =="account":
			if len(value) > 0:
				self.__dict__['account'] = value
				self.account_usage = AccountUsage(value)
				self.update()
			else:
				pass

	def on_draw (self, ctx):
		# if theme is loaded
		if self.theme:
			# set scale rel. to scale-attribute
			ctx.scale(self.scale, self.scale)
			# draw bg (if theme available)
			ctx.set_operator(cairo.OPERATOR_OVER)
			if self.account_usage ==  None:
				startDate = 'n/a'
				endDate = 'n/a'
				uploadValue = 0
				downloadValue = 0
			else:
				startDate = self.account_usage.startDate
				endDate = self.account_usage.endDate
				uploadValue = self.account_usage.uploadSize
				downloadValue = self.account_usage.downloadSize

			ctx.save()
			#Render the whole BG
			self.theme['widget.svg'].render_cairo(ctx)
			ctx.set_source_rgba(1,1,1,0.8)
			self.theme.draw_text( ctx, 'Usage from:' , 20,10,'Free Sans', 8, self.width,pango.ALIGN_LEFT)
			self.theme.draw_text( ctx, startDate , 100,10,'Free Sans', 8, self.width,pango.ALIGN_LEFT)
			self.theme.draw_text( ctx, 'to:' , 20,25,'Free Sans', 8, self.width,pango.ALIGN_LEFT)
			self.theme.draw_text( ctx, endDate , 100,25,'Free Sans', 8, self.width,pango.ALIGN_LEFT)
			# render the upload bg image
			ctx.save()
			ctx.translate(10,40)
			self.theme['background.svg'].render_cairo(ctx)
			ctx.save()
			ctx.set_source_rgba(1,1,1,0.8)
			self.theme.draw_text(ctx, 'Up',6,4, 'Free Sans', 10,  self.width,pango.ALIGN_LEFT)
			uploadPercent = (uploadValue/self.upload_limit)
			uploadWidth = uploadPercent*165
			self.theme.draw_text(ctx, str(uploadValue),80,4,'Free Sans', 10, self.width, pango.ALIGN_LEFT)
			if ( uploadPercent < 0.7 ):
				ctx.set_source_rgba(0,255,0,0.4)
			elif ( uploadPercent <0.9):
				ctx.set_source_rgba(255,165,0,0.4)
			else:
				ctx.set_source_rgba(255,0,0,0.4)
			self.theme.draw_rounded_rectangle(ctx,78,6,3,uploadWidth,9,True)
			ctx.set_source_rgba(1,1,1,0.8)
			# Render the download bg image
			ctx.translate(0,20)
			self.theme['background.svg'].render_cairo(ctx)
			self.theme.draw_text(ctx, 'Down',6,4, 'Free Sans', 10,  self.width,pango.ALIGN_LEFT)
			self.theme.draw_text(ctx, str(downloadValue),80,4, 'Free Sans', 10,  self.width,pango.ALIGN_LEFT)
			downloadPercent = (downloadValue/self.download_limit)
			downloadWidth = downloadPercent*165
			if ( uploadPercent < 0.7 ):
				ctx.set_source_rgba(0,255,0,0.4)
			elif ( uploadPercent <0.9):
				ctx.set_source_rgba(255,165,0,0.4)
			else:
				ctx.set_source_rgba(255,0,0,0.4)
			self.theme.draw_rounded_rectangle(ctx,78,6,3,downloadWidth,9,True)
			ctx.save()

	
	def on_draw_shape (self, ctx):
		self.on_draw(ctx)
	
	def update(self):
		self.account_usage.update()
		self.redraw_canvas()
		return True

	
# If the program is run directly or passed as an argument to the python
# interpreter then create a Screenlet instance and show it
if __name__ == "__main__":
	import screenlets.session
	screenlets.session.create_session(VideotronUsageScreenlet)

