#! /usr/bin/python3

from extra.server.server import Server
from extra.server.config import messages, config
import sys

if __name__ == "__main__":    
    
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            name, value = arg.split("=")
            if name.startswith("-"): 
                if config.Server.reconfigure(name[1:], value):
                    print("New value {0} accepted!".format(name))
                else:
                    raise Exception("No such value to reconfigure! Name: " + name)
    
    srv = Server()
    
    try:
        messages.log.program_started
        srv.run()
    except KeyboardInterrupt:
        messages.log.stop
        srv.enableRestart(False)  
        srv.kill()
