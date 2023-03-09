# Python standard library imports
import requests
import urllib.parse
import time
import csv
import os

# Third party imports
from geopy.geocoders import Nominatim
from rtree import index
from geopy.distance import great_circle
# from geopy.distance import distance

# NOTE:
# Zip code data source:
# https://simplemaps.com/data/us-zips

# "macro_address" field allows search for state code in addition to direct city

# Example url from comparative website:
# https://jobs.insightglobal.com/find_a_job/
# california/los-angeles/?
# ff=Location,LessThanOrEq,33.99,-118.39,100& # lat, long, radius
# zip=Los%20Angeles,%20CA%2090230&
# rd=100& # radius
# miles=False& 
# remote=False&
# srch=engineer

# Initialize geolocator
geolocator = Nominatim(user_agent="my-app")

# Initialize Loxo API
loxoapikey = os.environ["loxoapikey"]

# Function to search for jobs
def jobSearch(keyword, user_location, radius, page):
    start_time = time.time()

    # create the R-tree index
    idx = index.Index()

    # open the CSV file containing zip codes and their coordinates
    with open('uszips.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header row
        zip_codes = []
        for row in reader:
            zip_code = row[0]
            latitude = float(row[1])
            longitude = float(row[2])
            zip_codes.append((zip_code, (latitude, longitude)))

    # populate the R-tree index with the zip codes and their coordinates
    for i, (zip_code, (lat, lon)) in enumerate(zip_codes):
        idx.insert(i, (lon, lat, lon, lat))

    # determine the latitude and longitude of the user input using an API or database
    location = geolocator.geocode(user_location)
    lat, lon = location.latitude, location.longitude
    user_coords = (lat, lon) # example value: (40.7128, -74.0060)

    # search the R-tree index for zip codes within 100 miles of the user input
    nearby_zip_codes = []
    for item in idx.intersection((user_coords[1]-1, user_coords[0]-1, user_coords[1]+1, user_coords[0]+1), objects=True):
        i = item.id
        zip_code, (lat, lon) = zip_codes[i]
        if great_circle(user_coords, (lat, lon)).miles <= int(radius):
            nearby_zip_codes.append(zip_code)

    # join values with OR operator and enclose in parentheses
    lucene_zip = "(" + " OR ".join(nearby_zip_codes) + ")" # example value: zip_code:[08089 TO 12775] OR zip_code:[18940 TO 19154]
    lucene_syntax = f"zip: {lucene_zip} AND title: {keyword}"

    # Get the job list from the API
    search_encoded = urllib.parse.quote(lucene_syntax)
    url = f"https://app.loxo.co/api/career-collective/jobs?per_page=10&page={page}&query={search_encoded}"
    headers = {
        "accept": "application/json",
        "authorization": loxoapikey
        # "authorization": "Basic Y2FyZWVyLWNvbGxlY3RpdmVfYXBpOm5mZTRLQlUzcHFrNHB1YSp4Y3E="
    }
    response = requests.get(url, headers=headers)

    # Create lists to store the data
    title_list = []
    location_list = []
    salary_list = []

    # Get the length of the job list
    jobListLength = len(response.json()['results'])
    total_pages = response.json()['total_pages']
    total_jobs = response.json()['total_count']

    # Check if the location is within the given length of the user's location
    for i in range(jobListLength):
        # What to load on the job posting (Title, Company, Location, Salary, Job Type, Posted, Description?)
        # What to load on the search page (Title, Location, Salary, Full Time)
        title_list.append(response.json()['results'][i]['title'])
        location_list.append(response.json()['results'][i]['city'])
        salary_list.append(response.json()['results'][i]['salary'])

        if len(title_list) == 10:
            break

    print("Task took %s seconds" % (time.time() - start_time))
    return title_list, location_list, salary_list, total_pages, total_jobs