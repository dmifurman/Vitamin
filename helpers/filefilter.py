import os

def _filterPath(path, listFilter, listExt):
    _path, _ext = os.path.splitext(path)
    _goodExt = False
    _goodPath = False
    
    if not listExt and not listFilter: return True   
    if not listFilter: _goodPath = True
    else:
        for pattern in listFilter:
            if pattern in _path: 
                _gootPath = True
                break
    if not listExt: _goodExt = True
    else:
        for ext in listExt:
            if _ext == ext:
                _goodExt = True
                break
    return _goodPath and _goodExt

def _findFiles(path, listExt=[], listFilter=[]):    
    lFiles = []
    for root, dirs, files in os.walk('.'):
        lFiles += [os.path.join(root, name) for name in files
                    if _filterPath(name, listFilter, listExt)]
    return lFiles

def find(path, strExt="", strFilter=""):
    listExt = strExt.split()
    listFilter = strFilter.split()
    if os.path.exists(path):
        return _findFiles(path, listExt, listFilter)
    else:
        raise Exception()


