#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------#
# Summary: Retrieve and filter issues data based on the given inputs.
# Name: issues.py
# Author: Paul Holtz
# Date: 2018-07-11
#-----------------------------------------------------------------------------#

import requests
import json
import getpass
import base64
from datetime import datetime
from tqdm import tqdm
from color import Color
import client


def issues(args):
	default_username = getpass.getuser()
	username = input("Username[{}]: ".format(default_username)) or default_username
	password = getpass.getpass(prompt="Password: ")
	authorization = base64.b64encode("{}:{}".format(username, password).encode()).decode("utf-8")

	search_results = client.get_my_open_issues(authorization)

	issues = []
	for issue in search_results["issues"]:
		issues.append({
			"key": issue["key"],
			"summary": issue["fields"]["summary"],
			"type": issue["fields"]["issuetype"]["name"],
			"created": issue["fields"]["created"],
			"updated": issue["fields"]["updated"],
			"status": issue["fields"]["status"]["name"],
			"description": issue["fields"]["description"],
			"author": issue["fields"]["creator"]["displayName"],
			"subtasks": issue["fields"]["subtasks"],
			"labels": issue["fields"]["labels"]
		})

	# Sort issues from the earliest to the latest
	issues = sorted(issues, key=lambda issue: datetime.strptime(issue["created"], "%Y-%m-%dT%H:%M:%S.%f%z"))

	# Reformat timestamps to be human readable
	for issue in issues:
		updated = datetime.strptime(issue["created"], "%Y-%m-%dT%H:%M:%S.%f%z")
		issue["created"] = updated.strftime("%B %d")

	for issue in issues:
		print("{}{}: {} [{}]{} {}".format(Color.BOLD, issue["key"], issue["summary"], issue["status"], Color.END, " ".join("<{}>".format(label) for label in issue["labels"])))
		print("{} created by {} on {}".format(issue["type"], issue["author"], issue["created"]))
		print("{}".format(issue["description"]))
		print("\n")