#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------#
# Summary: Retrieve and filter comments data based on the given inputs.
# Name: comments.py
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


def comments(args):
	default_username = getpass.getuser()
	username = input("Username[{}]: ".format(default_username)) or default_username
	password = getpass.getpass(prompt="Password: ")
	authorization = base64.b64encode("{}:{}".format(username, password).encode()).decode("utf-8")

	search_results = client.get_my_open_issues(authorization)

	comments = []
	for issue in tqdm(search_results["issues"]):
		comment_results = client.get_issue_comments(authorization, issue["key"])
		for comment in comment_results["comments"]:
			comments.append({\
				"key": issue["key"],
				"summary": issue["fields"]["summary"],
				"created": comment["created"],
				"updated": comment["updated"],
				"author": comment["author"]["displayName"],
				"comment": comment["body"]
			})

	# Sort comments from the earliest to the latest
	sorted_comments = sorted(comments, key=lambda comment: datetime.strptime(comment["updated"], "%Y-%m-%dT%H:%M:%S.%f%z"))

	# Reformat timestamps to be human readable
	for comment in sorted_comments:
		updated = datetime.strptime(comment["updated"], "%Y-%m-%dT%H:%M:%S.%f%z")
		comment["updated"] = updated.strftime("%b %d")
		comment["comment"] = comment["comment"].replace("\r\n", "")

	grouped_comments = {}
	for comment in sorted_comments:
		if comment["key"] in grouped_comments:
			grouped_comments[comment["key"]].append(comment)
		else:
			grouped_comments[comment["key"]] = [comment]

	for key, value in grouped_comments.items():
		print("{}{}: {}{}".format(Color.BOLD, key, value[0]["summary"], Color.END))
		for comment in value:
			print("  {} {}: {}".format(comment["updated"], comment["author"], comment["comment"]))
		print("\n")