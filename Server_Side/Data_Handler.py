from os import name
from os.path import dirname, realpath, join
from random import uniform
from datetime import datetime
import requests, json

def write_data(dict_to_save, file_name):
    with open(file_name, 'w') as file:
        json.dump(dict_to_save, file, indent=4)
    file.close

def read_data(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    file.closed
    return data

def get_metofffice_data(location_id, saved_weather):
    api_key = open('/home/digiadmin/Documents/DigiLocal_code/met_api.txt', 'r').readlines()[0].rstrip()
    url = f'http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/{location_id}?res=daily&key={api_key}'
    #path_to_save_file = join(dirname(realpath( __file__ )), '..', 'Data', 'weather_data.json')
    new_weather_data = json.loads(requests.get(url).text)
    weather_date = new_weather_data["SiteRep"]["DV"]["dataDate"][:10]
    lat = new_weather_data["SiteRep"]["DV"]["Location"]["lat"]
    lon = new_weather_data["SiteRep"]["DV"]["Location"]["lon"]
    name = new_weather_data["SiteRep"]["DV"]["Location"]["name"]
    weather_today = new_weather_data["SiteRep"]["DV"]["Location"]["Period"][0]["Rep"]
    saved_weather[location_id] = {
        "weather_date" : weather_date,
        "lat" : lat,
        "lon" : lon,
        "name" : name,
        "weather_today" : weather_today
    }
    write_data(saved_weather, 'weather_today.json')
    return saved_weather

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

def get_weather_today(location_id):
    today = datetime.today().strftime('%Y-%m-%d')
    #weather_data = read_data(join(dirname(realpath( __file__ )), '..', 'Data', 'weather_today.json'))
    weather_data = read_data('weather_today.json')
    if location_id not in weather_data.keys() or today > weather_data[location_id]["weather_date"]:
        weather_data = get_metofffice_data(location_id, weather_data)
    weather_today = weather_data[location_id]["weather_today"]
    return {
        "type": get_weather_type(weather_today),
        "temp": int(weather_today[0]["Dm"]) + int(weather_today[1]["Nm"]) / 2,
        "sun": int(weather_today[0]["U"]) + uniform(5, 6),
        "rainfall": get_rainfall_today(weather_today)
    }

if __name__ == "__main__":
    #get_metofffice_data('val/wxfcs/all/json/sitelist', 'weather_site_list')
    #get_metofffice_data('val/wxfcs/all/json/310004')
    print(get_weather_today("310004"))

