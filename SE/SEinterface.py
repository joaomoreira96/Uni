#!/bin/python
# SE_3.4 interface to SE_3 module
import os, sys
import SE_3


def getFile():
	print(f"In this root directory, you have the this csv files:\n\t{SE_3.csvFinder('.')}")
	PFILE = input('Insira o nome/caminho do ficheiro: ')
	if os.path.isfile(PFILE):  # This allows for any file opening, given that the user has permisions to open it
		return PFILE
	else:
		print("The file/symlink you gave dosen't exist try again...")
		getFile()


def getIndexList(PFILE):
	pass
	# print the first parsable line and insert the index list
	SE_3.csvOpener(PFILE)


def argsParser():
	try:
		if len(sys.argv) == 1:
			print(f"{sys.argv[0]} usage:\n -f\t--file\tfile to process(required)\n --i=\t--indexList=\tlist of indexes to process(not required)(default=0,1,-1)")
		argList = {'file': ''}
		for arg in sys.argv[1:]:
			if arg.startswith('-f='):
				argList['file'] = arg.strip('-f=')
			if arg.startswith('--file='):
				argList['file'] = arg.strip('--file=')
			if arg.startswith('-i='):
				argList['indexList'] = arg.split('-i=')
			if arg.startswith('--indexList='):
				argList['indexList'] = arg.strip('-indexList=').strip(',')
		if argList['file'] != '':
			if isinstance(argList['indexList'], []):
				main(argList['file'], argList['indexList'])
			else:
				main(argList['file'], indexList=[0, 1, -1])
		return argList
	except Exception as e:
		print(e)


def main(PFILE, indexList=[0, 1, -1]):
	# run the functions from SE_3 cause code reusage(*****)
	dparsed = SE_3.csvParser(SE_3.csvOpener(PFILE), indexList)
	dposl = SE_3.haversineList(dparsed['posl'])
	tdlist = SE_3.dtp2p(dparsed['tlist'])
	td = SE_3.totalDistance(dposl)
	tt = SE_3.totalTime(dparsed['tlist'])
	vmsl, vkmhl = SE_3.velocityCounter(dposl, tdlist)
	print(f"Total time taken:\n\t {tt} seconds\n\t {tt / 60} minutes\n\t {tt / 3600} hours")  # This is for testing
	print(f"Total distance:\n\t {td} meters\n\t {td / 1000} kilometers")  # This is for testing


def menu():
	indexList = [0, 1, -1]
	argsList = argsParser()
	while True:
		print("************MAIN MENU**************")
		choice = input("""
	\t\t1/A: Insert the filename/path
	\t\t\t2/B: The index of the analised data
	\t\t\t3/C: The ammount of lines to ignore(Not implemented)\n(The way its implemented it only analyzes 7 dimentional lines)
	\t\t\t4/D: Produce Reports(skip input and run with default values)
	\t\t\t5/E: In which line is the header(Not implemented)
	\t\t\t6/Q: Quit menu
	\t\t\tPlease enter your choice: """)
		if choice == "A" or choice == "a" or choice == 1:
			PFILE = getFile()
		elif choice == "B" or choice == "b" or choice == 2:
			indexList = getIndexList()
		elif choice == "C" or choice == "c" or choice == 3:
			pass
			# ignore this option the code does this on its own
		elif choice == "D" or choice == "d" or choice == 4:
			main(PFILE, indexList)
		elif choice == "Q" or choice == "q" or choice == 'quit' or choice == 'Quit' or choice == "exit" or choice == 5:
			sys.exit(0)
		else:
			print("You must only select either A,B,C, or D.\nPlease try again.")


if __name__ == '__main__':
	menu()
