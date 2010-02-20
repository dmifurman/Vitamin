from abc import ABCMeta, abstractmethod


class ITemplateLoader(metaclass=ABCMeta):
    
    @abstractmethod
    def load(self, name):
        pass

    @abstractmethod
    def loadText(self, text):
        pass
