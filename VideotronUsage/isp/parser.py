import httplib, urllib, urllib2, datetime, calendar, logging
import re

class AccountUsage():
	def __init__(self, account):
		self.account = account
		self.last_update = False
		self.url = 'https://www.videotron.com/services/secur/ConsommationInternet.do?compteInternet='
		self.uploadSize = 0
		self.downloadSize = 0

	def update(self):
		logging.debug("Updating account information")
		print 'Updating account information'
		account = self.account
		page_contents = self.__get_usage_html(account)
		error_p = re.search('vlxxxxxx',page_contents)
		if ( error_p ):
			return
		p = re.compile(r'.*([0-9]+\.[0-9]+).*')
		values =  p.findall(page_contents, re.MULTILINE)
		self.uploadSize = float(values[4])
		self.downloadSize = float(values[2])

	def __get_usage_html(self, account):
		logging.debug("Logging into Videotron usage as " + account )
		handler = urllib2.HTTPSHandler()
		request = urllib2.Request(self.url + account)
		response = handler.https_open(request)
		return response.read()
