#!/bin/python3
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
# optimize cpu time and memory usage by specifing the imports(functions and classes instead of the full bloated modules)

# import easyxlsx, xlsxreporter
# from openpyxl import Workbook
# from xlwt import Workbook
# Pandas is good for data related stuff but more in the area of data science
# import pandas as pd
# import numpy as np


def csvOpener(pfile):
	return reader(open(pfile, newline=''))


def csvParser(f):
	# Use a dictionary for storing the different arrays in the future
	parsed_dict = {'posl': [], tlist: []}
	for row in f:
		if len(row) == 7:
			tlist.append(row[-1])
			posl.append((float(row[0]), float(row[1])))
	return parsed_dict


def totalDistance(dposl):
	td = 0
	for d in dposl:
		td += d


def writer(pfile, content):
	with open(pfile, 'w+') as fileOut:
		for l in content:
			fileOut.write(f"{l}\n")


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


def totalTime(tlist, t_notation='%H:%M:%S'):
	return time.mktime(time.strptime(tlist[-1], t_notation)) - time.mktime(time.strptime(tlist[0], t_notation))


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


def argsParser():
	try:
		argList = []
		for arg in sys.argv[1:]:
			pass
			# File can be accepted, 
		return argList
	except Exception as e:
		print(e)


def main():
	# some variables  # For now this variables will be globals while this is still being developed
	tlist = []  # time list
	tdlist = []  # time delta list
	posl = []  # position list [(lat, lon)]
	dposl = []  # delta distance
	td = 0.0  # total distance
	vmsl = []  # m/s velocity
	vkmhl = []  # km/h velocity
	t_notation = '%H:%M:%S'  # The used time notation
	PFILE = '20081026094426.csv'
	# csv opening and parsing
	csvRead = csvOpener(PFILE)

	# haversine distance
	dposl = haversineList(posl)

	# td
	td = totalDistance(dposl)
	# tt TotalTime
	tt = totalTime(tlist)
	# v
	for i in range(0, 1775):
		vmsl.append(dposl[i] / tdlist[i])
		vkmhl.append(float(dposl[i] / tdlist[i]) * 3.6)
	print(f"Total time taken:\n\t {tt} seconds\n\t {tt / 60} minutes\n\t {tt / 3600} hours")  # This is for testing
	print(f"Total distance:\n\t {td} meters\n\t {td / 1000} kilometers")  # This is for testing
	# text writers(only while xlsx is not being written
	# writer("timeTest.txt", tdlist)  # This is for testing
	# writer('distanceText.txt', dposl)  # This is for testing
	# writer("velocityText.txt", vmsl)
	# writer("khText.txt", vkmhl)

	workbook = xlsxwriter.Workbook('trabalhofinal.xlsx')
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

	print("************MAIN MENU**************")
	choice = input("""
\t\t1/A: Escolha o ficheiro a analisar
\t\t\t2/B: View Student details
\t\t\t3/C: Search by ID number
\t\t\t4/D: Produce Reports
\t\t\t5/Q: Quit menu
\t\t\t6/Please enter your choice: """)
	if choice == "A" or choice == "a" or choice == 1:
		PFILE = input('Insira o nome/caminho do ficheiro: ')
		if os.path.isfile(PFILE):
			PFILE = PFILE
	elif choice == "B" or choice == "b" or choice == 2:
		pass
	elif choice == "C" or choice == "c" or choice == 3:
		pass
	elif choice == "D" or choice == "d" or choice == 4:
		pass
	elif choice == "Q" or choice == "q" or choice == 'quit' or choice == 'Quit' or choice == "exit" or choice == 5:
		sys.exit()
	else:
		print("You must only select either A,B,C, or D.\nPlease try again.")


if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		print(e)
