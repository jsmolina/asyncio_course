import os
import sys
program = "python"
print("Process calling")
arguments = ["process.py"]
os.execvp(program, (program,) + tuple(arguments))
print("Good Bye!!")