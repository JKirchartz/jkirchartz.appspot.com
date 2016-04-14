#!/usr/bin/env python

# --------- Imports --------
import webapp2, logging
import libs.feedparser as feedparser
import datetime
import libs.PyRSS2Gen as PyRSS2Gen

# ---- The Job Handler --------
class doit(webapp2.RequestHandler):
    def get(self):
        keywords = ['python', 'php', 'javascript', 'wordpress', 'nodejs']
        output=""
        feeds = [
                 'http://www.pittsource.com/all_jobs.atom',
                 'http://rss.indeed.com/rss?q=(' + ' OR '.join(keywords) + ')&l=Pittsburgh%2C+PA',
                 'http://pghcareerconnector.com/jobs/?display=rss&keywords=' + ' OR '.join(keywords) + '&filter=%2BSTATE_PROVINCE%3Apennsylvania%20%2BSHOW_AT%3A766827&resultsPerPage=1000',
                 'https://pittsburgh.craigslist.org/search/web?format=rss&query=' + ' | '.join(keywords),
                 'https://pittsburgh.craigslist.org/search/eng?format=rss&query=' + ' | '.join(keywords),
                 'https://pittsburgh.craigslist.org/search/sof?format=rss&query=' + ' | '.join(keywords),
                 'https://pittsburgh.craigslist.org/search/cpg?format=rss&query=' + ' | '.join(keywords),
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
                title="JKirchartz's Pittsburgh Jobs Feed",
                link="http://tools.jkirchartz.com/jobfeed",
                description="JKirchartz's job searches everywhere in town",
                lastBuildDate= datetime.datetime.now(),
                items = items
            )


        self.response.headers['Content-Type'] = 'application/rss+xml'
        self.response.out.write(rss.to_xml(encoding = 'utf-8'))
        return

app = webapp2.WSGIApplication([('/jobfeed',doit)], debug=True)
