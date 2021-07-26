import os
from configparser import ConfigParser
print('hello world')
dir= os.path.abspath(os.path.join(os.path.dirname(__file__),'config_details.ini'))
print(dir)
conf= ConfigParser()
conf.read(dir)
conf.optionxform= str
print(conf.items('location_details'))
# print(conf.get('location_details','state_code'))