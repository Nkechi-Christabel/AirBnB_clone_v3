#!/usr/bin/python3
"""
A script that handles all Place's default RESTFul API actions.
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    if 'user_id' not in request.json:
        abort(400, "Missing user_id")
    if 'name' not in request.json:
        abort(400, "Missing name")
    data = request.get_json()
    user_id = data.get('user_id')
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data['city_id'] = city_id
    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Searches for Place objects based on the provided JSON"""
    if not request.json:
        abort(400, "Not a JSON")

    states = request.json.get('states', [])
    cities = request.json.get('cities', [])
    amenities = request.json.get('amenities', [])

    places = []
    if not states and not cities and not amenities:
        places = storage.all(Place).values()
    else:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    places.extend(city.places)

        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                places.extend(city.places)

        places = list(set(places))

        if amenities:
            places = [place for place in places if all(
                amenity_id in place.amenity_ids for amenity_id in amenities)]

    return jsonify([place.to_dict() for place in places])
