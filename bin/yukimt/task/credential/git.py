#!/usr/bin/python
#coding=utf-8
import json
import os
import base64
import urllib2


class GitCredentialProvider(object):
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.conf_path = current_dir + "/.git.json"
        self.username_key = "username"
        self.git_key = "github"
        self.zen_key = "zenhub"
        self.keys = [self.username_key, self.git_key, self.zen_key]

    """
    @return {
        username: <GITHUB_USERNAME>
        github: <GITHUB_API_TOKEN>
        zenhub: <ZENHUB_API_TOKEN>
    }
    """
    def get(self):
        conf = {}
        # load file data if exists
        if os.path.isfile(self.conf_path):
            with open(self.conf_path, "r") as f:
                conf = json.loads(f.read())
                conf = self.filter_conf(conf)

        # ask a user for data if data is not in the json file
        if len(conf) != len(self.keys):
            conf = self.ask()
            self.save(conf)

        return conf

    def filter_conf(self, conf):
        result = {}
        for key in self.keys:
            if key in conf:
                result[key] = conf[key]
        return result

    def ask(self):
        response = False
        while not response:
            username = raw_input('Input username in Github: ')
            password = raw_input('Input password in Github: ')
            try:
                response = self.authenticate(username, password)
            except urllib2.HTTPError as e:
                if (e.code == 401):
                    print('Invalid credentials. Please try again.')
                    continue
                else:
                    raise e

        ask_str = """\
Get Zenhub API Key in

https://dashboard.zenhub.io/#/settings

(Just hit Enter if you do not use Zenhub)
Paste the key: """
        zen = raw_input(ask_str)
        return {
            self.git_key: response['token'],
            self.zen_key: zen,
            self.username_key: username
        }

    def authenticate(self, username, password):
        url = 'https://api.github.com/authorizations'
        data = '{"scopes":["repo"],"note":"zen-toggl-trello"}'
        base64string = base64.b64encode('%s:%s' % (username, password))
        request = urllib2.Request(url, data, {'Authorization': 'Basic %s' % base64string})

        result = urllib2.urlopen(request)
        response = json.loads(result.read())
        result.close()
        return response

    def save(self, conf):
        with open(self.conf_path, 'w') as f:
            f.write(json.dumps(conf))

    def reset(self):
        os.remove(self.conf_path)
        print "Successfully delete Github API data"
