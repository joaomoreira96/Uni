#!/bin/python
# lib for date and time ops
# import datetime
import time
# imports for exel writing
import xlsxwriter
# imports from haversine module the function itself and the Unit class
from haversine import haversine, Unit
# you can use this instead of pandas to open and read csv (and it's in python std lib!)
from csv import reader  # https://docs.python.org/3/library/csv.html
import os, sys

# import easyxlsx, xlsxreporter
# from openpyxl import Workbook
# from xlwt import Workbook
# Pandas is good for data related stuff but more in the area of data science
# import pandas as pd
# import numpy as np


def csvOpener(pfile):
	return reader(open(pfile, newline=''))


def csvParser(f, parsed_dict={'posl': [], 'tlist': []}, indexList=[0, 1, -1]):
	for row in f:
		if len(row) == 7:
			parsed_dict['tlist'].append(row[int(indexList[-1])])
			parsed_dict['posl'].append((float(row[indexList[0]]), float(row[indexList[1]])))  # position list is a list of tuples containing longitute and latitude
			# parsed_dict['dlist'].append()  # If time is to be process
	return parsed_dict


def totalDistance(dposl):
	td = 0
	for d in dposl:
		td += d
	return td


def totalTime(tlist, t_notation='%H:%M:%S'):
	return time.mktime(time.strptime(tlist[-1], t_notation)) - time.mktime(time.strptime(tlist[0], t_notation))


def velocityCounter(dposl, tdlist):
	vmsl = []
	vkmhl = []
	for i in range(0, len(tdlist)):
		vmsl.append(dposl[i] / tdlist[i])
		vkmhl.append(float(dposl[i] / tdlist[i]) * 3.6)
	return vmsl, vkmhl


def haversineList(posl):
	dposl = []
	for i in range(1, len(posl)):
		dposl.append(haversine(posl[i], posl[i - 1], unit=Unit.METERS))
	return dposl


def dtp2p(tlist, t_notation='%H:%M:%S'):  # delta time from p2p
	tdlist = []
	for i in range(0, len(tlist)):
		if i >= 1:
			_td = time.mktime(time.strptime(tlist[i], t_notation)) - time.mktime(time.strptime(tlist[i - 1], t_notation))
			tdlist.append(_td)
	return tdlist


def transportationDetection(vl):
	t = []
	for i in range(0, len(vl)):
		if round(vl[i]) == 0:
			t.append('Parado')
		if vl[i] <= 5:
			t.append("Andar/Correr")
		if vl[i] > 5 and vl[i] < 10:
			t.append("Carro/Transporte Publico/Sprint")
		if vl[i] >= 10:
			t.append("Carro/Transporte Publico")
	return t


def csvFinder(pathStr):
	return [os.path.join(root, f) for root, subdirs, files in os.walk(pathStr) for f in files if os.path.isfile(f) and f.endswith('.csv')]


def writer(pfile, content):  # to be removed this was for testing only
	with open(pfile, 'w+') as fileOut:
		for l in content:
			fileOut.write(f"{l}\n")


def workbookWriter(td, tt, tdlist, dposl, vkmhl, pName='trabalhofinal.xlsx'):
	workbook = xlsxwriter.Workbook(pName)
	worksheet = workbook.add_worksheet()
	worksheet.write('A1', 'tempo entre ponto e ponto, segundos')
	worksheet.write('B1', 'distancia entre dois pontos, metros')
	worksheet.write('C1', 'velocidade de deslocação, kilometros')
	worksheet.write('D1', 'meio de transporte utilizade')
	worksheet.write('E1', 'distância total percorrida, metros')
	worksheet.write('F1', 'tempo total gasto, segundos')
	worksheet.write('E3', td)
	worksheet.write('F3', tt)
	for i in range(0, 1775):
		worksheet.write(i + 2, 0, tdlist[i])
		worksheet.write(i + 2, 1, dposl[i])
		worksheet.write(i + 2, 2, vkmhl[i])
		# worksheet.write(i+2, 3, t[i])
	workbook.close()
	print(f"The report is in: {pName}")


def main(PFILE):
	# The main function of the module call this with a csv to parse
	t_notation = '%H:%M:%S'  # The used time notation
	# csv opening and parsing
	# csvRead = csvOpener(PFILE)
	# parsed dict
	# dparsed = csvParser(csvRead)
	dparsed = csvParser(csvOpener(PFILE))
	# dparsed is the return dict from csvParse()

	# haversine distance
	dposl = haversineList(dparsed['posl'])
	# delta time from p2p
	tdlist = dtp2p(dparsed['tlist'])

	# td
	td = totalDistance(dposl)
	# tt TotalTime
	tt = totalTime(dparsed['tlist'])
	# v
	vmsl, vkmhl = velocityCounter(dposl, tdlist)
	print(f"Total time taken:\n\t {tt} seconds\n\t {tt / 60} minutes\n\t {tt / 3600} hours")  # This is for testing
	print(f"Total distance:\n\t {td} meters\n\t {td / 1000} kilometers")  # This is for testing

	# text writers(only while xlsx is not being written
	# writer("timeTest.txt", tdlist)  # This is for testing
	# writer('distanceText.txt', dposl)  # This is for testing
	# writer("velocityText.txt", vmsl)
	# writer("khText.txt", vkmhl)

	workbookWriter(td, tt, tdlist, dposl, vkmhl)


if __name__ == '__main__':
	main('20081026094426.csv')
