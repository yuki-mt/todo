# TODO Manager: Collaborate Github, Zenhub, Trello, and Toggl to manage your tasks.

![Overall Description](https://raw.github.com/wiki/yuki-mt/todo/images/description.png)

## Prerequsite Accounts
- [Github](https://github.com/)
- [Zenhub](https://www.zenhub.com/) (optional)
- [Trello](https://trello.com/)
- [Toggl](https://toggl.com/)
- [Heroku](https://www.heroku.com/) (for Webhook)

## Set up

```
$ git clone https://github.com/yuki-mt/todo.git
$ cd todo
### not only /usr/local/bin. can be anywhere in $PATH
$ sudo mv bin/* /usr/local/bin
```

## Features
### Account Information
#### Brief Description
Input Account Information.
#### How to Use
You need to input your account information only once.  
(replace uppercase parts with your own account information, and setting)  
("##" is comment)  
[Set up](https://github.com/yuki-mt/todo#set-up) before you try the following.

```
$ ym-task setup-cred
Input username in Trello: YOUR_TRELLO_USERNAME
Get Trello API Key in

https://trello.com/1/appKey/generate

Paste the key: TRELLO_DEVELOPER_KEY
Get Trello API Token in

https://trello.com/1/authorize?key=TRELLO_DEVELOPER_KEY&name=&expiration=never&response_type=token&scope=read,write

Paste the token: YOUR_TRELLO_TOKEN
Input email in Toggl: YOUR_TOGGL_EMAIL
Input password in Toggl: YOUR_TOGGLE_PASSWORD
Input username in Github: GITHUB_USERNAME
Input password in Github: GITHUB_PASSWORD
## If you get an error here, try to remove 'zen-toggl-trello' from https://github.com/settings/tokens
Get Zenhub API Key in

https://dashboard.zenhub.io/#/settings

(Just hit Enter if you do not use Zenhub)
Paste the key: ZENHUB_KEY
```

### Import
#### Brief Description
Import Github (or Zenhub) issues assigned to you to Trello
#### How to Use
Replace uppercase parts with your own account information, and setting  
If you skip [Account Information section](https://github.com/yuki-mt/todo#how-to-use), you may be asked more request to give account information.  
("##" is comment)  
[Set up](https://github.com/yuki-mt/todo#set-up) before you try the following.

```
$ ym-task import
import by what?
[g: Github label, z: Zenhub Board Name]: G_OR_Z
label or board name
(use , for multiple choices. e.g. 'In Progress,Backlog')
If you want all issues assigned to you, just hit Enter
## If you select "g" before and type "label1,label2,label3", you will import issues labeled "label1", "label2", or "label3", which are assigned to you.
input here: YOUR_LABEL_OR_BOARD(LIST?)_NAME
## repository from which you will import issues e.g. https://github.com/****/****
Repository URL: YOUR_REPOSITORY_URL
## you will find Repository ID in URL when you click on "Board" tab in Github if you have Zenhub account and plugin.
Repository ID (Enter if you do not use Zenhub): USER_REPOSITORY_ID 
Input Board and List Name in Trello as destination of importing
## the board to which you will import issues
target Trello Board name: YOUR_BOARD_NAME 
## the list to which you will import issues
target Trello List name: YOUR_LIST_NAME
Complete!
```

Now, your YOUR_LIST_NAME list in Trello has Github all issues labeled "label1", "label2", or "label3", which are assigned to you.  
If you already have some issues in Trello list, this command will not create the same issues.

### TODO
#### Brief Description
Output titles of cards in a certain list in Trello
#### How to Use
Replace uppercase parts with your own account settings  
("##" is comment)  
If you skip [Account Information section](https://github.com/yuki-mt/todo#how-to-use), you may be asked more request to give account information.  
[Set up](https://github.com/yuki-mt/todo#set-up) before you try the following.

```
$ ym-task todo
Input Board and List name in Trello. (The list is source of todo list)
## board from which your today's tasks are created.
target Trello Board name: YOUR_BOARD_NAME
## list from which your today's tasks are created.
target Trello List name: YOUR_LIST_NAME
## the following result will be output
[My Project]
-[] task1
-[] task2
```

Assume your YOUR_LIST_NAME list in YOUR_BOARD_NAME board in Trello has cards named "task1", "task2"

#### How to change todo list format
edit `/usr/local/bin/yukimt/task/todo/format.txt`

### Webhook
#### Brief Description
When you put a card in Trello to a certain list, start recording in Toggl.  
When you remove a card in Trello from the list, finish recording in Toggl.
#### How to Use
Replace uppercase parts with your own settings  
("##" is comment)  
If you skip [Account Information section](https://github.com/yuki-mt/todo#how-to-use), you may be asked more request to give account information.  
[Set up](https://github.com/yuki-mt/todo#set-up) before you try the following.

```
$ brew install heroku/brew/heroku
$ heroku login
Enter your Heroku credentials:
Email: YOUR_EMAIL
Password: YOUR_PASSWORD
$ heroku create
$ git push heroku master
$ ym-task webhook
Input Board and List Name in Trello for current work
target Trello Board name: YOUR_BOARD_NAME
target Trello List name: YOUR_LIST_NAME
## the URL that is opened when you execute "heroku open" command
callback url: YOUR_HEROKU_URL
Complete!
$ heroku config:set TARGET_LIST_ID=`ym-task trello-list`
$ heroku config:set TOGGL_TOKEN=`ym-task toggl-token`
```

Now, when you put or create a card on YOUR_LIST_NAME, Toggle automatically start recording your task.  
When you move or remove a card from YOUR_LIST_NAME, Toggle automatically stop recording your task.  

### Done
#### Brief Description
Output descriptions in a certain date in Toggl with spent time
#### How to Use
Replace uppercase parts with your own settings  
("##" is comment)  
If you skip [Account Information section](https://github.com/yuki-mt/todo#how-to-use), you may be asked more request to give account information.  
[Set up](https://github.com/yuki-mt/todo#set-up) before you try the following.

```
$ ym-task done
[My Project]
- [0.5] task3
- [2.0] task4

$ ym-task done -2
[My Project]
- [1.5] task1
- [1.0] task2
```

Assume

- today, you spent a half hour on task3 and spent 2 hours on task4
- 2 days before, you spent one and half hourson task1 and spent 1 hour on task2

#### How to change todo list format
edit `/usr/local/bin/yukimt/task/done/format.txt`

### Reset
#### Brief Description
reset stored account information
#### How to Use

```
$ ym-task import reset
Successfully delete Import setting
$ ym-task todo reset
Successfully delete Trello Target Board & List
$ ym-task setup-cred reset
Successfully delete Trello API data
Successfully delete Toggl API data
Successfully delete Github API data
$ ym-task setup-cred git reset 
Successfully delete Github API data
$ ym-task setup-cred trello reset 
Successfully delete Trello API data
$ ym-task setup-cred toggl reset 
Successfully delete Toggl API data
```

## Contributing
Always welcome for your contribution

## License & Authors
Author:: @yuki-mt  
License:: MIT
