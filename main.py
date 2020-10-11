from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

from os import path

# creates the flask app
app = Flask(__name__)

# initializes the flask app as an API
api = Api(app)

# initialize the database (note that sqlalchemy uses sqlite for storage)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

# the models can be created here, this is similar to what happense in node.js/express when creating migrations and 
# defining what the tables/columns/rows are going to be
class VideoModel(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={name}, views={views}, likes={likes})"

# creates the database - models should be defined before this is called
if path.exists('database.db') == False:
    # create_all should only be called if there is no database already created, this is why i check to see
    # if the file exists first
    db.create_all()

# the request parser object will parse the request and make sure it fits the guidelines
# basically it will validate what is being sent through the request to make sure its right
video_create_args = reqparse.RequestParser()

# name is basically the key of the argument, type is the type of value the key will have and
# help is what you give so that when the user doesnt send the right information it will give them a help message
# to know what they are missing 
# when required is set to true it will throw an error if the request does not have the right args attached
video_create_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_create_args.add_argument("views", type=int, help="Views of the video is required", required=True)
video_create_args.add_argument("likes", type=int, help="likes on the video is required", required=True)


# request parser for updating
# when updating none of the args needs to be required since we want the user to be able to update any single field
video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of the video is required")
video_update_args.add_argument("likes", type=int, help="likes on the video is required")

resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer,
}


# Video is inheriting from Resource
# this creates the structure of the resource
class Video(Resource):
    # marshal with will take the resource from the Video class and serialize it using the argument passed
    # in this case resource fields - not this needs to be above any request that needs to return a serialized object
    @marshal_with(resource_fields)
    # we override the get function to return our own resource
    def get(self, video_id):
        # we can query the videomodel by the id to get it
        # this is similar to building out models in express using knex and then querying them only difference
        # is that the methods come prebuilt - first will get the first response
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message=f"Video with id {video_id} does not exist")
        return result

    # both delete and get have need of the video id
    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).delete()
        if not result:
            abort(404, message=f"Video with id {video_id} does not exist")
        db.session.commit()
        return {"message": 'delete successful', "status": 204}
    
    @marshal_with(resource_fields)
    # patch can be used when we need to update only a PART of a resource
    def patch(self, video_id):
        args = video_update_args.parse_args()
        # filtered_args = { key: value for key, value in args.items() if value is not None }
        video = VideoModel.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message=f"Video with id {video_id} does not exist")
        # print(args['name'], 'argstype')
        if args["name"]:
            video.name = args["name"]
        elif args["views"]:
            video.views = args["views"]
        elif video["likes"]:
            video.likes = args["likes"]
        
        db.session.commit()
        return video, 200


# the api resource to use when creating a video - this needs to be separate from the above resource because i want the endpoint to not be associated with ids
# to create a video it should be as simple as sending a video object o the /video endpoint
class CreateVideo(Resource): 
    @marshal_with(resource_fields)
    def post(self):
        # this will parse the request for the args and if they arent in there it will automatically send back an error
        args = video_create_args.parse_args()
        video = VideoModel(name=args['name'], views=args['views'], likes=args['likes'])
        # adds the object to the database session - this adds the video to the database TEMPORARILY
        db.session.add(video)
        # commits any changes to the session to the database - adds anything in the current session to the database PERMANENTLY
        db.session.commit()
        # status codes can be returned with the request, in this case 201 is returned since it stands for created
        return video, 201


# this actually adds the resource to the api
api.add_resource(Video, "/video/<int:video_id>")
api.add_resource(CreateVideo, "/video")

# the app should run if the name of the file running is 'main'
# i also set debug to true to give us information logging in the console
# should only be set to true when running in development environment 
if __name__ == "__main__":
    app.run(debug=True)