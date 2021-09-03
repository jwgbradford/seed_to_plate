from Modules.Data_Handler import write_data, read_data
from os.path import dirname, realpath, join
from random import uniform
import requests, json

def get_metofffice_data(resource, file_name_to_save, resolution='res=daily&'):
    api_key = open('/home/w-s/Documents/ApiKey/weather_api.txt', 'r').readlines()[0].rstrip()
    url = f'http://datapoint.metoffice.gov.uk/public/data/{resource}?{resolution}key={api_key}'
    path_to_save_file = join(dirname(realpath( __file__ )), '..', 'Data', f'{file_name_to_save}.json')
    write_data(json.loads(requests.get(url).text), path_to_save_file)

def get_rainfall_today(weather_today):
    rain_percentage =  int(weather_today[0]["PPd"]) + int(weather_today[1]["PPn"])
    rain_type_day, rain_type_night = int(weather_today[0]["W"]), int(weather_today[1]["W"])
    if (15 > rain_type_day > 9) and (15 > rain_type_night > 9):
            rain_type = (rain_type_day + rain_type_night) / 2
    elif (15 > rain_type_day > 9):
        rain_type = rain_type_day
    elif (15 > rain_type_night > 9):
        rain_type = rain_type_night
    else: return 0
    return (rain_type - 9) * 0.041 * rain_percentage

def get_weather_type(weather_today):
    weather_type = weather_today[0]["W"]
    if (weather_type == 24) or (weather_type == 26) or (weather_type == 27):
        return 'Snow'
    return 'normal'

def get_weather_today():
    weather_data = read_data(join(dirname(realpath( __file__ )), '..', 'Data', 'weather_today.json'))
    weather_today = weather_data["SiteRep"]["DV"]["Location"]["Period"][0]["Rep"]
    return {
        "type": get_weather_type(weather_today),
        "temp": int(weather_today[0]["Dm"]) + int(weather_today[1]["Nm"]) / 2,
        "sun": int(weather_today[0]["U"]) + uniform(5, 6),
        "rainfall": get_rainfall_today(weather_today)
    }

if __name__ == "__main__":
    #get_metofffice_data('val/wxfcs/all/json/sitelist', 'weather_site_list')
    get_metofffice_data('val/wxfcs/all/json/310004', 'weather_today')
    print(get_weather_today())

