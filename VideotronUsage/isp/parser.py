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
		account = self.account
		page_contents = self.__get_usage_html(account)
		p = re.compile(r'.*([0-9]+\.[0-9]+).*')
		values =  p.findall(page_contents, re.MULTILINE)
		self.uploadSize = float(values[2])
		self.downloadSize = float(values[4])

	def __get_usage_html(self, account):
		logging.debug("Logging into Videotron usage as " + account )
		handler = urllib2.HTTPSHandler()
		request = urllib2.Request(self.url + account)
		response = handler.https_open(request)
		return response.read()
