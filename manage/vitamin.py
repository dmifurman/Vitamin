#!/usr/bin/python3

import os
import sys

sys.path.append("../")
sys.path.append(".")

from manage.iscript import IScript

WORKDIR = "."
SCRIPTS = os.path.join(WORKDIR, "scripts")
assert WORKDIR
assert os.path.exists(SCRIPTS)

class ScriptsResolver():

    def __init__(self):
        self.scripts = {}
        self.collect_scripts()
        print("{0} scripts found: {1}".format(
            len(self.scripts),
            ",".join(self.scripts)))
        
        if len(sys.argv) > 1:
            script = sys.argv[1]
            if script.lower() in self.scripts:
                self.scripts[script].run()
            else:
                print("Script '{0}' not found :'-(".format(script))               

    
    def collect_scripts(self):
        files = [x for x in os.listdir(SCRIPTS) if
            os.path.splitext(x)[1] == ".py" and
            not x.startswith("_")]
        
        def __foo(name):
            return "scripts." + name.replace(".py", "")
    
        modules = map(__foo, files)
        for m in modules:
            imp = __import__(m, fromlist=[1])
            try:
                script = [value for name, value in imp.__dict__.items() 
                          if not name.startswith("_")
                          and issubclass(value, IScript)][0]
                self.scripts[m.split(".")[-1].lower()] = script
            except KeyError:
                print("bad %s file" % m)            

if __name__ == "__main__":
    resolver = ScriptsResolver()
    
    
