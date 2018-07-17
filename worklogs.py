#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------#
# Summary: Retrieve and filter comments data based on the given inputs.
# Name: worklogs.py
# Author: Paul Holtz
# Date: 2018-07-16
#-----------------------------------------------------------------------------#

import requests
import json
import getpass
import base64
from datetime import datetime
from tqdm import tqdm
from color import Color
import client


def worklogs(args):
	default_username = getpass.getuser()
	username = input("Username[{}]: ".format(default_username)) or default_username
	password = getpass.getpass(prompt="Password: ")
	authorization = base64.b64encode("{}:{}".format(username, password).encode()).decode("utf-8")

	search_results = client.get_my_open_issues(authorization)

	worklogs = []
	for issue in tqdm(search_results["issues"]):
		worklog_results = client.get_issue_worklogs(authorization, issue["key"])
		for worklog in worklog_results["worklogs"]:
			if worklog["author"]["key"] == username:
				worklogs.append({\
					"issue": issue["key"],
					"summary": issue["fields"]["summary"],
					"author": worklog["author"]["displayName"],
					"started": worklog["started"],
					"time_spent": worklog["timeSpent"],
					"time_spent_seconds": worklog["timeSpentSeconds"],
					"comment": worklog["comment"]
				})

	# Sort worklogs from the earliest to the latest
	sorted_worklogs = sorted(worklogs, key=lambda worklog: datetime.strptime(worklog["started"], "%Y-%m-%dT%H:%M:%S.%f%z"))

	# Reformat timestamps to be human readable
	for worklog in sorted_worklogs:
		updated = datetime.strptime(worklog["started"], "%Y-%m-%dT%H:%M:%S.%f%z")
		worklog["started"] = updated.strftime("%a, %B %d")
		worklog["comment"] = worklog["comment"].replace("\r\n", "")

	for worklog in sorted_worklogs:
		print("{}: \t{} logged {} to {} ({})".format(worklog["started"], worklog["author"], worklog["time_spent"], worklog["issue"], worklog["summary"]))