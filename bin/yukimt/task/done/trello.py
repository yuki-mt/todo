#!/usr/bin/python
#coding=utf-8
import json
import os
import urllib2
from yukimt.task.credential.trello import TrelloCredentialProvider
from yukimt.task.trello import TrelloManager


class Webhook(object):
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.conf_path = current_dir + "/.trello.json"
        self.list_key = "list"
        self.board_key = "board"
        self.keys = [self.list_key, self.board_key]
        provider = TrelloCredentialProvider()
        self.cred = provider.get()
        self.manager = TrelloManager()

    def register(self):
        conf = self.get_conf()
        callback_url = raw_input("callback url: ")
        url = "https://api.trello.com/1/tokens/%s/webhooks/?key=%s" % (
            self.cred['token'], self.cred['key']
        )
        data = {
            'description': 'webhook for Toggl',
            'callbackURL': callback_url,
            'idModel': conf[self.board_key]['id']
        }
        data = json.dumps(data)
        request = urllib2.Request(url, data, {'Content-Type': 'application/json'})
        result = urllib2.urlopen(request)
        response = json.loads(result.read())
        result.close()
        print "Complete!"

    def get_conf(self):
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

    def ask(self):
        print "Input Board and List Name in Trello for current work"
        board = self.manager.get_board()
        t_list = self.manager.get_list(board['id'])
        return {self.list_key: t_list, self.board_key: board}

    def filter_conf(self, conf):
        result = {}
        for key in self.keys:
            if key in conf:
                result[key] = conf[key]
        return result

    def get_list_id(self):
        conf = self.get_conf()
        return conf[self.list_key]['id']

    def save(self, conf):
        with open(self.conf_path, 'w') as f:
            f.write(json.dumps(conf))

    def reset(self):
        os.remove(self.conf_path)
        print "Successfully delete Trello API data"
