import requests
import urllib.parse
from geopy.geocoders import Nominatim
from geopy.distance import distance
import time

geolocator = Nominatim(user_agent="my-app")

def jobSearch(keyword, user_location, length, page):
    start_time = time.time()
    if user_location.isdigit():
        lucene_syntax = f"zip:({user_location}) AND title:({keyword})"
    else:
        lucene_syntax = f"city:({user_location}) AND title:({keyword})"
    
    # Get the job list from the API
    keyword_encoded = urllib.parse.quote(lucene_syntax)
    url = f"https://app.loxo.co/api/career-collective/jobs?per_page=25&page={page}&query={keyword_encoded}"
    headers = {
        "accept": "application/json",
        "authorization": "Basic Y2FyZWVyLWNvbGxlY3RpdmVfYXBpOm5mZTRLQlUzcHFrNHB1YSp4Y3E="
    }
    response = requests.get(url, headers=headers)

    # Create lists to store the data
    title_list = []
    location_list = []
    salary_list = []

    # Get the length of the job list
    jobListLength = len(response.json()['results'])
    total_pages = response.json()['total_pages']
    # Check if the location is within the given length of the user's location
    for i in range(jobListLength):
        # job_location = response.json()['results'][i]['city']
        # if job_location == 'Nashville-Davidson metropolitan government (balance)':
        #     job_location = 'Nashville-Davidson'

        # # Measure the distance between the job location and the user's location
        # location1 = geolocator.geocode(job_location)
        # lat1, lon1 = location1.latitude, location1.longitude
        # location2 = geolocator.geocode(user_location)
        # lat2, lon2 = location2.latitude, location2.longitude
        # distance_in_miles = distance((lat1, lon1), (lat2, lon2)).miles

        # if distance_in_miles <= float(length):
        if True:
            # What to load on the job posting (Title, Company, Location, Salary, Job Type, Posted, Description?)
            # What to load on the search page (Title, Location, Salary, Full Time)
            title_list.append(response.json()['results'][i]['title'])
            location_list.append(response.json()['results'][i]['city'])
            salary_list.append(response.json()['results'][i]['salary'])
        else:
            pass

        if len(title_list) == 10:
            break

    print("Task took %s seconds" % (time.time() - start_time))
    return title_list, location_list, salary_list, total_pages

# MAYBE TRY PREEMPTIVELY GETTING ALL LOCATIONS
# IF WE KNOW ALL LOCATIONS AS A LIST, WE CAN CHECK IF THE LOCATION IS IN THE LIST FIRST
# THEN WE CAN CHECK IF THE LOCATION IS WITHIN X MILES OF THE USER'S LOCATION
# IF IT IS, THEN WE CAN CHECK IF THE JOB TITLE IS IN THE LIST OF JOB TITLES
# MAYBE DOWNLOAD JSON FILE OF ALL LOCATIONS AND ALL JOB TITLES
# JUST RETURN PER PAGE, WHEN PAGE 2 IS CLICKED, RUN AGAIN WITH PAGE NUMBER