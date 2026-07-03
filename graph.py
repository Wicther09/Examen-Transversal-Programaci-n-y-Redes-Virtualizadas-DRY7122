import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "5b525dbe-5cda-448b-8d53-0d6874df0cc8"

def geocoding(location, key):
    while location == "":
        location = input("Ingrese la ubicacion nuevamente: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        if "country" in json_data["hits"][0]:
            country = json_data["hits"][0]["country"]
        else:
            country = "" 
        if "state" in json_data["hits"][0]:
            state = json_data["hits"][0]["state"]
        else:
            state = ""
        if len(state) != 0 and len(country) != 0:
            new_loc = name + ", " + state + ", " + country
        elif len(state) != 0:
            new_loc = name + ", " + country
        else:
            new_loc = name
        print("Geocoding API URL para " + new_loc + " (Tipo: " + value + ")\n" + url)
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print("Geocode API status: " + str(json_status) + "\nError: " + json_data["message"])          
    return json_status, lat, lng, new_loc

while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfiles de vehiculo disponibles:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("car, bike, foot")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    profile = ["car", "bike", "foot"]
    vehicle = input("Ingrese un perfil de vehiculo (o 's' para salir): ")
    if vehicle.lower() == "s":
        print("Terminando programa...")
        break
    elif vehicle in profile:
        vehicle = vehicle
    else:
        vehicle = "car"
        print("Perfil no valido. Se usara el perfil car.")
    loc1 = input("Ciudad de Origen (o 's' para salir): ")
    if loc1.lower() == "s":
        print("Terminando programa...")
        break
    orig = geocoding(loc1, key)
    loc2 = input("Ciudad de Destino (o 's' para salir): ")
    if loc2.lower() == "s":
        print("Terminando programa...")
        break
    dest = geocoding(loc2, key)
    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle, "locale": "es"}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        print("Routing API Status: " + str(paths_status) + "\nRouting API URL:\n" + paths_url)
        print("=================================================")
        print("Direcciones de " + orig[3] + " a " + dest[3] + " en " + vehicle)
        print("=================================================")
        if paths_status == 200:
            km = paths_data["paths"][0]["distance"] / 1000
            millas = km / 1.61
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
            min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
            fuel = km * 0.08
            print("Distancia Total: {0:.2f} km / {1:.2f} millas".format(km, millas))
            print("Duracion del viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
            print("Combustible requerido: {0:.2f} litros".format(fuel))
            print("=============================================")
            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                print("{0} ( {1:.2f} km / {2:.2f} millas )".format(path, distance / 1000, distance / 1000 / 1.61))
            print("=============================================")
        else:
            print("Error: " + paths_data["message"])
            print("*************************************************")
