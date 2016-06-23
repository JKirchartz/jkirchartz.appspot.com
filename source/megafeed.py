#!/usr/bin/env python

# --------- Imports --------
import webapp2, logging
import libs.feedparser as feedparser
import datetime
import libs.PyRSS2Gen as PyRSS2Gen

# ---- The Job Handler --------
class doit(webapp2.RequestHandler):
    def get(self):
        output=""
        feeds = ['http://jkirchartz.com/rss.xml',
                 'http://glitches.jkirchartz.com/rss',
                 'http://tools.jkirchartz.com/researchfeed',
                 'http://stash.jkirchartz.com/rss',
                 'https://github.com/JKirchartz.atom',
                 'http://stackoverflow.com/feeds/user/276250'
                ]
        entries = []
        for feed in feeds:
            d = feedparser.parse(feed)
            entries.extend(d["items"])

        sorted_entries = sorted(entries, key=lambda entry: entry["date_parsed"])
        sorted_entries.reverse() # for most recent entries first

        items = [
                PyRSS2Gen.RSSItem(
                    title = x.title,
                    link = x.link,
                    description = x.description,
                    guid = x.link,
                    pubDate = datetime.datetime(
                        x.modified_parsed[0],
                        x.modified_parsed[1],
                        x.modified_parsed[2],
                        x.modified_parsed[3],
                        x.modified_parsed[4],
                        x.modified_parsed[5])
                    )

                for x in sorted_entries
            ]

        # make the RSS2 object
        # Try to grab the title, link, language etc from the orig feed

        rss = PyRSS2Gen.RSS2(
                title="JKirchartz's MegaFeed",
                link="http://tools.jkirchartz.com/megafeed",
                description="JKirchartz's feeds from everywhere",
                lastBuildDate= datetime.datetime.now(),
                items = items
            )


        self.response.headers['Content-Type'] = 'application/rss+xml'
        self.response.out.write(rss.to_xml(encoding = 'utf-8'))
        return

app = webapp2.WSGIApplication([('/megafeed',doit)], debug=True)
