# import os
# from configparser import ConfigParser
# print('hello world')
# dir= os.path.abspath(os.path.join(os.path.dirname(__file__),'config_details.ini'))
# print(dir)
# conf= ConfigParser()
# conf.read(dir)
# conf.optionxform= str
# print(conf.items('location_details'))
# # print(conf.get('location_details','state_code'))

first = 0
second = 0

dose_type= 'available_capacity_dose1' if first ==1 and second == 0 else 'available_capacity_dose2' if first==0 and second==1\
 else 'both' if first ==1 and second == 1 else 'ignore'

print(dose_type)