#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------#
# Summary: Create and send requests to the jira rest api.
# Name: client.py
# Author: Paul Holtz
# Date: 2018-07-11
#-----------------------------------------------------------------------------#

import requests
import json
from urllib3.exceptions import InsecureRequestWarning

hostname = "jira.qvcdev.qvc.net"


def get_my_open_issues(authorization):
	disable_https_warnings()
	payload = {"jql": "assignee=currentuser() and project=ITCM and status != Closed"}
	headers = {"Content-Type": "application/json", "Authorization": "Basic {}".format(authorization)}
	search_response = requests.post("https://{}/rest/api/latest/search".format(hostname), headers=headers, data=json.dumps(payload), verify=False)
	if search_response.status_code != 200:
		raise RuntimeError("Error while retrieving assigned issues")
	search_results = json.loads(search_response.text)
	return search_results


def get_issue_comments(authorization, issue_key):
	headers = {"Content-Type": "application/json", "Authorization": "Basic {}".format(authorization)}
	comment_response = requests.get("https://{}/rest/api/latest/issue/{}/comment".format(hostname, issue_key), headers=headers, verify=False)
	if comment_response.status_code != 200:
		print("Error while retrieving comments for issue {}".format(issue_key))
		return
	comment_results = json.loads(comment_response.text)
	return comment_results


def disable_https_warnings():
	requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)