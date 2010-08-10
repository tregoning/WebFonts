# About

	* The latest web font format (WOFF) requires special HTTP headers when served from a different domain
	(e.g. Tumblr web templates). Unfortunately most cheap/free host providers including Amazon S3 doen't 
	allow you to set this particular header.
	
	* App Engine when combined with it's Memcache service create an incredibly fast, reliable and scalable
	 way of delivering web fonts for free. (Around 8 and a half million font deliveries per day)

# Setting up WebFonts

## Prerequisites

	* Python 2.5
	* App Engine Python SDK
	* Google's App Engine account with an application ID
	
## Setup

	* git clone git://github.com/tregoning/WebFonts.git
	* cd WebFont
	* Update the "application" entry in the app.yaml file with the name of your application ID
	* Add all the fonts that you would like to serve into the folder named "Fonts" (no subfolders)
		
## Deploy

	* To deploy the application simply follow this instructions:
	http://code.google.com/appengine/docs/python/gettingstarted/uploading.html

## How to run

	* Once you application has been deployed, you can request an specific font as follows:
	 http://{your application id}.appspot.com/fonts/{the font name that you want}

# Further work

	* Investigate options to serve content gzipped
