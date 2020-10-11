from configuration.extensions import db

# the models can be created here, this is similar to what happense in node.js/express when creating migrations and 
# defining what the tables/columns/rows are going to be
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={name}, views={views}, likes={likes})"