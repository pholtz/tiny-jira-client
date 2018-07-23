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
from environment import Environment


def get_my_open_issues(authorization):
	disable_https_warnings()
	payload = {"jql": "assignee=currentuser() and project={} and status != Closed".format(Environment.project)}
	headers = {"Content-Type": "application/json", "Authorization": "Basic {}".format(authorization)}
	search_response = requests.post("https://{}/rest/api/latest/search".format(Environment.hostname), headers=headers, data=json.dumps(payload), verify=False)
	if search_response.status_code != 200:
		raise RuntimeError("Error while retrieving assigned issues")
	search_results = json.loads(search_response.text)
	return search_results


def get_my_recent_issues(authorization):
	disable_https_warnings()
	payload = {"jql": "assignee=currentuser() and project={} and updated > -30d".format(Environment.project)}
	headers = {"Content-Type": "application/json", "Authorization": "Basic {}".format(authorization)}
	search_response = requests.post("https://{}/rest/api/latest/search".format(Environment.hostname), headers=headers, data=json.dumps(payload), verify=False)
	if search_response.status_code != 200:
		raise RuntimeError("Error while retrieving assigned issues")
	search_results = json.loads(search_response.text)
	return search_results


def get_worked_issues(authorization):
	disable_https_warnings()
	payload = {"jql": "worklogAuthor=currentUser() and project={} and updated > -30d".format(Environment.project)}
	headers = {"Content-Type": "application/json", "Authorization": "Basic {}".format(authorization)}
	search_response = requests.post("https://{}/rest/api/latest/search".format(Environment.hostname), headers=headers, data=json.dumps(payload), verify=False)
	if search_response.status_code != 200:
		raise RuntimeError("Error while retrieving assigned issues")
	search_results = json.loads(search_response.text)
	return search_results


def get_custom_issues(authorization, query):
	disable_https_warnings()
	payload = {"jql": query}
	headers = {"Content-Type": "application/json", "Authorization": "Basic {}".format(authorization)}
	search_response = requests.post("https://{}/rest/api/latest/search".format(Environment.hostname), headers=headers, data=json.dumps(payload), verify=False)
	if search_response.status_code != 200:
		raise RuntimeError("Error while retrieving assigned issues")
	search_results = json.loads(search_response.text)
	return search_results


def get_issue_comments(authorization, issue_key):
	headers = {"Content-Type": "application/json", "Authorization": "Basic {}".format(authorization)}
	comment_response = requests.get("https://{}/rest/api/latest/issue/{}/comment".format(Environment.hostname, issue_key), headers=headers, verify=False)
	if comment_response.status_code != 200:
		print("Error while retrieving comments for issue {}".format(issue_key))
		return
	comment_results = json.loads(comment_response.text)
	return comment_results


def get_issue_worklogs(authorization, issue_key):
	headers = {"Content-Type": "application/json", "Authorization": "Basic {}".format(authorization)}
	worklog_response = requests.get("https://{}/rest/api/latest/issue/{}/worklog".format(Environment.hostname, issue_key), headers=headers, verify=False)
	if worklog_response.status_code != 200:
		print("Error while retrieving worklogs for issue {}".format(issue_key))
		return
	worklog_results = json.loads(worklog_response.text)
	return worklog_results


def disable_https_warnings():
	requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)