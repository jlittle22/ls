from ls import ls
import sys
import os
import cProfile

""" Driver class for the list command """
class DriverLS:
	# set of valid command line options
    _valid_args = set()
    _valid_args.add("R")
    _valid_args.add("-")

    """ initializer for the class... gathers command line arguments and sets defaults """
    def __init__(self):
        self._args = sys.argv
        self._args_count = len(sys.argv)
        self._recursive_flag = False
        self._path_provided = False
        self._path = ""
        self._exception_arg = ""

    """ accepts a path and validates """
    def ProcessPathArg(self, path_arg):
        if os.path.exists(path_arg) == True:
            self._path_provided = True
            self._path = path_arg
        else:
            raise Exception("Invalid Path")

    """ processes an option argument and adjusts flags as necessary """
    def ProcessOptionArg(self, option):
        chars = list(option)
        for i in range(len(chars)):
            if chars[i] not in self._valid_args:
                self._exception_arg = chars[i]
                raise Exception("Invalid Options " + chars[i])
            else:
                if chars[i] == "R":
                    self._recursive_flag = True
                elif (chars[i] == "-"):
                    if (i == len(chars) - 1):
                        self._exception_arg = "-"
                        raise Exception("Invalid '-' position")

    """ driver function to process command line and run the list program """
    def Run(self):
        self._args.pop(0)  # remove the 'python' argument
        for each in self._args:
        	# each argument can either be an option or a target directory/file
            if each[0] == "-":
                try:
                    self.ProcessOptionArg(each)
                except:
                    print("ls: invalid option -- '" + self._exception_arg + "'")
                    sys.exit()
            else:
                try:
                    self.ProcessPathArg(each)
                except:
                    print("ls: cannot access " + each + ": No such file or directory")
                    sys.exit()
        # if the user has not provided a path to a target, default to listing the current working directory
        if not self._path_provided:
            self._path = os.getcwd()

        # init and run the list program with our processed flags
        runner = ls(self._path, self._recursive_flag)
        runner.PrintDirContents()


            
def main():
    driver = DriverLS()
    driver.Run()

if __name__ == "__main__":
    #cProfile.run("main()")
    main()