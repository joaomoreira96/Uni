#!/bin/python
# SE_3.4 interface to SE_3 module
import os, sys
# get the code from SE_3.py
import SE_3

if __name__ == '__main__':
	print("************MAIN MENU**************")
	choice = input("""
\t\t1/A: Escolha o ficheiro a analisar
\t\t\t2/B: View Student details
\t\t\t3/C: Search by ID number
\t\t\t4/D: Produce Reports
\t\t\t5/Q: Quit menu
\t\t\t6/Please enter your choice: """)
	if choice == "A" or choice == "a" or choice == 1:
		print(f"In this root directory, you have the this csv files:\n\t{SE_3.csvFinder('.')}")
		PFILE = input('Insira o nome/caminho do ficheiro: ')
		if os.path.isfile(PFILE):  # This allows for any file opening, given that the user has permisions to open it
			PFILE = PFILE
		else:
			print("The file/symlink you gave dosen't exist try again...")
			sys.exit(1)
	elif choice == "B" or choice == "b" or choice == 2:
		pass
		# print the first parsable line of csv and ask for the field dimensions
		print()
	elif choice == "C" or choice == "c" or choice == 3:
		pass
		# ignore this option the code does this on its own
	elif choice == "D" or choice == "d" or choice == 4:
		pass
	elif choice == "Q" or choice == "q" or choice == 'quit' or choice == 'Quit' or choice == "exit" or choice == 5:
		sys.exit()
	else:
		print("You must only select either A,B,C, or D.\nPlease try again.")
	SE_3.main(PFILE)
