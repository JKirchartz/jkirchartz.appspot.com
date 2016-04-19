#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyleft (ↄ) 2016 kirch <kirch@arp>
#
# Distributed under terms of the NPL (Necessary Public License) license.

import webapp2, logging
from indeed import IndeedClient

class Portal(webapp2.RequestHandler):
    def jobs(self, client, query):
        params = {
            'q': query, # query
            'l': 'Pittsburgh, Pa', #location
            'userip': self.request.remote_addr, # required
            'useragent': self.request.headers.get('User-Agent'), # required
            'latlong': 1 # get latlong for each position matched
        }
        return client.search(**params)

    def details(self, client, jobs):
        return client.jobs(jobkeys = jobs)


    def get(self):
        client = IndeedClient('4970113146490412') # not secure, but whatevs
        posts = self.jobs(client, 'query')
        # do stuff with jobs posts

        # get details for jobs
        # jobs=[] # list for storing job keys
        # jobs.append('') # add job key
        # details = self.details(client, tuple(jobs))

        # output to browser
        self.response.out.write(posts)


app = webapp2.WSGIApplication([('/jobportal', Portal)], debug=True)
