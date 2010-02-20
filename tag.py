#! /usr/bin/python3
import os, sys

TAG = (
"""
#$Rev$     
#$Author$  
#$Date$ 

#This file is part of Vitamin Project

""")

try:
    path = sys.argv[1]
except IndexError:
    print("Please enter path as argument")

if os.path.splitext(path)[1] == ".py":
    try:
        with open(path, "r+") as f:
            text = f.read()
            f.seek(0, whence=0)
            f.write(TAG + text)
    except Exception as msg:
        sys.exit(msg)
else:
    print("This file is not .py")

