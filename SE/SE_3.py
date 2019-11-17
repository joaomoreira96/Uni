#!/bin/python3
# lib for date and time ops
import datetime
import time
# imports for exel writing
import xlsxwriter
import easyxlsx, xlsxreporter
from xlwt import Workbook 
# Pandas is good for data related stuff but more in the area of data science
import pandas as pd
import numpy as np
# haversine module
from haversine import haversine, Unit
# you can use this instead of pandas to open and read csv (and it's in python std lib!)
import csv  # https://docs.python.org/3/library/csv.html


def csvOpener(pfile):
	return csv.reader(open(pfile, newline=''))


def writer(pfile, content):
	with open(pfile, 'w+') as fileOut:
		for l in content:
			fileOut.write(f"{l}\n")


def main():
	# some variables
	tlist = []  # time list
	tdlist = []  # time delta list
	posl = []  # position list [(lat, lon)]
	dposl = []  # delta distance
	td = 0.0  # total distance
	vmsl = []  # m/s velocity
	vkmhl = []  # km/h velocity
	t_notation = '%H:%M:%S'  # The used time notation
	# csv opening and parsing
	csvRead = csvOpener('20081026094426.csv')
	for row in csvRead:
		if len(row) == 7:
			tlist.append(row[-1])
			posl.append((float(row[0]), float(row[1])))

	# dt from p2p
	for i in range(0, len(tlist)):
		if i >= 1:
			_td = time.mktime(time.strptime(tlist[i], t_notation)) - time.mktime(time.strptime(tlist[i - 1], t_notation))
			tdlist.append(_td)
	# tt
	tt = time.mktime(time.strptime(tlist[-1], t_notation)) - time.mktime(time.strptime(tlist[0], t_notation))
	for i in range(1, len(posl)):
		dposl.append(haversine(posl[i], posl[i - 1], unit=Unit.METERS))
	# td
	for d in dposl:
		td += d
	# v
	for i in range(0, 1775):
		vmsl.append(dposl[i] / tdlist[i])
		vkmhl.append(float(dposl[i] / tdlist[i]) * 3.6)
	print(f"Total time taken:\n\t {tt} seconds\n\t {tt / 60} minutes\n\t {tt / 3600} hours")  # This is for testing
	print(f"Total distance:\n\t {td} meters\n\t {td / 1000} kilometers")  # This is for testing
	# text writers(only while xlsx is not being written
	writer("timeTest.txt", tdlist)  # This is for testing
	writer('distanceText.txt', dposl)  # This is for testing
	writer("velocityText.txt", vmsl)
	writer("khText.txt", vkmhl)

	wb = Workbook() 
	sheet1 = wb.add_sheet('Sheet 1') 
	sheet1.write(0, 1, 'tempo entre ponto e ponto') 
	sheet1.write(0, 2, 'distancia entre dois pontos') 
	sheet1.write(0, 3, 'velocidade de deslocação') 
	sheet1.write(0, 4, 'meio de transporte utilizado') 
	sheet1.write(0, 5, 'distância total percorrida') 
	sheet1.write(0, 6, 'tempo total gasto')

	ii = 0

	while ii <= 1775:
		sheet1.write(1, tdlist[ii])
		ii += 1
	

	wb.save('trabalhoFinal.xls') 

if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		print(e)
