from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

latest_frame = []

# Frame class to obtain the frames from spot-it-3d.
class Frame(Resource):
    # method to get the frame of a given frame id
    def get(self, frame_id):
        # checks if the frame exists
        check_frame_exist(frame_id)
        # compares the frame id with the latest saved frame
        compare_latest_frame(frame_id)
        return frames[frame_id]

    # method to post frame to the backend
    def post(self, frame_id):
        check_existing_frame(frame_id)
        args = frames_put_args.parse_args()
        frames[frame_id] = args
        return frames[frame_id], 201

def check_frame_exist(frame_id):
    # returns an error if the queried frame does not exist.
    if frame_id not in frames:
        abort(404, message = "Frame not found...")

def check_existing_frame(frame_id):
    # returns an error if the frame added already exist.
    if frame_id in frames:
        abort(409, message = "Frame already exist...")

def compare_latest_frame(frame_id):
    if frame_id > latest_frame_number:
        retrurn True

def reset_run():
    latest_frame_number = 0
    return {"Frame number sucessfully resetted"}

# JSON parsesr for frames
frames_put_args = reqparse.RequestParser()
frames_put_args.add_argument("num_cameras", type=int, help="Number of cameras in one frame", required=True)
frames_put_args.add_argument("num_targets", type=int, help="Number of targets in one frame", required=True)

class ResetFrame(Resource):
    def get(self):
        reset_run()

class LatestFrame(Resource):
    def get(self):
        #get the latest frame id
        frame_id = get_latest_frame()
        return frame_id

def get_latest_frame():
    # returns the index of the latest key
    return len(frames) - 1

api.add_resource(ResetFrame, "/object/object_id")
api.add_resource(Frame, "/frame/<int:frame_id>")
api.add_resource(LatestFrame, "/frame/latest_frame")

if __name__ == "__main__":
    app.run(debug = True)