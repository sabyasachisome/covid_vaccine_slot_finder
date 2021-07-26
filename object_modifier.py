from configparser import ConfigParser

class ObjectModifier:
    def __init__(self, *args) -> None:
        self.config_file= args[0]
    
    def get_config(self):
        self.config= ConfigParser()
        self.config.read(self.config_file)
        self.config.optionxform= str