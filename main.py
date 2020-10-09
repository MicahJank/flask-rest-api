from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort

# creates the flask app
app = Flask(__name__)
# initializes the flask app as an API
api = Api(app)

# the request parser object will parse the request and make sure it fits the guidelines
# basically it will validate what is being sent through the request to make sure its right
video_put_args = reqparse.RequestParser()

# name is basically the key of the argument, type is the type of value the key will have and
# help is what you give so that when the user doesnt send the right information it will give them a help message
# to know what they are missing 
# when required is set to true it will throw an error if the request does not have the right args attached
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video is required", required=True)
video_put_args.add_argument("likes", type=int, help="likes on the video is required", required=True)
videos = {}

# this function will handle what happense whenver some data the request is trying to access doenst exist
# abort comes from the flask_restful library, it sends back an error message that we can define in the parameter
# the status code signals what type of error we should send back
def handle_request_error(video_id):
    if video_id not in videos:
        abort(404, message=f"Couldn't find video with id {video_id}")

# Video is inheriting from Resource
# this creates the structure of the resource
class Video(Resource):
    # we override the get function to return our own resource
    def get(self, video_id):
        handle_request_error(video_id)
        return videos[video_id]
    
    def put(self, video_id):
        # this will parse the request for the args and if they arent in there it will automatically send back an error
        args = video_put_args.parse_args()
        videos[video_id] = args
        # status codes can be returned with the request, in this case 201 is returned since it stands for created
        return videos[video_id], 201


# this actually adds the resource to the api
api.add_resource(Video, "/video/<int:video_id>")

# the app should run if the name of the file running is 'main'
# i also set debug to true to give us information logging in the console
# should only be set to true when running in development environment 
if __name__ == "__main__":
    app.run(debug=True)