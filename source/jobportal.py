#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyleft (ↄ) 2016 kirch <kirch@arp>
#
# Distributed under terms of the NPL (Necessary Public License) license.

import webapp2, logging, json
from indeed import IndeedClient

class JobPortal(webapp2.RequestHandler):
    def indeedJobs(self, client, query, location):
        params = {
            'q': query, # query
            'l': location, #location
            'userip': self.request.remote_addr, # required
            'useragent': self.request.headers.get('User-Agent'), # required
            'latlong': 1, # get latlong for each position matched
            'limit': 25,
            'highlight': 1
        }
        return client.search(**params)

    def indeedDetails(self, client, jobs):
        return client.jobs(jobkeys = jobs)

    def get(self):
        client = IndeedClient('4970113146490412') # not secure, coz repo, but whatevs
        query = self.request.get_all("q")
        location = self.request.get_all("l")
        jobids = self.request.get_all("jobids")
        all = self.request.get_all("all")
        output = ""

        if query and not jobids:
            output = self.indeedJobs(client, query, location)
        elif jobids and not query:
            output = self.indeedDetails(client, tuple(jobids.split(',')))
        elif all != '':
            jobs = self.indeedJobs(client, query, location)
            results = jobs.results
            output = self.indeedDetails(client,
                                        tuple([job.jobkey for job in results]))



            # for job in jobs get jobkey & use that to get all data then
            # colloide data on job key


        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(output))

app = webapp2.WSGIApplication([('/jobportal.json', JobPortal)], debug=True)
