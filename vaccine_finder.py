import requests
from configparser import ConfigParser
import os
import json
import pandas as pd

lat_long_request_url= 'https://cdn-api.co-vin.in/api/v2/appointment/centers/public/findByLatLong?'

class DetailsAssigner:
    def __init__(self, *args) -> None:
        self.config_obj= args[0]
        self.dose_type= 'available_capacity_dose1' if int(self.config_obj.items('dose_type')[0][1])==1 else 'available_capacity_dose2'
        self.age_details= self.config_obj.items('age_details')[0][1]
        # self.vaccine_name= 'COVISHIELD' if self.config_obj.get('vaccine_name','COVISHIELD')==1 else 'COVAXIN' if self.config_obj.get('vaccine_name','COVAXIN')==1 else 'both'
        print('checking for age {} and dose number {}'.format(self.age_details,self.dose_type))

class ObjectModifier:
    def __init__(self, *args) -> None:
        self.config_file= args[0]
    
    def get_config(self):
        self.config= ConfigParser()
        self.config.read(self.config_file)
        self.config.optionxform= str

class VaccineGenerator(DetailsAssigner, ObjectModifier):
    def __init__(self, *args) -> None:
        super(VaccineGenerator, self).__init__(*args)
    
    def get_latitude_longitude(self):
        lat_long_request_param= {}
        my_ip_resp= requests.get('https://get.geojs.io/v1/ip.json').json()['ip']
        lat_long_url= 'https://get.geojs.io/v1/ip/geo/'+my_ip_resp+'.json'
        address_response= requests.get(lat_long_url).json()
        lat_long_request_param['lat']=address_response['latitude']
        lat_long_request_param['long']=address_response['longitude']
        return lat_long_request_param

    def get_nearby_centres(self):
        self.centre_ids= set()
        lat_long_request_param= self.get_latitude_longitude()
        resp= requests.get('https://cdn-api.co-vin.in/api/v2/appointment/centers/public/findByLatLong?', params= lat_long_request_param)
        centre_dict= json.loads(resp.text)
        for dict_elem in centre_dict['centers']:
            self.centre_ids.add(dict_elem['center_id'])

    def parse_json(self, vaccine_available_centre_detailed_list):
        dose_type= self.dose_type
        age= int(self.age_details)
        vaccine_available_dict={}

        for centre_idx in range(len(vaccine_available_centre_detailed_list)):
            centre_id= vaccine_available_centre_detailed_list[centre_idx]['center_id']
        #     print(vaccine_available_centre_detailed_list[centre_idx])
            centre_details= [vaccine_available_centre_detailed_list[centre_idx]['name'],vaccine_available_centre_detailed_list[centre_idx]['address'],vaccine_available_centre_detailed_list[centre_idx]['block_name'],vaccine_available_centre_detailed_list[centre_idx]['pincode']]
            for session_idx in range(len(vaccine_available_centre_detailed_list[centre_idx]['sessions'])):
                if vaccine_available_centre_detailed_list[centre_idx]['sessions'][session_idx][dose_type]>0 and vaccine_available_centre_detailed_list[centre_idx]['sessions'][session_idx]['min_age_limit']<age:
                    slot_details_value= [vaccine_available_centre_detailed_list[centre_idx]['sessions'][session_idx]['date'],vaccine_available_centre_detailed_list[centre_idx]['sessions'][session_idx]['vaccine'],dose_type, vaccine_available_centre_detailed_list[centre_idx]['sessions'][session_idx][dose_type],vaccine_available_centre_detailed_list[centre_idx]['sessions'][session_idx]['min_age_limit'],vaccine_available_centre_detailed_list[centre_idx]['sessions'][session_idx]['slots']]
                    slot_val=[]
                    slot_val.extend(centre_details)
                    slot_val.extend(slot_details_value)
                    if centre_id not in vaccine_available_dict:
                        vaccine_available_dict[centre_id]= list()
                    vaccine_available_dict[centre_id].append(slot_val)
        return vaccine_available_dict

    def check_availability(self):
        availability_details_dict= {}
        centre_id_api_params= {}
        vaccine_available_centre_detailed_list= []
        test_list=[]
        cur_date= pd.to_datetime('now').strftime('%d-%m-%Y')
        for centre_id in self.centre_ids:
            centre_id_api_params['center_id']= centre_id
            centre_id_api_params['date']= cur_date
            response= requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByCenter?', params= centre_id_api_params)
            availability_details_dict= json.loads(response.text)
            if len(availability_details_dict)>0:
                vaccine_available_centre_detailed_list.append(availability_details_dict['centers'])
                test_list.append(availability_details_dict)
        vaccine_available_dict= self.parse_json(vaccine_available_centre_detailed_list)
        print(vaccine_available_dict)
        if len(vaccine_available_dict)>=1:
            os.system("afplay " + 'vaccine_alert.WAV')

if __name__ == '__main__':
    config_file_abs_path= os.path.abspath(os.path.join(os.path.dirname(__file__),'config_details.ini'))
    obj_modify= ObjectModifier(config_file_abs_path)
    obj_modify.get_config()
    vaccine_generator= VaccineGenerator(obj_modify.config)
    vaccine_generator.get_nearby_centres()
    vaccine_generator.check_availability()
