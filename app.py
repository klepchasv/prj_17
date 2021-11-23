# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

movies_ns = api.namespace("movies")
directors_ns = api.namespace("directors")
genres_ns = api.namespace("genres")


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@movies_ns.route("/")
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get("director_id")
        genre_id = request.args.get("genre_id")
        if director_id and genre_id:
            movies = Movie.query.filter(Movie.director_id==director_id, Movie.genre_id==genre_id).all()
            return movies_schema.dump(movies), 200
        if director_id:
            movies = Movie.query.filter(Movie.director_id==director_id).all()
            return movies_schema.dump(movies), 200
        if genre_id:
            movies = Movie.query.filter(Movie.genre_id==genre_id).all()
            return movies_schema.dump(movies), 200
        movies = Movie.query.all()
        return movies_schema.dump(movies), 200


@movies_ns.route("/<int:mid>")
class MovieView(Resource):
    def get(self, mid):
        movie = Movie.query.get(mid)
        if movie:
            return  movie_schema.dump(movie), 200
        return "", 404


@genres_ns.route("/<int:gid>")
class GenresView(Resource):
    def post(self, gid):
        genre = request.get_json()[0]
        new_genre = Genre(id = genre["id"], name = genre["name"])
        with db.session.begin():
            db.session.add(new_genre)
        return "", 204
    def put(self, gid):
        new_data = request.get_json()[0]
        genre_to_update = Genre.query.get(gid)
        genre_to_update.name = new_data["name"]
        db.session.add(genre_to_update)
        db.session.commit()
        return "", 204
    def delete(self, gid):
        genre_to_delete = Genre.query.get(gid)
        db.session.delete(genre_to_delete)
        db.session.commit()
        return "", 204
        

@directors_ns.route("/<int:did>")
class DirectorsView(Resource):
    def post(self, did):
        director = request.get_json()[0]
        new_director = Genre(id = director["id"], name = director["name"])
        with db.session.begin():
            db.session.add(new_director)
        return "", 204
    def put(self, did):
        new_data = request.get_json()[0]
        director_to_update = Genre.query.get(did)
        director_to_update.name = new_data["name"]
        db.session.add(director_to_update)
        db.session.commit()
        return "", 204
    def delete(self, did):
        director_to_delete = Genre.query.get(did)
        db.session.delete(director_to_delete)
        db.session.commit()
        return "", 204
        

if __name__ == '__main__':
    app.run(debug=True)
