#!/usr/bin/env python

# --------- Imports --------
import webapp2, logging
from libs.untinyurl import untiny
# untinyurl.py; https://github.com/JulienPalard/untinyurl

# ---- The Job Handler --------
class doit(webapp2.RequestHandler):
    def get(self):
        url = self.request.get("url")
        #url = urllib.unquote_plus(url)
        logging.info(url)
        output = untiny(url)
        logging.info(output)
        self.response.out.write(output)
        return

app = webapp2.WSGIApplication([('/untiny',doit)], debug=True)
