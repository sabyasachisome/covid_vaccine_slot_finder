import requests
from object_modifier import ObjectModifier
import os

class LocationAssigner:
    def __init__(self, *args) -> None:
        config_obj= args[0]
        self.district_url_param= {}
        # print(config_obj.items('location_details'))
        for tuple_idx in range(len(config_obj.items('location_details'))):
            # setattr(self, config_obj.items('location_details')[tuple_idx][0], config_obj.items('location_details')[tuple_idx][1])
            self.district_url_param[config_obj.items('location_details')[tuple_idx][0]]= config_obj.items('location_details')[tuple_idx][1]
        # print(self.state_code, self.district_code)
        print(self.district_url_param)


class VaccineGenerator(LocationAssigner, ObjectModifier):
    def __init__(self, *args) -> None:
        super(VaccineGenerator, self).__init__(*args)
    
    def check_availablity(self):
        print(self.request_url)
        requests.get(self.request_url)

if __name__ == '__main__':
    config_file_abs_path= os.path.abspath(os.path.join(os.path.dirname(__file__),'config_details.ini'))
    # print(config_file_abs_path)
    obj_modify= ObjectModifier(config_file_abs_path)
    obj_modify.get_config()
    vaccine_generator= VaccineGenerator(obj_modify.config)
    # vaccine_generator.check_availablity()
