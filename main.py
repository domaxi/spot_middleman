from sqlite3 import Timestamp
from time import time
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
        append_frames(args)
        return "Latest frame sucessfully added", 201

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
    # initialize the list if the list is empty.
    if(list_size == 0):
        return
    else:
        # appends the list until the maxiumum frame size.
        if (list_size < FRAME_BUFFER_SIZE):
            frames.append(frames[list_size - 1])
        # shifts the frames by one index place.
        for i in reversed(range(0,list_size)):
            frames[i+1] = frames[i]

def append_frames(args):
    if(get_list_size() == 0):
        print("Adding the first element to the list")
        frames.append(args)
    else:
        frames[0] =  args

# returns an error if the frame added already exist.
def check_existing_frame():
    #if frame_id in frames:
    #    abort(409, message = "Frame already exist...")
    return

# JSON parsesr for frames
frames_put_args = reqparse.RequestParser()
frames_put_args.add_argument("Detections", type=str, action= 'append', help="Please provide camera geolocation", required=True)
# frames_put_args.add_argument("ID", type=int, action = 'append', help="Please provide frame ID", required=True)
# frames_put_args.add_argument("Timestamp", type=Timestamp, action = 'append', help="Please provide the object data", required=True)
# frames_put_args.add_argument("XYZ-Coordinates", type=float, action = 'append', help="Please provide the object data", required=True)

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