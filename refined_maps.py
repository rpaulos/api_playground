from pprint import pprint
import requests
import googlemaps
from sk import myGoogleMapsAPI

API_KEY = myGoogleMapsAPI
map_client = googlemaps.Client(API_KEY)

def print_menu():
    print("\nWhat do you wanna do?")
    print("1 - Search by name")
    print("2 - Search by location")
    print("3 - Distance Matrix")
    print("4 - Weather Data")
    print("5 - Convert name to Latitude and Longitude")

# Seach by text input
def search_by_name():
    query = input("Search Place: ")
    result = map_client.places(query)
    pprint(result)

# Search an establishment type via the latitude and longitude
def search_by_location():
    lat = float(input("Latitude: "))
    lng = float(input("Longitutde: "))
    place_type = input("Establishment type: ")

    result = map_client.places_nearby(
        location = (lat, lng),
        radius = 500, #this can be changed
        type = place_type
    )
    pprint(result)

# Get the distance between two points and the estimated time of arrival via driving
def get_distance_matrix():
    # 14.606967
    # 120.993233
    origin_latitude = input("Origin Latitude: ")
    origin_longitude = (input("Origin Longitude: "))
    origin = f"{origin_latitude},{origin_longitude}"

    # 14.589762
    # 120.983074
    destination_latitude = input("Destination Latitude: ")
    destination_longitude = input("Destination Longitude: ")
    destination = f"{destination_latitude},{destination_longitude}"

    # Call Google Maps Distance Matrix API
    result = map_client.distance_matrix(
        origins = origin,
        destinations = destination,
        mode = "driving",
        # Departure time can be adjusted and will be based on previous data and not live
        departure_time="now"
    )

    distance = (
        result.get('rows', [{}])[0]
            .get('elements', {})[0]
            .get('distance', {})
            .get('text', 'Unknown')
    )

    duration = (
        result.get('rows', [{}])[0]
            .get('elements', {})[0]
            .get('duration', {})
            .get('text', 'Unknown')
    )

    duration_in_traffic = (
    result.get("rows", [{}])[0]
        .get("elements", [{}])[0]
        .get("duration_in_traffic", {})
        .get("text", "Unknown")
    )

    # Prints out the distance, duration, and duration with traffic
    # For the actuali implementation, it should return these values
    print("Distance: ", distance)
    print("Duration: ", duration)
    print("Duration with traffic:", duration_in_traffic)

# Get the weather data for a place using their latitude and longitude
def get_weather_data():
    # This is just for testing the weather API. 
    # In the actual implementation, this function should take `lat` and `lng` as parameters
    lat = float(input("Latitude: "))
    lng = float(input("Longitude: "))

    # Construct the request URL with the API key and coordinates
    URL = (
        "https://weather.googleapis.com/v1/forecast/days:lookup"
        f"?key={API_KEY}&location.latitude={lat}&location.longitude={lng}"
    )

    # Send a GET request to the Weather API
    response = requests.get(URL)

    # If the request was successful, process the data
    if response.status_code == 200:
        data = response.json()

        weather_condition = (
            data.get('forecastDays', [{}])[0]
                .get('daytimeForecast', {})
                .get('weatherCondition', {})
                .get('description', {})
                .get('text', 'Unknown')
        )

        max_heat_index = (
            data.get('forecastDays', [{}])[0]
                #.get('daytimeForecast', {})
                .get('maxHeatIndex', {})
                .get('degrees', 'Unknown')
        )

        sunset_time = (
            data.get('forecastDays', [{}])[0]
                #.get('daytimeForecast', {})
                .get('sunEvents', {})
                .get('sunsetTime', 'Unknown')

        )
        # Prints out the latitue ang longitude
        # For the actuali implementation, it should return these values
        print(f"Weather condition:  " + weather_condition)
        print("Max Heat Index:     " + f"{max_heat_index}")
        print("Sunset Time:        " + f"{sunset_time}")

    else:
        print("Failed to retrieve weather data")
    pprint(data)

def get_geocode():
    # This is just for testing the geocode feature of Google Maps.
    # In actual implementation, the address should be passed as a parameter to this method
    address = input("Address: ")

    # Call the Google Maps Geocoding API and pass in the text address
    result = map_client.geocode(address)

    # result is a list so get the first element which is a dict that contains the latitude and longitude
    location = result[0].get("geometry", {}).get("location", {})
    latitude = location.get("lat", "Unknown")
    longitude = location.get("lng", "Unknown")

    # Prints out the latitue ang longitude
    # For the actuali implementation, it should return latitude and longitude
    print("Latitude:    ", latitude)
    print("Longitude:   ", longitude)


def main():
    # print(dir(map_client))  # Lists available methods
    print_menu()
    
    try:
        choice = int(input("\nEnter your choice: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    if choice == 1:
        search_by_name()
    elif choice == 2:
        search_by_location()
    elif choice == 3:
        get_distance_matrix()
    elif choice == 4:
        get_weather_data()
    elif choice == 5:
        get_geocode()
    else:
        print("Invalid choice. Please select a number from 1 to 5.")

if __name__ == "__main__":
    main()
