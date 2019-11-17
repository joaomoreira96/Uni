#!/bin/python3
# lib for date and time ops
import datetime
import time
# imports for exel writing
import xlsxwriter
import easyxlsx, xlsxreporter
# Pandas is good for data related stuff but more in the area of data science
import pandas as pd
import numpy as np
# you can use this instead of pandas to open and read csv (and it's in python std lib!)
import csv  # https://docs.python.org/3/library/csv.html


def csvOpener(pfile):
	return csv.reader(open(pfile, newline=''))


def main():
	# some variables
	tlist = []  # given that the day is the same only the time will change so only one dimension
	#
	csvRead = csvOpener('20081026094426.csv')
	for row in csvRead:
		if len(row) == 7:
			tlist.append(row[-1])
	# the csv file is []

	# dt from p2p
	for i in range(0, len(tlist)):
		if i >= 1:
			t_notation = '%H:%M:%S'
			print(f"Time taken from last point {time.mktime(time.strptime(tlist[i], t_notation)) - time.mktime(time.strptime(tlist[i - 1], t_notation))}")
		else:
			print(f"First point at: {tlist[i]} hours")
	# tt
	print(tlist[1])


if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		print(e)
