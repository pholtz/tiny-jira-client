#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------#
# Summary: Interact with the jira rest api.
# Name: jira.py
# Author: Paul Holtz
# Date: 2018-07-10
#-----------------------------------------------------------------------------#

import argparse
from comments import comments
from issues import issues


def main():
	parser = argparse.ArgumentParser(description="Interact with the jira rest api")
	parser.add_argument("--verbose", action="store_true", help="Enable more verbose output")
	subparsers = parser.add_subparsers()

	comments_parser = subparsers.add_parser("comments", help="Retrieve the most recent comments for the given user")
	comments_parser.add_argument("--limit", type=int, help="Limit the number of returned comments")
	comments_parser.set_defaults(func=comments)
	
	issues_parser = subparsers.add_parser("issues", help="Retrieve the currently assigned issues for the given user")
	issues_parser.set_defaults(func=issues)
	
	args = parser.parse_args()
	if hasattr(args, "func"):
		args.func(args)
	else:
		parser.print_help()


if __name__ == "__main__":
	main()
