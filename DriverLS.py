from ls import ls
import sys
import os

def main():
	arguments_list = sys.argv
	if len(arguments_list) == 1:
		tester = ls(os.getcwd())
	elif len(arguments_list) == 2:
		tester = ls(arguments_list[1])
	tester.PrintDirContents()

if __name__ == "__main__":
	main()