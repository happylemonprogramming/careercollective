import json
import os
import requests
from jobsearch import *

# Web Server Library
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
# Should be an environmental variable
app.config["SECRET_KEY"] = os.environ.get('flasksecret')

# __________________________________________________________________________________________________________________________________________________________

# Route for Twitter Token Generator
@app.route('/', methods=["POST"])
def index():
  #Example JSON
    # JSON Body = {"keyword": "Architect", "location": "Raleigh", "length": "100", "page": "1"}

  # Variable loading for JSON
  json_data = request.get_json()
  keyword = json_data['keyword']
  location = json_data['location']
  length = json_data['length']
  page = json_data['page']
  # Job Search API
  job_search_output = jobSearch(keyword, location, length, page)
  dictionary = {"1": job_search_output[0], '2': job_search_output[1]}
  api_response = json.dumps(dictionary)
  return api_response

# __________________________________________________________________________________________________________________________________________________________

# Run app on server (must be at end of code)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True) # Change host back to 0.0.0.0, if needed or http(s)://127.0.0.1