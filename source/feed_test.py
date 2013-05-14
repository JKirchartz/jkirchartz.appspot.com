#!/usr/bin/env python

# --------- Imports --------
import feedparser

output=""
feeds = [   "http://jkirchartz.com/rss.xml",
            "http://glitches.jkirchartz.com/rss",
            "http://research.jkirchartz.com/rss",
            "http://stash.jkirchartz.com/rss",
            "https://github.com/JKirchartz.atom",
            "http://stackoverflow.com/feeds/user/276250"
            "http://api.twitter.com/1/statuses/user_timeline.rss?screen_name=jkirchartz"
        ]
entries = []
for feed in feeds:
    d = feedparser.parse(feed)
    entries.extend(d["items"])

sorted_entries = sorted(entries, key=lambda entry: entry["date_parsed"])
sorted_entries.reverse() # for most recent entries first

for entry in sorted_entries:
    print entry

print output
