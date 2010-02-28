from abc import ABCMeta, abstractmethod
from optparse import OptionParser

class IScript(metaclass=ABCMeta):
    
    options = OptionParser()
    
    workdir = ""
    currentdir = ""
    
    def _set_folders(self, workdir, currentdir):
        
        """Устанавливает значения для служебный путей
        workdir и currentdir. В workdir содержится путь
        да папки manage, а в currentdir - текущий рабочий
        каталог"""
        
        self.workdir = workdir
        self.currentdir = currentdir
    
    @abstractmethod    
    def run(self): pass
    
