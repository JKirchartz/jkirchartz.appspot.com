#!/usr/bin/env python

# --------- Imports --------
import webapp2, logging
import libs.feedparser as feedparser
import datetime
import libs.PyRSS2Gen as PyRSS2Gen
import re

# ---- The Job Handler --------
class Doit(webapp2.RequestHandler):
    """ make the web thingy """
    def get(self):
        """ cleanup research RSS to be suitable for sharing elsewhere """
        output = ""
        feed = feedparser.parse("http://research.jkirchartz.com/rss")
        entries = feed['items']

        sorted_entries = sorted(entries, key=lambda entry: entry["date_parsed"])
        sorted_entries.reverse() # for most recent entries first

        items = []
        for x in sorted_entries:
            link_rex = re.search(r'href=[\'"]?([^\'" >]+)', x.summary)
            if link_rex:
                items.append(PyRSS2Gen.RSSItem(
                    title=x.title,
                    link=link_rex.group(1),
                    description=x.title,
                    guid=x.link,
                    pubDate=datetime.datetime(
                        x.modified_parsed[0],
                        x.modified_parsed[1],
                        x.modified_parsed[2],
                        x.modified_parsed[3],
                        x.modified_parsed[4],
                        x.modified_parsed[5])
                ))


        # make the RSS2 object
        # Try to grab the title, link, language etc from the orig feed

        rss = PyRSS2Gen.RSS2(
            title="JKirchartz's Research Feed",
            link="http://tools.jkirchartz.com/researchfeed",
            description="JKirchartz's Research Feed",
            lastBuildDate=datetime.datetime.now(),
            items=items
        )


        self.response.headers['Content-Type'] = 'application/rss+xml'
        self.response.out.write(rss.to_xml())
        return

app = webapp2.WSGIApplication([('/researchfeed', Doit)], debug=True)
