from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_heroku import Heroku

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://mnzsrrjbysgnyl:3ff9c29ee8a96a62be6b2d84b28944422dc253ced6c7873dc9ba2b6acc2ddbf2@ec2-54-83-23-121.compute-1.amazonaws.com:5432/d4fchoqi7jvgfv"

heroku = Heroku(app)
db = SQLAlchemy(app)

class Movie(db.Model):
	__tablename__ = "movies"
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120))
	rating = db.Column(db.Integer)

	def __init__(self, title, rating):
		self.title = title
		self.rating = rating

	def __repr__(self):
		return '<Title %r>' % self.title


@app.route('/')
def home():
	return "<h1>Hello!</h1>"

@app.route('/movies/input', methods=['POST'])
def movies_input():
	if request.content_type == 'application/json':
		post_data = request.get_json()
		title = post_data.get('title')
		rating = post_data.get('rating')
		reg = Movie(title, rating)
		db.session.add(reg)
		db.session.commit()
		return "Data Posted"
	return ""

@app.route('/return/movies', methods=['GET'])
def return_movies():
	all_movies = db.session.query(Movie.title, Movie.rating).all()
	return jsonify(all_movies)

if __name__ == '__main__':
	app.debug = True
	app.run()