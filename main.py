from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField, URLField
from wtforms.validators import DataRequired, URL, Optional
from moviedb import MovieDB

BASE_IMAGE_URL="https://image.tmdb.org/t/p/original/"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movie-collection.db"
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

db.init_app(app)

# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()

class Search(FlaskForm):
    search = StringField("Search Title", validators=[DataRequired()])
    # title = StringField("Title", validators=[DataRequired()])
    # year = IntegerField("Year", validators=[DataRequired()])
    # description = StringField("Description", validators=[DataRequired()])
    # rating = FloatField("Rating", validators=[DataRequired()])
    # ranking = IntegerField("Ranking", validators=[DataRequired()])
    # review = StringField("Review", validators=[DataRequired()])
    # img_url = URLField("Image URL", validators=[DataRequired()])
    submit = SubmitField('Submit')

class Edit(FlaskForm):
    rating = FloatField("Rating", validators=[Optional()])
    ranking = IntegerField("Ranking", validators=[Optional()])
    review = StringField("Review")
    # description = StringField("Description")
    # img_url = URLField("Image URL")
    submit = SubmitField('Submit')

@app.route("/")
def home():
    # new_movie = Movie(
    #     title="Phone Booth",
    #     year=2002,
    #     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
    #     rating=7.3,
    #     ranking=10,
    #     review="My favourite character was the caller.",
    #     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
    # )
    # db.session.add(new_movie)
    # db.session.commit()
    # second_movie = Movie(
    #     title="Avatar The Way of Water",
    #     year=2022,
    #     description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
    #     rating=7.3,
    #     ranking=9,
    #     review="I liked the water.",
    #     img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
    # )
    # db.session.add(second_movie)
    # db.session.commit()
    all_movies = db.session.execute(db.select(Movie).order_by(Movie.ranking)).scalars()
    print(all_movies)
    return render_template("index.html", all_movies=all_movies)

@app.route('/edit', methods=["GET", "POST"])
def edit_movie():
    form = Edit()
    if form.validate_on_submit():
        id = request.args.get('id')
        movie = db.get_or_404(Movie, id)
        if form.rating.data:
            movie.rating = form.rating.data
        if form.ranking.data:
            movie.ranking = form.ranking.data
        if form.review.data:
            movie.review = form.review.data
        # if form.description.data:
        #     movie.description = form.description.data
        # if form.img_url.data:
        #     movie.img_url = form.img_url.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', form=form)

@app.route("/delete")
def delete():
    id = request.args.get('id')
    movie = db.get_or_404(Movie, id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/search', methods=["GET", "POST"])
def search():
    form = Search()
    if form.validate_on_submit():
        print("submitting")
        new_search = MovieDB()
        print(form.search.data)
        results = new_search.search(form.search.data)
        print(results)
        return render_template('select.html', results=results)
    return render_template('search.html', form=form)

@app.route('/select', methods=["GET", "POST"])
def select(results):
    return render_template('select.html', results=results)

@app.route('/add', methods=["GET", "POST"])
def add():
    new_movie = Movie(
        title=request.args.get('title'),
        year=request.args.get('year'),
        description=request.args.get('description'),
        img_url=BASE_IMAGE_URL + request.args.get('img_url')
    )
    db.session.add(new_movie)
    db.session.commit()
    print(new_movie.id)
    return redirect(url_for("edit_movie", id=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)
