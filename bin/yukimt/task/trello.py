#!/usr/bin/python
#coding=utf-8
import json
import os
import urllib2
from yukimt.task.credential.trello import TrelloCredentialProvider
import sys


class TrelloManager(object):
    def __init__(self):
        provider = TrelloCredentialProvider()
        self.cred = provider.get()

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
        try:
            response = json.loads(result.read())
        except urllib2.URLError, e:
            print "Error: Failed to authorize in Trello"
            sys.exit(1)

        result.close()
        for b in response:
            if b['name'] == new_name:
                return b
        print "Error: The target name is not found in Your Account"
        sys.exit(1)
