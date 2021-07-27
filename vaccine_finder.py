import requests
from object_modifier import ObjectModifier
import os
import json

class LocationAssigner:
    def __init__(self, *args) -> None:
        self.config_obj= args[0]
        self.dose_type= 'available_capacity_dose1' if self.config_obj.items('dose_type')[0][1]==1 else 'available_capacity_dose2'
        print(self.dose_type)
        self.district_url_param= {}
        for tuple_idx in range(len(self.config_obj.items('location_details'))):
            # setattr(self, config_obj.items('location_details')[tuple_idx][0], config_obj.items('location_details')[tuple_idx][1])
            self.district_url_param[self.config_obj.items('location_details')[tuple_idx][0]]= self.config_obj.items('location_details')[tuple_idx][1]


class VaccineGenerator(LocationAssigner, ObjectModifier):
    def __init__(self, *args) -> None:
        super(VaccineGenerator, self).__init__(*args)
    
    def check_availablity(self):
        resp= requests.get(self.config_obj.get('url_details','request_url'), params=self.district_url_param)
        resp_dict= json.loads(resp.text)
        # print(resp_dict)
        for resp_dict_key, resp_dict_val in resp_dict.items():
            pass
        for idx in range(len(resp_dict_val)):
            # print(resp_dict_val[idx])
            if int(resp_dict_val[idx].get('available_capacity'))>0 and resp_dict_val[idx].get('min_age_limit')< int(self.config_obj.get('age_details','age'))\
            and int(resp_dict_val[idx].get(self.dose_type))>0:
                print(resp_dict_val[idx])
                print(resp_dict_val[idx].get('available_capacity'))



if __name__ == '__main__':
    config_file_abs_path= os.path.abspath(os.path.join(os.path.dirname(__file__),'config_details.ini'))
    obj_modify= ObjectModifier(config_file_abs_path)
    obj_modify.get_config()
    vaccine_generator= VaccineGenerator(obj_modify.config)
    vaccine_generator.check_availablity()
