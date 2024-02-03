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

@app_views.route('/places_search', methods=['POST'])
def places_search():

    headers = request.headers.get('Content-Type')
    if headers != 'application/json':
        abort(400, 'Not a JSON')

    if not request.get_json():
        return jsonify([places.to_dict() for
                        places in storage.all('Place').values()])

    res = []
    places = []
    amenities = []
    obj = request.get_json()

    #get all cities from states if states passed
    for k, v in obj.items():
        if k == 'states':
            for item in v:
                state_obj = storage.get('State', item)
                for city in state_obj.cities:
                    res.append(city.id)
    #add cities to existing cities list after looking through states
    for k, v in obj.items():
        if k == 'cities':
            for item in v:
                if item not in res:
                    res.append(item)

    #create amenities list if amenities passed
    for k, v in obj.items():
        if k == 'amenities':
            for item in v:
                if item not in res:
                    amenities.append(item)

    #create list of place id's from all cities
    for place in storage.all('Place').values():
        if place.city_id in res:
            places.append(place.id)

    #if places is empty and amenities is not empty
    if places == [] and amenities != []:
        remove = []
        res = []
        places = [place.id for place in storage.all('Place').values()]
        for place in places:
            obj = storage.get('Place', place)
            for amen in obj.amenities:
                if amen.id not in amenities:
                    if place not in remove:
                        remove.append(place)
        for place in places:
            if place not in remove:
                res.append(place)
        return jsonify([storage.get('Place', obj).to_dict()
                        for obj in res])

    if amenities != []:
        for place in places:
            obj = storage.get('Place', place)
            for amenity in amenities:
                if amenity not in obj.amenities:
                    places.remove(place)

    return jsonify([storage.get('Place', id).to_dict() for id in places])
