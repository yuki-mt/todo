#!/usr/bin/python
#coding=utf-8
import json
import os
import base64
import urllib2


class TogglCredentialProvider(object):
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.conf_path = current_dir + "/.toggl.json"
        self.wid_key = "wid"
        self.token_key = "token"
        self.keys = [self.wid_key, self.token_key]

    """
    @return {
        wid: <TOGGLE_WORKSPACE_ID>,
        token: <TOGGLE_TOKEN>
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

    def get_token(self):
        conf = self.get()
        return conf[self.token_key]

    def filter_conf(self, conf):
        result = {}
        for key in self.keys:
            if key in conf:
                result[key] = conf[key]
        return result

    def ask(self):
        response = False
        while not response:
            email = raw_input('Input email in Toggl: ')
            password = raw_input('Input password in Toggl: ')
            try:
                response = self.authenticate(email, password)
            except urllib2.HTTPError as e:
                if (e.code == 403):
                    print('Invalid credentials. Please try again.')
                    continue
                else:
                    raise e

        token = response['data']['api_token']
        workspaces = response['data']['workspaces']

        if len(workspaces) == 1:
            wid = workspaces[0]['id']
        else:
            work_names = [w['name'] for w in workspaces]
            wid = False
            while not wid:
                name = raw_input("Choose workspace from %s: " % ",".join(work_names))
                for w in workspaces:
                    if w['name'] == name:
                        wid = w['id']
                if (not wid): print('Workspace not found.')

        return {
            self.wid_key: wid,
            self.token_key: token
        }

    def authenticate(self, email, password):
        url = "https://www.toggl.com/api/v8/me"
        request = urllib2.Request(url)
        base64string = base64.b64encode('%s:%s' % (email, password))
        request.add_header("Authorization", "Basic %s" % base64string)

        result = urllib2.urlopen(request)
        response = json.loads(result.read())
        result.close()
        return response

    def save(self, conf):
        with open(self.conf_path, 'w') as f:
            f.write(json.dumps(conf))

    def reset(self):
        os.remove(self.conf_path)
        print "Successfully delete Toggl API data"
