

class SiteInfo():

    __name = ""
    __description = "" 
    __version = ""
    __authors = ""
    __vitamin_version = ""

    @property
    def name(self):
        return self.__name
    
    @property
    def description(self):
        return self.__description
    
    @property
    def version(self):
        return self.__version
    
    @property
    def authors(self):
        return self.__authors
    
    @property
    def vitamin(self):
        return self.__vitamin_version
    
