#!/usr/bin/python
#coding=utf-8
import json
import os
import urllib2
from yukimt.task.credential.trello import TrelloCredentialProvider
from yukimt.task.trello import TrelloManager


class TrelloTodo(object):
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.conf_path = current_dir + "/.trello.json"
        self.format_path = current_dir + "/format.txt"
        self.list_key = "list"
        self.keys = [self.list_key]
        provider = TrelloCredentialProvider()
        self.cred = provider.get()
        self.manager = TrelloManager()

    def generate(self):
        conf = self.get_conf()
        cards = self.manager.get_cards(conf[self.list_key]['id'])
        names = [c['name'].encode('utf-8') for c in cards]

        self.output(names)

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

    def filter_conf(self, conf):
        result = {}
        for key in self.keys:
            if key in conf:
                result[key] = conf[key]
        return result

    # output result with format
    def output(self, names):
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
                        for n in names:
                            result += loop_format % n
                    else:
                        loop_started = True
                else:
                    if loop_started:
                        loop_format += line
                    else:
                        result += line
                line = f.readline()
        print result

    def ask(self):
        print "Input Board and List name in Trello. (The list is source of todo list)"
        board = self.manager.get_board()
        t_list = self.manager.get_list(board['id'])
        return {self.list_key: t_list}
            
    def save(self, conf):
        with open(self.conf_path, 'w') as f:
            f.write(json.dumps(conf))

    def reset(self):
        os.remove(self.conf_path)
        print "Successfully delete Trello Target Board & List"
