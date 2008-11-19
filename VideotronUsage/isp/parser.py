import httplib, urllib, urllib2, datetime, calendar, logging
import re

class AccountUsage():
	def __init__(self, account):
		self.account = account
		self.last_update = False
		self.url = 'https://www.videotron.com/services/secur/ConsommationInternet.do?compteInternet='
		self.uploadSize = 0
		self.downloadSize = 0
		self.startDate = ''
		self.endDate = ''

	def update(self):
		logging.debug("Updating account information")
		print 'Updating account information'
		account = self.account
		page_contents = self.__get_usage_html(account)
		error_p = re.search('vlxxxxxx',page_contents)
		if ( error_p ):
			return
		p = re.compile(r'.*>([0-9]+\.[0-9]+).*')
		values =  p.findall(page_contents, re.MULTILINE)
		self.uploadSize = float(values[3])
		self.downloadSize = float(values[1])
		start_date_pattern = re.compile(r'>([0-9][0-9][0-9][0-9]\-[0-9][0-9]\-[0-9][0-9]).* ')
		end_date_pattern = re.compile(r'>([0-9][0-9][0-9][0-9]\-[0-9][0-9]\-[0-9][0-9])<.*')
		start_date_values = start_date_pattern.findall(page_contents,re.MULTILINE)
		end_date_values = end_date_pattern.findall(page_contents,re.MULTILINE)
		self.startDate = start_date_values[0]
		self.endDate = end_date_values[0]

	def __get_usage_html(self, account):
		logging.debug("Logging into Videotron usage as " + account )
		handler = urllib2.HTTPSHandler()
		request = urllib2.Request(self.url + account)
		response = handler.https_open(request)
		return response.read()
