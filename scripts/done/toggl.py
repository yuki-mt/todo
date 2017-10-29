#!/usr/bin/python
#coding=utf-8
import json
import os
import urllib2
from credential.toggl import TogglCredentialProvider
import datetime
import math
import base64
from itertools import groupby
from operator import itemgetter


class TogglDone(object):
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.format_path = current_dir + "/format.txt"

        provider = TogglCredentialProvider()
        self.cred = provider.get()

    def generate(self, nDaysAgo = 0):
        tasks = self.get_tasks(nDaysAgo)
        self.output(tasks)

    # output result with format
    def output(self, tasks):
        loop_key = '<@loop>'
        loop_started = False
        loop_format = ""
        result = ""
        with open(self.format_path, "r") as f:
            line = f.readline()
            while line:
                if line == loop_key or line == loop_key + "\n":
                    if loop_started:
                        loop_started = False
                        for t in tasks:
                            result += loop_format % (t['hours'], t['title'])
                    else:
                        loop_started = True
                else:
                    if loop_started:
                        loop_format += line
                    else:
                        result += line
                line = f.readline()
        print result

    def get_tasks(self, nDaysAgo):
        date = datetime.date.today() - datetime.timedelta(days=nDaysAgo)
        end_date = (date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        start_date = date.strftime("%Y-%m-%d")

        url = "https://www.toggl.com/api/v8/time_entries?start_date=" + start_date + "T00%3A00%3A00%2B09%3A00&end_date=" + end_date + "T00%3A00%3A00%2B09%3A00"
        request = urllib2.Request(url)
        base64string = base64.b64encode('%s:api_token' % self.cred['token'])
        request.add_header("Authorization", "Basic %s" % base64string)
        result = urllib2.urlopen(request)
        response = json.loads(result.read())
        result.close()

        res = sorted(response, key=lambda x:x['description'])
        tasks = []
        for desc, items in groupby(res, key=itemgetter('description')):
            secs = sum(i['duration'] for i in items)
            task = {'hours': self.get_hours(secs), 'title': desc}
            tasks.append(task)

        return tasks

    def get_hours(self, secs):
        hours = secs / 3600.0
        return math.ceil(hours * 10) / 10
