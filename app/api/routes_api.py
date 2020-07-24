from flask import Blueprint, jsonify, request

from flask_jwt_extended import (jwt_required, get_jwt_identity)

routes_api = Blueprint('routes_api', __name__)


@routes_api.route('/mp3Route')
@jwt_required
def mp3_route():
    identity = get_jwt_identity()

    if identity is None:
        response = {
            'message': 'this_endpoint_need_a_valid_session_token'
        }
        return jsonify(response), 400

    response = {
        'message': 'thank_you_for_visiting_your_event_is_logged'
    }
    return jsonify(response), 200


@routes_api.route('/getMp3Route')
@jwt_required
def get_mp3_api():
    identity = get_jwt_identity()

    if get_jwt_identity() is None:
        response = {
            'message': 'this_endpoint_need_a_valid_session_token'
        }
        return jsonify(response), 400

    # get action from param action
    action_arg = request.args.get('action', default='pageView', type=str)

    return True
