from iscript import IScript
import os
from vitamin.siteinfo import create_info, write_to

class init(IScript):

    def run(self):
        self.create_simple_site()   
    
    simple_site = [
        "models",
        "templates",
        "views",
        "stuff/scripts",
        "stuff/styles",
        "stuff/files"]
    
    def create_simple_site(self):
        
        """
        Создает файловую структуру и все необходимые файлы
        для создания простого vitamin- сайта.
        """
        
        list(map(os.makedirs, self.simple_site)) 
        name = input("Enter site name:")
        description = input("Enter site description:")
        version = input("Enter site version:")
        authors = input("Enter site authors:")
        vitamin_version = input("Enter site vitamin version:")
        text = create_info(name, description, version, authors, vitamin_version)
        write_to(text, self.currentdir)
