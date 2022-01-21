import requests
import json

BASE = "http://127.0.0.1:5000/"

file = open("example.json")
file2 = open("empty_example.json")

data = json.load(file)
data2 = json.load(file2)

# FRAMES
# API call test and examples
# GET method
# response = requests.get(BASE + "latestframe/1")
#input()
# POST method
# response = requests.post(BASE + "latestframe", json = data)
# List all the elements in the list
response = requests.get(BASE + "listframes/3", data)
# print(response.json())
#input()
#response = requests.get(BASE + "latestframe")
# LIST method
# response = requests.get
#print (response.json())
# response = requests.get(BASE + "latestframe", data)
print(response.json())