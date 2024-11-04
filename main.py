# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    response = requests.get(
        "https://api.openweathermap.org/data/3.0/onecall?lat=10.79&lon=78.70&appid=994a740f9903a45e4059aecd6b26f111")
    response_obj = response.json()
    data = {
        'lat': response_obj['lat'],
        'lon': response_obj['lon'],
        'City': 'Trichy',
        'Temp': response_obj['current']['temp'],
        'Pressure': response_obj['current']['pressure'],
        'Visibility': response_obj['current']['visibility']
    }
    print(data)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
