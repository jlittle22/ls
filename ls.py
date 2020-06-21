import os
import sys
import shutil
import math
import subprocess
import time

# small class to contain the file/directory names
class ColoredName:
	def __init__(self, new_name, new_length):
		self.name_string = new_name    # the ANSI color-formatted string
		self.real_length = new_length  # the length of the filename (not including ANSI chars)

# class implements the ls command
class ls:
	# __colors contains some ANSI escape sequences that can be used to format names
	__colors = {} 
	__colors["RED"] = "\u001b[31m"
	__colors["DIRECTORY"] = "\u001b[34m"
	__colors["REG_FILE"] = "\u001b[37m"
	__colors["GREEN"] = "\u001b[32m"
	__colors["DEFAULT"] = "\u001b[32m"

	__std_min_padding = 2  # standard minimum number of spaces between file/directory names

	#
	# @brief initializer for ls class
	# @param path_string path to the target directory as a string
	#
	def __init__(self, path_string):
		os.system("")
		self._directory_path = path_string

	#
	# @brief shuts down the program in the case of an error
	#
	def __ShutDown(self):
		print(self.__colors["DEFAULT"], end = "")
		sys.exit()

	#
	# @brief returns the complete path to a file/directory in the target directory
	# @param element_name a file/directory name as a string
	#
	def __CreatePath(self, element_name):
		return self._directory_path + '\\' + element_name

	#
	# @brief retrieves the target directory's contents in a list of strings
	#
	def __GetDirAsList(self):
		try:
			dir_list = os.listdir(self._directory_path)
		except FileNotFoundError:
			print("Directory " + self._directory_path + " not found")
			self.__ShutDown()
		return dir_list

	# TODO - NOT working/complete
	def __IsExecutable(self, file_name):
		output = subprocess.Popen("call " + file_name, stdout = subprocess.PIPE, shell= True)

	#
	# @brief correctly formats a file's name string based on its identity
	# @param file_name the file's name as a string
	# @return the new ANSI color-formatted string 
	#
	def __ProcessFile(self, file_name):
		try:
			return self.__colors["REG_FILE"] + file_name
		except:
			print("Unexpected Error for file " + self.__CreatePath(file_name))
			self.__ShutDown()
	#
	# @brief correctly formats a directory's name string
	# @param dir_name directory name as a string
	# @return the formatted ANSI color string
	#
	def __ProcessDir(self, dir_name):
		try:
			return self.__colors["DIRECTORY"] + dir_name
		except: 
			print("Unexpected Error for directory " + self.__CreatePath(dir_name))
			self.__ShutDown()
	#
	# @brief formats the output matrix and prints
	# @param colored_names_matrix a matrix of ColoredName objects arranged in the printing positions
	#
	def __FormatOutput(self, colored_names_matrix):
		num_cols = len(colored_names_matrix)
		max_rows = len(colored_names_matrix[0])
		size = self._longest_length + self.__std_min_padding
		for i in range(max_rows):
			for j in range(num_cols):
				if(i >= len(colored_names_matrix[j])):
					break
				offset = size - colored_names_matrix[j][i].real_length
				print_me = colored_names_matrix[j][i].name_string + str(' ' * offset)
				print(print_me, end = "")
			if i != max_rows-1:
				print()

	#
	# @brief finds the length (not including ANSI chars) of the longest name string in colored_names
	# @param colored_names list of ColoredName objects
	# @return the length as an int
	#
	def __FindLengthOfLongestName(self, colored_names):
		max_length = 0
		for i in range(len(colored_names)):
			if colored_names[i].real_length > max_length:
				max_length = colored_names[i].real_length
		return max_length

	#
	# @brief organized the contents of colored_names in a matrix that represents print order 
	#        to ensure that the output fits inside the width of the terminal
	# @param colored_names list of ColoredName objects 
	# @return the matrix spine (list of lists)
	#
	def __PackMatrix(self, colored_names):
		terminal_size = shutil.get_terminal_size().columns
		self._longest_length = self.__FindLengthOfLongestName(colored_names)
		
		# find the worst case number of words that can fit in the terminal's width
		num_words_in_terminal_width = terminal_size // (self._longest_length + self.__std_min_padding)

		# find the maximum number of words possible in each column
		max_words_per_col = math.ceil(len(colored_names) / num_words_in_terminal_width)

		matrix_spine = []
		while len(colored_names) != 0:
			curr_col_count = 0
			current_col = []
			# load elements into column and append it... repeat
			while ((curr_col_count < max_words_per_col)) and (len(colored_names) != 0):
				new_element = colored_names.pop(0)
				current_col.append(new_element)
				curr_col_count += 1
			matrix_spine.append(current_col)

		return matrix_spine


	def PrintDirContents(self):
		# get directory as list of strings
		dir_list = self.__GetDirAsList()

		# color format and add each element in directory to list of ColoredNames
		colored_names = []
		for each in dir_list:
			if os.path.isfile(self.__CreatePath(each)) == True:
				colored_names.append(ColoredName(self.__ProcessFile(each), len(each)))
			elif os.path.isdir(self.__CreatePath(each)) == True:
				colored_names.append(ColoredName(self.__ProcessDir(each), len(each)))
			else: 
				raise Exception("Error: unknown object " + self.__CreatePath(each))
				self.__ShutDown()

		# if the directory is empty, print newline and exit
		if not dir_list:
			print()
		else:
			# convert ColoredName list to printable matrix
			matrix = self.__PackMatrix(colored_names)

			# format and print the matrix contents
			self.__FormatOutput(matrix)

			# reset the terminal's text color to the default
			print(self.__colors["DEFAULT"], end = "")
