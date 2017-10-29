#!/usr/bin/python
#coding=utf-8
from todo.trello import TrelloTodo
from todo.importer import Importer
from done.trello import CurrentWork
from done.toggl import TogglDone
from credential.toggl import TogglCredentialProvider

t = TogglDone()
t.generate(2)
#t = TogglCredentialProvider()
#print t.get()

#i = Importer()
#i.sync()
#todo = TrelloTodo()
#todo.generate()

#c = CurrentWork()
#c.get_id()
