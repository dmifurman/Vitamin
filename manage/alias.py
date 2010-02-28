#!/usr/bin/python3
import re
import os
import sys

FILE = sys.argv[0]
if not FILE:
    sys.exit()

import vitascript
VITAMIN_SCRIPT = vitascript.__file__

SHELL = os.environ["SHELL"]
HOME = os.environ["HOME"]
ALIAS = "alias vitamin='{0}'".format(VITAMIN_SCRIPT)

CMD = "echo " + repr(ALIAS)
regexp = re.compile("""alias\s+vitamin\s*?=\s*?["'].*?["']""")

if __name__ == "__main__":
    
    if os.path.exists("/usr/bin"):
        print("Making link...")
        if os.path.exists("/usr/bin/vitamin"):
            os.remove("/usr/bin/vitamin")
            print("Old link has been removed..")
        os.popen("ln {0} /usr/bin/vitamin --symbolic".format(repr(VITAMIN_SCRIPT)))
        print("Executable access...")
        os.popen("chmod +x " + repr(VITAMIN_SCRIPT))
        print("All done!")
        print()
        print("Use 'vitamin' command to control your sites")
        print()
    else:
        print("Strange system without /usr/bin")
        
    
                
    
            
            

