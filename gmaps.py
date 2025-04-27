from pprint import pprint
from sk import myGoogleMapsAPI
import googlemaps
import requests

API_KEY = myGoogleMapsAPI

map_client = googlemaps.Client(API_KEY)

#prints out the api services we can use :D
print(dir(map_client))

choice = int(input("What do you wanna do? (1 - Search by name |2 - Search by Location |3 - Distance Matrix |4 - Weather Data)"))

if (choice == 1):
    #Nearby search by text input
    search_places_near = input("Search Places Near: ")
    nearby_search = map_client.places(search_places_near)
    pprint(nearby_search)

elif (choice == 2):
    #Nearby search by location
    lat = float(input("Latitude: "))
    lng = float(input("Longitude: "))
    type = input("Establishment type: ")
    nearby_search_location = map_client.places_nearby(
        location = (lat, lng), 
        #radius
        radius=500, 
        type = type
    )
    pprint(nearby_search_location)

elif (choice ==3):
    #distance matrix to return the time it takes to go there
    #and the distance in meters
    #activate distance matrix in the gmaps API
    origin = input("Origin: ")
    destination = input("Destination: ")
    mode = input("Mode of transportation (1 - Driving | 2 - Biking | 3 - Transit | 4 - Walking | 5 - Public Transpo): ")

    if (mode == "1"):
        mode = "driving"
    elif (mode == "2"):
        mode = "biking"
    elif (mode == "3"):
        mode = "transit"
    elif (mode == "4"):
        mode = "walking"
    elif (mode == "5"):
        mode = int(input("Transit (1 - Bus | 2 - Subway | 3 - Train | 4 - Tram | 5 - Rail)"))

    matrix = map_client.distance_matrix(
        origin, 
        destination, 
        mode
    )
    pprint(matrix)

elif (choice == 4):
    lat = float(input("Latitude: "))
    lng = float(input("Longitude: "))

    url = (
        "https://weather.googleapis.com/v1/forecast/days:lookup"
        f"?key={API_KEY}&location.latitude={lat}&location.longitude={lng}"
    )

    response = requests.get(url)
    data = response.json()
    pprint(data)


#https://maps.googleapis.com/maps/api/geocode/json?address=1+Market+St,+San+Francisco,+CA&key={myAPIKey}