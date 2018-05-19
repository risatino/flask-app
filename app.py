# import necessary libraries
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    movie_title = db.Column(db.String(80), nullable=False)
    imdb_id = db.Column(db.String(12), nullable=True)
    year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Movie %r>' % self.movie_title

class AnyObjectThing(db.Model):
    __tablename__ = 'any'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)

db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send", methods=["GET","POST"])
def send_data():
    if request.method == "POST":
        movie_title = request.form["movie_title"]
        imdb_id = request.form["imdb_id"]
        year = request.form["year"]
        movie = Movie(movie_title=movie_title, imdb_id=imdb_id, year=year)
        db.session.add(movie)
        db.session.commit()

        return redirect("/", code=302)

    return render_template("send.html")

@app.route("/display")
def display_movies():
    results = db.session.query(Movie.movie_title, Movie.imdb_id).all()
    print(results)
    return render_template("movies.html", movies=results)

@app.route("/api/data")
def api_data():
    results = db.session.query(Movie.movie_title, Movie.imdb_id, Movie.year).all()
    result_objects = [{"title": x[0], "imdb_id": x[1], "year": x[2]} for x in results]
    return jsonify(result_objects)

if __name__ == "__main__":
    app.run(debug=True)