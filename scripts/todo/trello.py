#!/usr/bin/python
#coding=utf-8
import json
import os
import urllib2
from credential.trello import TrelloCredentialProvider


class TrelloTodo(object):
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.conf_path = current_dir + "/.trello.json"
        self.format_path = current_dir + "/format.txt"
        self.list_key = "list"
        self.keys = [self.list_key]

        provider = TrelloCredentialProvider()
        self.cred = provider.get()

    def generate(self):
        conf = self.get_conf()
        cards = self.get_cards(conf[self.list_key]['id'])
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
        board = self.get_board()
        t_list = self.get_list(board['id'])
        return {self.list_key: t_list}
            
    def get_board(self):
        url = "https://trello.com/1/members/%s/boards?key=%s&token=%s&fields=name" % (
            self.cred['username'], self.cred['key'], self.cred['token']
        )
        return self.get_data("Board", url)

    def get_list(self, board_id):
        url = "https://trello.com/1/boards/%s/lists?key=%s&token=%s&fields=name" % (
            board_id, self.cred['key'], self.cred['token']
        )
        return self.get_data(self.list_key, url)

    def get_cards(self, list_id):
        url = "https://trello.com/1/lists/%s/cards?key=%s&token=%s&fields=name" % (
            list_id, self.cred['key'], self.cred['token']
        )
        result = urllib2.urlopen(url)
        response = json.loads(result.read())
        result.close()
        return response

    def get_data(self, key, url):
        ask_str = "target Trello %s name: " % key
        new_name = raw_input(ask_str)
        new_name = new_name.decode('utf-8')

        result = urllib2.urlopen(url)
        response = json.loads(result.read())
        result.close()
        #TODO: throw if not authorized
        for b in response:
            if b['name'] == new_name:
                return b
        #TODO: throw exception

    def save(self, conf):
        with open(self.conf_path, 'w') as f:
            f.write(json.dumps(conf))

    def reset(self):
        os.remove(self.conf_path)
        print "Successfully delete Trello Target Board & List"
