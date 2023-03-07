import requests
import urllib.parse
# HOW TO CHECK IF A POSTAL CODE IS WITHIN 50 MILES OF ANOTHER POSTAL CODE
from geopy.geocoders import Nominatim
from geopy.distance import distance

geolocator = Nominatim(user_agent="my-app")

def jobSearch(keyword, location, length, page):
    # Get the job list from the API
    keyword_encoded = urllib.parse.quote(keyword)
    url = f"https://app.loxo.co/api/career-collective/jobs?per_page=10&page={page}&query={keyword_encoded}"
    headers = {
        "accept": "application/json",
        "authorization": "Basic Y2FyZWVyLWNvbGxlY3RpdmVfYXBpOm5mZTRLQlUzcHFrNHB1YSp4Y3E="
    }
    response = requests.get(url, headers=headers)

    # Create lists to store the data
    title_list = []
    location_list = []
    salary_list = []
    full_time_list = []

    # Get the length of the job list
    jobListLength = len(response.json()['results'])
    total_pages = response.json()['total_pages']
    # Check if the location is within the given length of the user's location
    for i in range(jobListLength):
        job_location = response.json()['results'][i]['city']
        if job_location == 'Nashville-Davidson metropolitan government (balance)':
            job_location = 'Nashville-Davidson'
        input_location = location
        location1 = geolocator.geocode(job_location)
        lat1, lon1 = location1.latitude, location1.longitude
        location2 = geolocator.geocode(input_location)
        lat2, lon2 = location2.latitude, location2.longitude
        distance_in_miles = distance((lat1, lon1), (lat2, lon2)).miles

        if distance_in_miles <= length:
            # What to load on the job posting
            # Title
            # Company
            # Location
            # Salary
            # Job Type
            # Posted
            # Description? (Architecture Design)
            # What to load on the search page
            # Title
            # Location
            # Salary
            # Full Time
            title_list.append(response.json()['results'][i]['title'])
            location_list.append(response.json()['results'][i]['city'])
            salary_list.append(response.json()['results'][i]['salary'])
            # full_time_list.append(response.json()['results'][i]['full_time'])
            # print(response.json()['results'][i]['title'])
            # print(response.json()['results'][i]['city'])
            # print(response.json()['results'][i]['salary'])
        else:
            print(f"The given postal code is NOT within {length} miles of the other postal code.")
    #     if keyword == response.json()['results'][i]['title']:
    #         print(response.json()['results'][i]['title'])
    #         print(response.json()['results'][i]['city'])
    #         print(response.json()['results'][i]['salary'])
    # print(response.json()['results'][0]['salary'])
    return title_list, location_list, salary_list, total_pages
    # # Get the latitude and longitude of the first postal code
    # location1 = geolocator.geocode(location)
    # lat1, lon1 = location1.latitude, location1.longitude

    # # Get the latitude and longitude of the second postal code
    # location2 = geolocator.geocode("92374")
    # lat2, lon2 = location2.latitude, location2.longitude

    # # Calculate the distance between the two postal codes
    # distance_in_miles = distance((lat1, lon1), (lat2, lon2)).miles
    # print(distance_in_miles)
    # # Check if the distance is within 50 miles
    # if distance_in_miles <= 50:
    #     print("The given postal code is within 50 miles of the other postal code.")
    # else:
    #     print("The given postal code is NOT within 50 miles of the other postal code.")

test = jobSearch("Architect", "Raleigh", 100, 11)
print(test)
# MAYBE TRY PREEMPTIVELY GETTING ALL LOCATIONS
# IF WE KNOW ALL LOCATIONS AS A LIST, WE CAN CHECK IF THE LOCATION IS IN THE LIST FIRST
# THEN WE CAN CHECK IF THE LOCATION IS WITHIN X MILES OF THE USER'S LOCATION
# IF IT IS, THEN WE CAN CHECK IF THE JOB TITLE IS IN THE LIST OF JOB TITLES
# MAYBE DOWNLOAD JSON FILE OF ALL LOCATIONS AND ALL JOB TITLES
# JUST RETURN PER PAGE, WHEN PAGE 2 IS CLICKED, RUN AGAIN WITH PAGE NUMBER

