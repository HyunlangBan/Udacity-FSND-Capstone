import os
from flask import Flask, render_template, jsonify, request, abort, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from forms import *
from models import setup_db, Restaurant, Reservation, Customer, db
import os
from datetime import datetime
from auth import AuthError, requires_auth


NUM_PER_PAGE = 10


def paginate_restaurants(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page-1)*NUM_PER_PAGE
    end = start + NUM_PER_PAGE

    restaurants = [restaurant.format() for restaurant in selection]
    current_restaurants = restaurants[start:end]

    return current_restaurants


def capacity_check(check_time, rest_id, number):
    rest = Restaurant.query.filter(Restaurant.id == rest_id).one_or_none()
    reservations = Reservation.query.filter(Reservation.rest_id == rest_id)
    reserved_number = 0
    capacity = rest.capacity
    check_time = datetime.strptime(check_time, '%Y-%m-%d %H:%M:%S')

    for reservation in reservations:
        if reservation.time == check_time:
            reserved_number += reservation.number

    total_number = reserved_number + int(number)
    if total_number <= capacity:
        return True
    else:
        return False


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    app.config['SECRET_KEY'] = 'secret'

    @app.route('/')
    def index():
        return redirect('https://hrban.auth0.com/authorize?audience=reservation&response_type=token&client_id=xnDUNOvj9p9HAkqHLvFabfh5zuwat9uQ&redirect_uri=https://capstone-reservation-service.herokuapp.com/login-results')

    # restaurants
    @app.route('/restaurants')
    @requires_auth('get:restaurants')
    def get_restaurants_list(jwt):
        selection = Restaurant.query.order_by(Restaurant.id).all()
        current_restaurants = paginate_restaurants(request, selection)

        return jsonify(
            {'restaurants': current_restaurants,
             'total_restaurants': len(Restaurant.query.all()),
             'success': True}
        )

    @app.route('/restaurants/create', methods=['POST'])
    @requires_auth('post:restaurants')
    def create_restaurants(jwt):
        body = request.get_json()

        if body is None:
            abort(422)

        rest = Restaurant()

        rest.name = body.get('name')
        rest.address = body.get('address')
        rest.category = body.get('category')
        rest.photo = body.get('photo', None)
        rest.tel = body.get('tel')
        rest.menu = body.get('menu')
        rest.capacity = body.get('capacity')
        rest.open_time = body.get('open_time')
        rest.close_time = body.get('close_time')

        rest.insert()

        selection = Restaurant.query.order_by(Restaurant.id).all()

        current_restaurnats = paginate_restaurants(request, selection)

        return jsonify(
            {
                'current_restaurants': current_restaurnats,
                'total_restaurants': len(current_restaurnats),
                'success': True,
                'result': rest.name
            }
        )

    @app.route('/restaurants/search', methods=['POST'])
    @requires_auth('search:restaurants')
    def search_restaurants(jwt):
        searchTerm = request.args.get('searchTerm', '', type=str)

        selection = Restaurant.query.order_by(Restaurant.id).filter(
            Restaurant.name.ilike('%{}%'.format(searchTerm))).all()
        current_restaurants = paginate_restaurants(request, selection)

        return jsonify(
            {'current_restaurants': current_restaurants,
             'total_restaurants': len(current_restaurants),
             'success': True}
        )

    @app.route('/restaurants/<int:rest_id>')
    @requires_auth('get:restaurant')
    def show_restaurant(jwt, rest_id):
        restaurant = Restaurant.query.filter(
            Restaurant.id == rest_id).one_or_none()

        if restaurant is None:
            abort(404)

        else:
            return jsonify(
                {
                    'success': True,
                    'restaurant': restaurant.format(),
                    'rest_id': rest_id
                }
            )

    @app.route('/restaurants/<int:rest_id>', methods=['DELETE'])
    @requires_auth('delete:restaurant')
    def delete_restaurant(jwt, rest_id):
        restaurant = Restaurant.query.filter(
            Restaurant.id == rest_id).one_or_none()

        if restaurant is None:
            abort(404)

        restaurant.delete()

        selection = Restaurant.query.order_by(Restaurant.id).all()
        current_restaurants = paginate_restaurants(request, selection)

        return jsonify(
            {
                'success': True,
                'current_restaurants': current_restaurants,
                'total_restaurants': len(current_restaurants),
                'deleted': rest_id
            }
        )

    @app.route('/restaurants/<int:rest_id>/edit', methods=['PATCH'])
    @requires_auth('edit:restaurant')
    def edit_restaurant_submission(jwt, rest_id):
        body = request.get_json()

        if body is None:
            abort(422)

        rest = Restaurant.query.filter(Restaurant.id == rest_id).one_or_none()

        rest.name = body.get('name')
        rest.address = body.get('address')
        rest.category = body.get('category')
        rest.photo = body.get('photo')
        rest.tel = body.get('tel')
        rest.menu = body.get('menu')
        rest.capacity = body.get('capacity')
        rest.open_time = body.get('open_time')
        rest.close_time = body.get('close_time')

        rest.update()

        selection = Restaurant.query.order_by(Restaurant.id).all()

        current_restaurants = paginate_restaurants(request, selection)

        return jsonify(
            {
                'current_restaurants': current_restaurants,
                'edited': rest_id,
                'success': True
            }
        )

    # reservations
    @app.route('/reservations/create', methods=['POST'])
    @requires_auth('make:reservation')
    def make_reservations(jwt):
        email = request.args.get('customer_email', type=str)
        customer_id = db.session.query(Customer.id).filter(
            Customer.email == email).one_or_none()

        if customer_id is None:
            abort(404)

        rest_name = request.args.get('rest_name', type=str)
        rest_id = db.session.query(Restaurant.id).filter(
            Restaurant.name == rest_name).one_or_none()

        if rest_id is None:
            abort(404)

        body = request.get_json()

        if body is None:
            abort(422)

        time = body.get('time')
        number = body.get('number')

        if capacity_check(time, rest_id, number):
            rsvn = Reservation()
            rsvn.rest_id = rest_id
            rsvn.customer_id = customer_id

            rsvn.number = number
            rsvn.time = time
            rsvn.request = body.get('request', None)

            rsvn.insert()

            reservation_details = {
                'customer': rsvn.customer.format(),
                'restaurant': rsvn.rest.format(),
                'reservation': rsvn.format()
            }

            return jsonify(
                {
                    'success': True,
                    'reservation': reservation_details
                }
            )

        else:
            return jsonify({
                'message': "This restaurant is fully booked. Check other times.",
                'success': False
            })

    @app.route('/reservations/<int:customer_id>')
    @requires_auth('get:reservations')
    def show_reservations_list_for_customer(jwt, customer_id):
        reservations = Reservation.query.order_by(Reservation.time).filter(
            Reservation.customer_id == customer_id).all()

        if reservations == []:
            abort(404)

        past_reservations = []
        upcoming_reservations = []

        for reservation in reservations:
            if reservation.time < datetime.now():
                past_reservations.append(reservation.format())
            else:
                upcoming_reservations.append(reservation.format())

        return jsonify(
            {
                'success': True,
                'past_reservations': past_reservations,
                'upcoming_reservations': upcoming_reservations
            }
        )

    @app.route('/reservations/<int:rest_id>/owner')
    @requires_auth('check:reservations')
    def show_reservations_list_for_restaurant(jwt, rest_id):
        reservations = Reservation.query.order_by(
            Reservation.time).filter(Reservation.rest_id == rest_id).all()

        if reservations == []:
            abort(404)

        past_reservations = []
        upcoming_reservations = []

        for reservation in reservations:
            customer = reservation.customer
            if reservation.time < datetime.now():
                data = {
                    'reservations': reservation.format(),
                    'customer': customer.format()
                }
                past_reservations.append(data)
            else:
                data = {
                    'reservations': reservation.format(),
                    'customer': customer.format()
                }
                past_reservations.append(data)

        return jsonify(
            {
                'success': True,
                'past_reservations': past_reservations,
                'upcoming_reservations': upcoming_reservations
            }
        )

    @app.route('/reservations/<int:reservation_id>/review', methods=['PATCH'])
    @requires_auth('post:review')
    def review_past_reservations(jwt, reservation_id):
        rsvn = Reservation.query.filter(
            Reservation.id == reservation_id).one_or_none()

        if rsvn is None:
            abort(404)

        body = request.get_json()

        if body is None:
            abort(422)

        review = body.get('review')
        rsvn.review = review

        rsvn.update()

        return jsonify(
            {
                'reservation': rsvn.format(),
                'success': True
            }
        )

    @app.route('/reservations/<int:reservation_id>/edit', methods=['PATCH'])
    @requires_auth('edit:reservation')
    def edit_upcoming_reservation_submission(jwt, reservation_id):
        body = request.get_json()

        if body is None:
            abort(422)

        rsvn = Reservation.query.filter(
            Reservation.id == reservation_id).one_or_none()

        if rsvn is None:
            abort(404)

        rest_id = rsvn.rest.id
        rsvn.number = body.get('number')
        rsvn.time = body.get('time')
        rsvn.request = body.get('request', None)

        capacity = capacity_check(rsvn.time, rest_id, rsvn.number)

        if capacity:
            rsvn.update()

            return jsonify(
                {
                    'reservation': rsvn.format(),
                    'success': True
                }
            )

        else:
            return jsonify(
                {
                    'success': False,
                    'message': "The number is over capactiy."
                }
            )

    # customers
    @app.route('/customers/create', methods=['POST'])
    @requires_auth('post:customer')
    def create_customer(jwt):
        body = request.get_json()

        if body is None:
            abort(422)

        customer = Customer()

        customer.name = body.get('name')
        customer.phone = body.get('phone')
        customer.email = body.get('email')

        customer.insert()

        return jsonify(
            {
                'customer': customer.format(),
                'success': True
            }
        )

    @app.route('/customers/<int:customer_id>/edit', methods=['POST'])
    @requires_auth('edit:customer')
    def edit_customer_submission(jwt, customer_id):
        body = request.get_json()

        if body is None:
            abort(422)

        customer = Customer.query.filter(
            Customer.id == customer_id).one_or_none()

        if customer is None:
            abort(404)

        customer.name = body.get('name')
        customer.phone = body.get('phone')
        customer.email = body.get('email')

        customer.update()

        return jsonify(
            {
                'customer': customer.format(),
                'success': True
            }
        )

    @app.route('/customers/<int:customer_id>', methods=['DELETE'])
    @requires_auth('delete:customer')
    def delete_customer(jwt, customer_id):
        customer = Customer.query.filter(
            Customer.id == customer_id).one_or_none()

        if customer is None:
            abort(404)

        customer.delete()

        current_customers = Customer.query.all()

        return jsonify(
            {
                'deleted': customer_id,
                'success': True
            }
        )

    # Error Handling
    @app.errorhandler(AuthError)
    def authentification_failed(AuthError):
        return jsonify({
            "success": False,
            "error": AuthError.status_code,
            "message": "authentification fails"
        }), 401

    @app.errorhandler(404)
    def authentification_failed(AuthError):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'maessage': 'unprocessable',
            'error': 422
        }), 422

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify(
            {
                'success': False,
                'message': 'Method not allowed',
                'error': 405
            }
        ), 405

    return app
