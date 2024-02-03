#!/usr/bin/python3
"""
A new view for the link between Place objects and Amenity objects
that handles all default RESTFul API actions
"""
from flask import jsonify, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if storage.__class__.__name__ == 'DBStorage':
        amenities = [amenity.to_dict() for amenity in place.amenities]
    elif storage.__class__.__name__ == 'FileStorage':
        amenities = [storage.get(Amenity, amenity_id).to_dict() for amenity_id in place.amenity_ids]

    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def link_place_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if storage.__class__.__name__ == 'DBStorage':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    elif storage.__class__.__name__ == 'FileStorage':
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)

    storage.save()
    return jsonify(amenity.to_dict()), 201
