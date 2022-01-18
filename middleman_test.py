import requests
import json

BASE = "http://127.0.0.1:5000/"

file = open("example.json")

data = json.load(file)

# FRAMES
# API call test and examples
# GET method
# response = requests.get(BASE + "latestframe")
#input()
# POST method
response = requests.post(BASE + "latestframe", json = data)
# List all the elements in the list
response = requests.get(BASE + "listframes")
print(response.json())
#input()
#response = requests.get(BASE + "latestframe")
# LIST method
#response = requests.get
#print (response.json())