import requests

BASE = "http://127.0.0.1:5000/"

data = { 
    "id" : 1,
    "cameras" : [
        "Camera_1", "Camera_2"
    ],
    "objects" : [
        {
            "Object_1" :
                {
                    "X" : 20, 
                    "Y" : 30, 
                    "Z" : 40
                }
        },
        {
            "Object_2" :
                {
                    "X" : 20, 
                    "Y" : 30, 
                    "Z" : 40
                }
        } 
    ]
    
}
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