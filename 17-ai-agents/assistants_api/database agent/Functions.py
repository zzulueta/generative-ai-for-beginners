tools_function = [
    {   "type": "file_search"},
    {
        "type": "function",
        "function": {
            "name": "get_weather_for_city",
            "description": "Retrieves the current weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city (e.g., 'Phoenix', 'Sacramento')."
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_restaurants_for_city",
            "description": "Retrieves the restaurants for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city (e.g., 'Phoenix', 'Sacramento')."
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_hotels_for_city",
            "description": "Retrieves the hotels for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city (e.g., 'Phoenix', 'Sacramento')."
                    }
                },
                "required": ["city"]
            }
        }
    },

]



# define functions
import http.client
def get_weather_for_city(city):
    conn = http.client.HTTPSConnection("weatherapi-com.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "e703448e68msh3f503e9fed5f7c4p19c154jsnb72125bf2887",
        'x-rapidapi-host': "weatherapi-com.p.rapidapi.com"
    }
    #remove spaces in city
    city = city.replace(" ", "%20")
    url = f"/current.json?q={city}"
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")


import http.client
import re
import json
def get_restaurants_for_city(city):
    conn = http.client.HTTPSConnection("tripadvisor16.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "570c937e9emsh9290d2f6a449024p1c526fjsna02711a72ec5",
        'x-rapidapi-host': "tripadvisor16.p.rapidapi.com"
    }
    city = city.replace(" ", "%20")
    url = f"/api/v1/restaurant/searchLocation?query={city}"
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    json_data = res.read()
    json_data = json.loads(json_data)
    element = json_data["data"][0]
    geo_id = re.search(r'g(\d+)',element["documentId"]).group(1)

    conn = http.client.HTTPSConnection("tripadvisor16.p.rapidapi.com")
    url = f"/api/v1/restaurant/searchRestaurants?locationId={geo_id}"
    conn.request("GET", url, headers=headers)

    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")

import http.client
def get_hotels_for_city(city):
    conn = http.client.HTTPSConnection("booking-com18.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "e703448e68msh3f503e9fed5f7c4p19c154jsnb72125bf2887",
        'x-rapidapi-host': "booking-com18.p.rapidapi.com"
    }
    city = city.replace(" ", "%20")
    url = f"/stays/auto-complete?query={city}"
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")
