@ECHO OFF
if $%~1$ == "" GOTO NO_ARG else GOTO WARG
:WARG
py C:\Users\jakel\Desktop\python\ls\DriverLS.py %1
GOTO LEAVE
:NO_ARG
py C:\Users\jakel\Desktop\python\ls\DriverLS.py
GOTO LEAVE
:LEAVE