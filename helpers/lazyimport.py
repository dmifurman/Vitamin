import sys
   
def smartimport(path, environment=[]):
    if environment:
        sys.path.extend(environment)
    
    pval = None
    try:
        pmodule, pval = path.split("::")
    except ValueError:
        pmodule = path
        
    imodule = __import__(pmodule, globals={}, locals={}, fromlist=[""])
    if pval:
        return getattr(imodule, pval)
    else: return imodule
