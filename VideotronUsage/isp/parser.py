#!/usr/bin/env python
import httplib, urllib, urllib2, datetime, calendar, logging
import re
import optparse

class AccountUsage():
    def __init__(self, account):
        """
        Constructor

        takes a single parameter, the videotron account that we want to query.
        """
        self.account = account
        self.last_update = False
        self.url = 'https://www.videotron.com/services/secur/en/votre_compte/StartTransaction.jsp'
        self.field = 'compteInternet'
        self.uploadSize = 0
        self.downloadSize = 0
        self.startDate = ''
        self.endDate = ''

    def update(self):
        """
        Updates the global variables with data from the server and parsing the result page.
        """
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
        """
        retrieves the data from the server
        """
        logging.debug("Logging into Videotron usage as [user=" + account +"]" )
        form_values = {
            self.field : self.account
        }
        request = urllib2.Request(self.url)
        request.add_data( urllib.urlencode(form_values))
        opener = urllib2.build_opener( urllib2.HTTPSHandler() )
        urllib2.install_opener( opener )
        fs = urllib2.urlopen( request )
        https_response = fs.read()
        https_headers = fs.info().headers
        https_mimetype = fs.info().type

        return https_response

def main():
    """
    Main method to test
    """
    p = optparse.OptionParser(description="", prog="parser",version="0.1", usage="%prog --account=<account>")
    p.add_option("--account","-a",action="store",help="The isp account identifier")
    p.add_option("--verbose","-v",action="store_true",help="Enables Verbose logging.")
    options,arguments = p.parse_args()
    if options.verbose:
        print "Running parser"

    if not options.account:
        p.print_help()
        return;

    au = AccountUsage(options.account)
    au.update()
    print(au.startDate)
    print(au.endDate)
    print(au.uploadSize)
    print(au.downloadSize)

if __name__ == "__main__":
    main()
