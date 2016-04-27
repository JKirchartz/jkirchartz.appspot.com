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
    """Get Jobs to place on map
    """
    def jobs(self, client, query, location):
        """Query Indeed.com for jobs
        """
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

    def get(self):
        """Interact with `get` request from front-end
        Currently only does Indeed, other APIs to take into consideration:
            USAjobs.gov, key:  EwesKi7XhFETegcAroJCod5jeP9wwBkzanA1qatBMRY=
            AuthenticJobs.com, key: de1d14f970eaf280a271b1d5beffafe9
        """
        indeed_key = '4970113146490412' # not secure, coz repo, but whatevs
        client = IndeedClient(indeed_key)
        query = self.request.get_all("q")
        location = self.request.get_all("l")
        jobids = self.request.get_all("jobids")
        all = self.request.get_all("all")
        output = ""

        if query and not jobids:
            output = self.jobs(client, query, location)
        elif jobids and not query:
            output = client.jobs(tuple(jobids.split(',')))
        elif all != '':
            jobs = self.jobs(client, query, location)
            output = client.jobs(tuple([job.jobkey for job in jobs.results]))

            # for job in jobs get jobkey & use that to get all data then
            # colloide data on job key


        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(output))

app = webapp2.WSGIApplication([('/jobportal.json', JobPortal)], debug=True)
