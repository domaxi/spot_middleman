import requests

BASE = "http://127.0.0.1:5000/"

data = {
    "frame" : [
        { 
            "id" : 0
            "cameras" : [
                "Camera_1", "Camera_2"
            ]
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
    ]
}

response = requests.get(BASE + "frame/latest_frame")
print (response.json())
input()
response = requests.get(BASE + "frame/0")
print (response.json())