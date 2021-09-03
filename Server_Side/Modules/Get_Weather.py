from Data_Handler import write_data, read_data
from os.path import dirname, realpath
import requests, json

def get_metofffice_data(resource, file_name_to_save, resolution='res=daily&'):
    api_key = open('/home/w-s/Documents/ApiKey/weather_api.txt', 'r').readlines()[0].rstrip()
    url = f'http://datapoint.metoffice.gov.uk/public/data/{resource}?{resolution}key={api_key}'
    path_to_save_file = dirname(realpath(__file__))+'/../Data/'+file_name_to_save+'.json'
    write_data(json.loads(requests.get(url).text), path_to_save_file)

def get_weather_keys():
    weather_data = read_data('today\'s_weather.json')
    weather_data_keys = weather_data['Wx']['Param']
    

get_metofffice_data('val/wxfcs/all/json/sitelist', 'weather_site_list')
get_metofffice_data('val/wxfcs/all/json/310004', 'today\'s_weather')