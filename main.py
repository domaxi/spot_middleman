from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort
import json

app = Flask(__name__)
api = Api(app)

# constants
FRAME_BUFFER_SIZE = 5

# variable that contains the frames. 
# the lastest frame will be appended in the first element.
# older frames will be shifted to the higher index.
frames = [
    { 
        "id" : 0,
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
    },
    { 
        "id" : 2,
        "cameras" : [
            "Camera_1", "Camera_2"
        ],
        "objects" : [
            {
                "Object_1" :
                    {
                        "X" : 30, 
                        "Y" : 40, 
                        "Z" : 50
                    }
            },
            {
                "Object_2" :
                    {
                        "X" : 200, 
                        "Y" : 300, 
                        "Z" : 400
                    }
            } 
        ]
    }
]

image = [
]

# Frame class to obtain the frames from spot-it-3d.
class LatestFrame(Resource):
    # method to get the frame of a given frame id
    def get(self):
        # checks if the frame exists.
        check_frame_buffer()
        # returns the first element in the frame.
        packet = get_latest_frame()
        return packet, 200

    # method to post frame to the backend
    def post(self):
        check_existing_frame()
        args = frames_put_args.parse_args()
        shift_frame_index(get_list_size())
        frames[0] = args
        print(get_list_size())
        return "Latest frame sucessfully added",201

    def list(self):
        # returns a python list that contains all the frames.
        return frames

#checks if there are already frames in the buffer
def check_frame_buffer():
    if (len(frames) == 0):
        return abort(404, message = "Frame not found...")

# returns the first element of the buffter
def get_latest_frame():
    return frames[1]

# returns the current list size
def get_list_size():
    return len(frames)

# shifts the elements of the list by one index
def shift_frame_index(list_size):
    # appends the list until the maxiumum frame size.
    if (list_size < FRAME_BUFFER_SIZE):
        frames.append(frames[list_size - 1])
    # shifts the frames by one index place.
    for i in reversed(range(0,list_size)):
        frames[i+1] = frames[i]

# returns an error if the frame added already exist.
def check_existing_frame():
    #if frame_id in frames:
    #    abort(409, message = "Frame already exist...")
    return

# JSON parsesr for frames
frames_put_args = reqparse.RequestParser()
frames_put_args.add_argument("id", type=int, help="Frame ID number", required=True)
frames_put_args.add_argument("cameras", type=str, action = 'append', help="Number of cameras in one frame", required=True)
frames_put_args.add_argument("objects", type=str, action = 'append', help="Number of objects in one frame", required=True)

# Converter class to handle conversion from relative to absolute position
class Converter(Resource):
    def post():
        # posts the latitude and longitude of the camera position
        camera_location = lat_long_args.parse_args()
        data = convert_relative_to_absolute(camera_location)
        return data


# performs calcualtion on the lat long and the base psoe from spot it.
# returns the list of the lat and long.
def convert_relative_to_absolute(camera_location):
    
    relative_position = get_latest_position()
    camera_lat = camera_location["latitude"]
    camera_long = camera_location["logitude"]

    # calcualtes the absolute lat long
    absolute_lat = camera_lat + relative_position["X"]
    absolute_long = camera_long + relative_position["Y"]

    # combines the absolute lat and absolute_long into json file
    absolute_pose = [absolute_lat,absolute_long]
    absolute_pose_json = json.dumps(absolute_pose)

    return absolute_pose_json

def get_latest_position():
    return

#JSON parser for lat long
lat_long_args = reqparse.RequestParser()
lat_long_args.add_argument("latitude", type=float, help =  "Please provide the latitude", required = True)
lat_long_args.add_argument("longitude", type=float, help =  "Please provide the longitude", required = True)

class ListFrames(Resource):
    def get(self):
        frames_json = json.dumps(frames)
        return frames_json, 200

# api.add_resource(Frame, "/frame")
api.add_resource(LatestFrame, "/latestframe")
api.add_resource(Converter, "/convert")
api.add_resource(ListFrames, "/listframes")

if __name__ == "__main__":
    app.run(debug = True)