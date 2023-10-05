# ---------------------------------------------------------------------------- #
# Imports
# ---------------------------------------------------------------------------- #

from datetime import datetime
import babel
import dateutil.parser
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from flask_moment import Moment

from forms import ShowForm, VenueForm, ArtistForm
from logger import Logger
from models import Venue, Artist, Show, db

# ---------------------------------------------------------------------------- #
# App Config.
# ---------------------------------------------------------------------------- #

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
with app.app_context():
    db.create_all()
logger = Logger.get_logger(__name__)
migrate = Migrate(app, db)


# ---------------------------------------------------------------------------- #
# Page Constants.
# ---------------------------------------------------------------------------- #
PAGE_HOME = 'pages/home.html'
PAGE_VENUE = 'pages/venues.html'
PAGE_SEARCH_VENUE = 'pages/search_venues.html'
PAGE_NEW_VENUE = 'forms/new_venue.html'
PAGE_EDIT_VENUE = 'forms/edit_venue.html'
PAGE_SHOW_VENUE = 'pages/show_venue.html'
PAGE_ARTIST = 'pages/artists.html'
PAGE_SHOW_ARTIST = 'pages/show_artist.html'
PAGE_SEARCH_ARTIST = 'pages/search_artists.html'
PAGE_NEW_ARTIST = 'forms/new_artist.html'
PAGE_EDIT_ARTIST = 'forms/edit_artist.html'
PAGE_SHOW = 'pages/shows.html'
PAGE_CREATE_SHOW = 'forms/new_show.html'
PAGE_ERROR_404 = 'errors/404.html'
PAGE_ERROR_500 = 'errors/500.html'


# ---------------------------------------------------------------------------- #
# Filters.
# ---------------------------------------------------------------------------- #


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        _format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        _format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, _format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

# ---------------------------------------------------------------------------- #
# Controllers.
# ---------------------------------------------------------------------------- #


@app.route('/')
def index() -> str:
    logger.info('Requesting home page')
    return render_template(template_name_or_list=PAGE_HOME)


# ---------------------------------------------------------------------------- #
#  Venues.
#  --------------------------------------------------------------------------- #

@app.route('/venues')
def venues():
    logger.info('Requesting venues page')
    response = []
    city_list = []
    venue_list = Venue.query.all()
    for venue in venue_list:
        if venue.city not in city_list:
            city_list.append(venue.city)
            response.append({
                'city': venue.city,
                'state': venue.state,
                'venues': [
                    {
                        'id': item.id,
                        'name': item.name,
                        'num_upcoming_shows': len(item.shows)
                    }
                    for item in venue_list
                    if item.city == venue.city
                ]
            })
    logger.info('Response: ' + str(response))
    return render_template(
        template_name_or_list=PAGE_VENUE,
        areas=response
    )


@app.route('/venues/search', methods=['POST'])
def search_venues():
    logger.info('Requesting search venues page')
    response = {"count": 0, "data": []}
    search_term = request.form.get('search_term', '')

    terms = search_term.strip().split(',')
    if len(terms) == 2:
        city, state = terms
        city = city.strip()
        state = state.strip()
        venues = Venue.query.filter(
            Venue.city.ilike(f'%{city}%'),
            Venue.state.ilike(f'%{state}%'))
        response['city'] = city
        response['state'] = state
    else:
        venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%'))
    response["count"] = venues.count()
    for venue in venues:
        response["data"].append({
            'id': venue.id,
            'name': venue.name,
            'num_upcoming_shows': len(venue.shows)
        })
    logger.info('Response: ' + str(response))
    return render_template(
        template_name_or_list=PAGE_SEARCH_VENUE,
        results=response,
        search_term=request.form.get('search_term', '')
    )


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    logger.info('Requesting show venue page')
    venue = Venue.query.get(venue_id)

    past_shows_query = db.session.query(Show).join(Venue).filter(
        Show.venue_id == venue_id).filter(
        Show.start_time < datetime.now()).all()
    past_shows = []
    for show in past_shows_query:
        past_shows.append(
            {
                "artist_id": show.artist_id,
                "artist_name": show.artist.name,
                "artist_image_link": show.artist.image_link,
                "start_time": str(show.start_time)
            }
        )

    upcoming_shows_query = db.session.query(Show).join(Venue).filter(
        Show.venue_id == venue_id).filter(
        Show.start_time > datetime.now()).all()
    upcoming_shows = []
    for show in upcoming_shows_query:
        upcoming_shows.append(
            {
                "artist_id": show.artist_id,
                "artist_name": show.artist.name,
                "artist_image_link": show.artist.image_link,
                "start_time": str(show.start_time)
            }
        )

    response = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres.split(','),
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }
    logger.info('Response: ' + str(response))
    return render_template(
        template_name_or_list=PAGE_SHOW_VENUE,
        venue=response
    )


# ---------------------------------------------------------------------------- #
#  Create Venue.
# ---------------------------------------------------------------------------- #


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    logger.info('Requesting create venue page')
    return render_template(
        template_name_or_list=PAGE_NEW_VENUE,
        form=VenueForm()
    )


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    logger.info('Requesting create venue submission')
    try:
        form = VenueForm(request.form)
        name = form.name.data.strip()
        city = form.city.data.strip()
        state = form.state.data.strip()
        address = form.address.data.strip()
        phone = form.phone.data.strip()
        image_link = form.image_link.data.strip()
        facebook_link = form.facebook_link.data.strip()
        seeking_talent = form.seeking_talent.data
        seeking_description = form.seeking_description.data.strip()
        website = form.website_link.data.strip()
        genres = ",".join(form.genres.data)

        venue = Venue(
            name=name,
            state=state,
            city=city,
            address=address,
            phone=phone,
            image_link=image_link,
            facebook_link=facebook_link,
            seeking_talent=seeking_talent,
            seeking_description=seeking_description,
            website_link=website,
            genres=genres
        )
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
        db.session.add(venue)
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash(
            'An error occurred. Venue '
            + request.form['name']
            + ' could not be listed.'
        )
    finally:
        db.session.close()
    return render_template(template_name_or_list=PAGE_HOME)


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    logger.info('Requesting delete venue')
    try:
        venue = Venue.query.get(venue_id)
        for show in venue.shows:
            db.session.delete(show)

        db.session.delete(venue)
        db.session.commit()
        flash(venue.name + ' is successfully deleted!')
        logger.info('Deleted venue: ' + venue.name)
    except Exception:
        db.session.rollback()
        flash('An error occurred. Venue ' + venue.name + ' is not deleted!!!')
    finally:
        db.session.close()
    return redirect(url_for('index'))

# ---------------------------------------------------------------------------- #
# Artists.
# ---------------------------------------------------------------------------- #


@app.route('/artists')
def artists():
    logger.info('Requesting artists page')
    response = Artist.query.all()
    logger.info('Response: ' + str(response))
    return render_template(
        template_name_or_list=PAGE_ARTIST,
        artists=response
    )


@app.route('/artists/search', methods=['POST'])
def search_artists():
    logger.info('Requesting search artists page')
    response = {"count": 0, "data": []}
    search_term = request.form.get('search_term', '')

    terms = search_term.strip().split(',')
    if len(terms) == 2:
        city, state = terms
        city = city.strip()
        state = state.strip()
        artists = Artist.query.filter(
            Artist.city.ilike(f'%{city}%'),
            Artist.state.ilike(f'%{state}%'))
        response['city'] = city
        response['state'] = state
    else:
        artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%'))
    response["count"] = artists.count()
    for artist in artists:
        response["data"].append({
            'id': artist.id,
            'name': artist.name,
            'num_upcoming_shows': len(artist.shows)
        })
    logger.info('Response: ' + str(response))
    return render_template(
        template_name_or_list=PAGE_SEARCH_ARTIST,
        results=response,
        search_term=request.form.get(
            'search_term',
            '')
    )


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    logger.info('Requesting show artist page')
    artist = Artist.query.get(artist_id)
    past_shows_query = db.session.query(Show).join(Artist).filter(
        Show.artist_id == artist_id).filter(
        Show.start_time < datetime.now()).all()
    past_shows = []
    for show in past_shows_query:
        past_shows.append(
            {
                "venue_id": show.venue_id,
                "venue_name": show.venue.name,
                "venue_image_link": show.venue.image_link,
                "start_time": str(show.start_time)
            }
        )

    upcoming_shows_query = db.session.query(Show).join(Artist).filter(
        Show.artist_id == artist_id).filter(
        Show.start_time > datetime.now()).all()
    upcoming_shows = []
    for show in upcoming_shows_query:
        upcoming_shows.append(
            {
                "venue_id": show.venue_id,
                "venue_name": show.venue.name,
                "venue_image_link": show.venue.image_link,
                "start_time": str(show.start_time)
            }
        )

    response = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres.split(','),
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }
    logger.info('Response: ' + str(response))
    return render_template(
        template_name_or_list=PAGE_SHOW_ARTIST,
        artist=response
    )

# ---------------------------------------------------------------------------- #
# Update.
# ---------------------------------------------------------------------------- #


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    logger.info('Requesting edit artist page')
    artist = Artist.query.get(artist_id)
    form = ArtistForm()
    form.genres.default = artist.genres.split(",")
    form.name.default = artist.name
    form.city.default = artist.city
    form.state.default = artist.state
    form.phone.default = artist.phone
    form.facebook_link.default = artist.facebook_link
    form.website_link.default = artist.website_link
    form.image_link.default = artist.image_link
    form.seeking_venue.default = artist.seeking_venue
    form.seeking_description.default = artist.seeking_description
    form.process()
    return render_template(
        template_name_or_list=PAGE_EDIT_ARTIST,
        form=form,
        artist=artist
    )


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    logger.info('Requesting edit artist submission')
    try:
        artist = Artist.query.get(artist_id)
        form = ArtistForm(request.form)
        artist.name = form.name.data
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.facebook_link = form.facebook_link.data
        artist.website_link = form.website_link.data
        artist.image_link = form.image_link.data
        artist.seeking_venue = form.seeking_venue.data
        artist.seeking_description = form.seeking_description.data
        artist.genres = ",".join(form.genres.data)

        db.session.commit()
        flash('ARTIST ' + request.form['name'] + ' WAS SUCCESSFULLY UPDATED!')
    except Exception:
        db.session.rollback()
        flash('FAILED TO UPDATE' + request.form['name'] + ' in the database!!')
    return redirect(
        location=url_for(
            endpoint='show_artist',
            artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    logger.info('Requesting edit venue page')
    venue = Venue.query.get(venue_id)
    form = VenueForm(obj=venue)
    form.genres.default = venue.genres.split(",")
    form.name.default = venue.name
    form.city.default = venue.city
    form.state.default = venue.state
    form.address.default = venue.address
    form.phone.default = venue.phone
    form.facebook_link.default = venue.facebook_link
    form.website_link.default = venue.website_link
    form.image_link.default = venue.image_link
    form.seeking_talent.default = venue.seeking_talent
    form.seeking_description.default = venue.seeking_description
    form.process()
    return render_template(
        template_name_or_list=PAGE_EDIT_VENUE,
        form=form,
        venue=venue
    )


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    logger.info('Requesting edit venue submission')
    try:
        venue = Venue.query.get(venue_id)
        form = VenueForm(request.form)
        venue.name = form.name.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.phone = form.phone.data
        venue.address = form.address.data
        venue.facebook_link = form.facebook_link.data
        venue.website_link = form.website_link.data
        venue.image_link = form.image_link.data
        venue.seeking_talent = form.seeking_talent.data
        venue.seeking_description = form.seeking_description.data
        venue.genres = ",".join(form.genres.data)

        db.session.commit()
        flash('VENUE ' + request.form['name'] + ' WAS SUCCESSFULLY UPDATED!')
    except Exception:
        db.session.rollback()
        flash('FAILED TO UPDATE' + request.form['name'] + ' in the database!!')
    return redirect(url_for('show_venue', venue_id=venue_id))

# ---------------------------------------------------------------------------- #
# Create Artist.
# ---------------------------------------------------------------------------- #


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    logger.info('Requesting create artist page')
    return render_template(
        template_name_or_list=PAGE_NEW_ARTIST,
        form=ArtistForm()
    )


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    logger.info('Requesting create artist submission')
    try:
        form = ArtistForm(request.form)
        name = form.name.data.strip()
        city = form.city.data.strip()
        state = form.state.data.strip()
        phone = form.phone.data.strip()
        image_link = form.image_link.data.strip()
        facebook_link = form.facebook_link.data.strip()
        seeking_venue = form.seeking_venue.data
        seeking_description = form.seeking_description.data.strip()
        website = form.website_link.data.strip()
        genres = ",".join(form.genres.data)

        artist = Artist(
            name=name,
            city=city,
            state=state,
            phone=phone,
            image_link=image_link,
            facebook_link=facebook_link,
            seeking_venue=seeking_venue,
            seeking_description=seeking_description,
            website_link=website,
            genres=genres
        )
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except Exception:
        db.session.rollback()
        flash(
            'An error occurred. Artist '
            + request.form['name']
            + ' could not be listed!'
        )
    finally:
        db.session.close()
    return render_template(template_name_or_list=PAGE_HOME)


# ---------------------------------------------------------------------------- #
# Shows.
# ---------------------------------------------------------------------------- #

@app.route('/shows')
def shows():
    logger.info('Requesting shows page')
    response = []
    show_list = Show.query.all()
    for show in show_list:
        response.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": str(show.start_time)
        })
    logger.info('Response: ' + str(response))
    return render_template(
        template_name_or_list=PAGE_SHOW,
        shows=response
    )


@app.route('/shows/create')
def create_shows():
    logger.info('Requesting create show page')
    return render_template(
        template_name_or_list=PAGE_CREATE_SHOW,
        form=ShowForm()
    )


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    logger.info('Requesting create show submission')
    try:
        form = ShowForm(request.form)
        artist_id = int(form.artist_id.data)
        venue_id = int(form.venue_id.data)
        start_time = form.start_time.data
        show = Show(
            start_time=start_time,
            artist_id=artist_id,
            venue_id=venue_id
        )
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
    except Exception:
        db.session.rollback()
        flash('An error occurred. Show could not be listed!')
    finally:
        db.session.close()
    return render_template(template_name_or_list=PAGE_HOME)


@app.errorhandler(404)
def not_found_error(error):
    logger.error('404 error')
    return render_template(template_name_or_list=PAGE_ERROR_404), 404


@app.errorhandler(500)
def server_error(error):
    logger.error('500 error')
    return render_template(template_name_or_list=PAGE_ERROR_500), 500


if not app.debug:
    app.logger = logger
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
