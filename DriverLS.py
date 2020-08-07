from ls import ls
import sys
import os
import cProfile

class DriverLS:
    _valid_args = set()
    _valid_args.add("R")
    _valid_args.add("-")

    def __init__(self):
        self._args = sys.argv
        self._args_count = len(sys.argv)
        self._recursive_flag = False
        self._path_provided = False
        self._path = ""
        self._exception_arg = ""

    def ProcessPathArg(self, path_arg):
        if os.path.exists(path_arg) == True:
            self._path_provided = True
            self._path = path_arg
        else:
            raise Exception("Invalid Path")

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
    def Run(self):
        self._args.pop(0)
        for each in self._args:
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

        if not self._path_provided:
            self._path = os.getcwd()

        runner = ls(self._path, self._recursive_flag)
        runner.PrintDirContents()


            
def main():
    driver = DriverLS()
    driver.Run()

if __name__ == "__main__":
    #cProfile.run("main()")
    main()