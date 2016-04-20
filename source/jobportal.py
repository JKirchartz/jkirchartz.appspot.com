#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyleft (ↄ) 2016 kirch <kirch@arp>
#
# Distributed under terms of the NPL (Necessary Public License) license.

import webapp2, logging, json
from indeed import IndeedClient

class Indeed(webapp2.RequestHandler):
    def jobs(self, client, query, location):
        params = {
            'q': query, # query
            'l': location, #location
            'userip': self.request.remote_addr, # required
            'useragent': self.request.headers.get('User-Agent'), # required
            'latlong': 1 # get latlong for each position matched
        }
        return client.search(**params)

    def details(self, client, jobs):
        return client.jobs(jobkeys = jobs)


    def get(self):
        client = IndeedClient('4970113146490412') # not secure, but whatevs
        query = self.request.get_all("q")
        location = self.request.get_all("l")
        jobids = self.request.get_all("jobids")
        output = ""

        if query:
            output = self.jobs(client, query, location)

        if jobids:
            output = self.details(client, tuple(jobids.split(',')))

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(output))

app = webapp2.WSGIApplication([('/jobportal.json', Indeed)], debug=True)
