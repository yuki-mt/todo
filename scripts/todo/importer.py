#!/usr/bin/python
#coding=utf-8
import json
import os
import urllib2
import urllib
from credential.git import GitCredentialProvider
from credential.trello import TrelloCredentialProvider
from todo.trello import TrelloTodo


class Importer(object):
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.conf_path = current_dir + "/.importer.json"
        self.source_type_key = "source_type"
        self.source_key = "source"
        self.url_key = "repository_url"
        self.repo_key = "repository_id"
        self.keys = [self.source_type_key, self.source_key, self.repo_key, self.url_key]

        provider = TrelloCredentialProvider()
        self.trello_cred = provider.get()
        provider = GitCredentialProvider()
        self.git_cred = provider.get()

        self.todo = TrelloTodo()
        self.trello_conf = self.todo.get_conf()

    def sync(self):
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

        issues = self.get_issues(conf)
        self.import_issues(conf, issues)
        print "Complete!"

    def filter_conf(self, conf):
        result = {}
        for key in self.keys:
            if key in conf:
                result[key] = conf[key]
        return result

    def ask(self):
        source_type = raw_input("""\
import by what?
[g: Github label, z: Zenhub Board Name]: """)
        source = raw_input("""\
label or board name
(use , for multiple choices. e.g. 'In Progress,Backlog')
If you want all issues assigned to you, just hit Enter

input here: """)
        source = source.split(',')
        url = raw_input("Repository URL: ")
        url = url.replace("github.com", "api.github.com/repos")

        repo_id = raw_input("Repository ID (Enter if you do not use Zenhub): ")
        return {
            self.source_type_key: source_type,
            self.source_key: source,
            self.url_key: url,
            self.repo_key: repo_id
        }
            
    def get_issues(self, conf):
        # TODO: get all issues by using pagination
        url = conf[self.url_key] + "/issues?assignee=%s&per_page=100" % self.git_cred['username']
        request = urllib2.Request(url)
        request.add_header("Authorization", "token %s" % self.git_cred['github'])
        result = urllib2.urlopen(request)
        response = json.loads(result.read())
        result.close()

        issues = []
        for r in response:
            issue = {}
            issue['url'] = r['url'].replace("api.github.com/repos", "github.com")
            issue['number'] = r['number']
            issue['title'] = r['title']
            issue['labels'] = [l['name'].encode('utf-8') for l in r['labels']]
            issues.append(issue)
        return self.filter_issues(conf, issues)

    def filter_issues(self, conf, issues):
        if conf[self.source_key] == ['']:
            return issues
        if conf[self.source_type_key] == 'g':
            result = []
            labels = conf[self.source_key]
            if not labels:
                return issues
            for issue in issues:
                for label in labels:
                    if label in issue['labels']:
                        result.append(issue)
                        break
            return result
        else:
            url = "https://api.zenhub.io/p1/repositories/%s/board" % conf[self.repo_key]
            request = urllib2.Request(url)
            request.add_header("X-Authentication-Token", self.git_cred['zenhub'])
            result = urllib2.urlopen(request)
            response = json.loads(result.read())
            result.close()

            zen_issues = []
            for r in response['pipelines']:
                if r['name'] in conf[self.source_key]:
                    numbers = [i['issue_number'] for i in r['issues']]
                    zen_issues.extend(numbers)

            result = []
            for issue in issues:
                if issue['number'] in zen_issues:
                    result.append(issue)
            return result

    def import_issues(self, conf, issues):
        list_id = self.trello_conf[self.todo.list_key]['id']
        cards = self.todo.get_cards(list_id)
        card_names = [c['name'] for c in cards]
        base_url = "https://trello.com/1/cards?key=%s&token=%s&idList=%s" % (
            self.trello_cred['key'], self.trello_cred['token'], list_id
        )

        for i in issues:
            if i['title'] in card_names:
                continue
            param = {'name': i['title'].encode("utf-8"), 'desc': i['url'].encode("utf-8")}
            url = base_url + '&' + urllib.urlencode(param)
            result = urllib2.urlopen(url, {})
            result.close()


    def save(self, conf):
        with open(self.conf_path, 'w') as f:
            f.write(json.dumps(conf))

    def reset(self):
        os.remove(self.conf_path)
        print "Successfully delete Import setting"
