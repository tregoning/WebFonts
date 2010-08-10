import os
from google.appengine.ext.webapp import template

import cgi
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from datetime import datetime
from datetime import timedelta
from datetime import date
from google.appengine.api import memcache	

class MainPage(webapp.RequestHandler):
    def get(self):

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, {}))



class StaticCustomFileHandler(webapp.RequestHandler):
		
    def get(self):
	
        filename = self.request.path.split("/")[-1]
        folder = "fonts"
        fileContent = self.getFile(filename, folder)
	
        if fileContent:
              self.setHeaders(filename)		
              self.response.out.write(fileContent)

        else:
            self.error(404)


    # HTTP Headers are set according to advice from:
    # http://code.google.com/speed/page-speed/docs/caching.html
    def setHeaders(self, filename):

		current_time = datetime.utcnow()
		expires_time = current_time + timedelta(days=365)

		# As the content is static, the Last-Modified header shoudn't change, set to fixed date in the past.
		last_modified = date(1980, 07, 10)
		self.response.headers.add_header("Last-Modified", last_modified.strftime('%a, %d %b %Y %H:%M:%S GMT'))
		
		# Specify either Expires OR Cache-Control headers NOT both
		# Setting Expires header to maximum values allowd by the RFC guidelines
		self.response.headers.add_header("Expires", expires_time.strftime('%a, %d %b %Y %H:%M:%S GMT') )
		self.response.headers['Cache-Control'] = 'public, max-age=315360000'
		
		# Woff files will now work cross domain unless Access-Control-Allow-Origin is set
		# You can set this to * (for request from any domain) or you can set your domain explicitly
		self.response.headers.add_header("Access-Control-Allow-Origin", "*")

		# Some font formats won't work unless Content-Type is set correctly.
		fileExtension = filename.split(".")[-1]
		contentType = {
			'svg': 'image/svg+xml',
			'eot': 'application/vnd.ms-fontobject',
			'ttf': 'application/octet-stream',
			'woff': 'application/x-woff'
		}[fileExtension]

		self.response.headers['Content-Type'] = contentType
		
		
		
    def getFile(self, filename, folder):

	    file_data = memcache.get(filename)
	    if file_data is not None:
	    	return file_data
		
	    else:
	    	pathToFile = folder + "/" + filename

	    	if os.path.exists(pathToFile):
		          file_data = open(pathToFile, "r").read()
		          memcache.add(filename, file_data)
		          return file_data

	    	else:
		          return False


		
application = webapp.WSGIApplication(
                                     [('/', MainPage),
									 (r'/fonts/.*', StaticCustomFileHandler)],
                                     debug=False)



def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()