#!/usr/bin/python
#coding=utf-8
import json
import os


class TrelloCredentialProvider(object):
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.conf_path = current_dir + "/.trello.json"
        self.username_key = "username"
        self.key_key = "key"
        self.token_key = "token"
        self.keys = [self.username_key, self.key_key, self.token_key]

    """
    @return {
        username: <YOUR_USERNAME>,
        key: <TRELLO_API_KEY>,
        token: <TRELLO_API_TOKEN>
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
        username = raw_input('Input username in Trello: ')

        ask_key_str = """\
Get Trello API Key in

https://trello.com/1/appKey/generate

Paste the key: """
        key = raw_input(ask_key_str)

        ask_token_str = """\
Get Trello API Token in

https://trello.com/1/authorize?key=%s&name=&expiration=never\
&response_type=token&scope=read,write

Paste the token: """ % key
        token = raw_input(ask_token_str)
        return {
            self.username_key: username,
            self.key_key: key,
            self.token_key: token
        }

    def save(self, conf):
        with open(self.conf_path, 'w') as f:
            f.write(json.dumps(conf))

    def reset(self):
        os.remove(self.conf_path)
        print "Successfully delete Trello API data"
