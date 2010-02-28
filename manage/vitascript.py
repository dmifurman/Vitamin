#!/usr/bin/python3

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
                s = self.scripts[script]()
                s._set_folders(WORKDIR, CURRENT)
                s.run()
            else:
                print("Script '{0}' not found ^-(O_O)-^".format(script))            

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
                script = imp.__dict__[m.split(".")[-1]]
                assert issubclass(script, IScript)
                self.scripts[m.split(".")[-1].lower()] = script
            except KeyError:
                print("bad %s file" % m)            

if __name__ == "__main__":
    
    import os
    import sys   

    WORKDIR = os.path.dirname(os.readlink(__file__))
    CURRENT = os.getcwd()
    SCRIPTS = os.path.join(WORKDIR, "scripts")
    
    sys.path.append(WORKDIR)
    sys.path.append(os.path.dirname(WORKDIR))
    
    from iscript import IScript    

    assert WORKDIR
    assert os.path.exists(SCRIPTS)
    
    resolver = ScriptsResolver()
    
    
