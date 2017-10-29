#!/usr/bin/python
#coding=utf-8
import json
import os
import urllib2
from credential.trello import TrelloCredentialProvider


class CurrentWork(object):
    def __init__(self):
        provider = TrelloCredentialProvider()
        self.cred = provider.get()

    def get_id(self):
        list_id = self.ask()
        print "Your List ID is (for webhook): " + list_id


    def ask(self):
        board = self.get_board()
        t_list = self.get_list(board['id'])
        return t_list['id']

    def get_board(self):
        url = "https://trello.com/1/members/%s/boards?key=%s&token=%s&fields=name" % (
            self.cred['username'], self.cred['key'], self.cred['token']
        )
        return self.get_data("Board", url)

    def get_list(self, board_id):
        url = "https://trello.com/1/boards/%s/lists?key=%s&token=%s&fields=name" % (
            board_id, self.cred['key'], self.cred['token']
        )
        return self.get_data("List", url)

    def get_data(self, key, url):
        ask_str = "target Trello %s name for current work: " % key
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
