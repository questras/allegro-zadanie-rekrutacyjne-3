"""
Module with views present in the app.
"""

from flask import Blueprint, current_app, request, jsonify, abort

from .services import GithubApiService
from .exceptions import (
    UserNotFoundServiceException,
    BadCredentialsServiceException,
    ApiRateLimitExceededServiceException,
    UnprocessableEntityServiceException
)

# Flask blueprint for endpoints related to github.
github_blueprint = Blueprint('github', __name__)


@github_blueprint.errorhandler(404)
def user_not_found(_):
    message = jsonify({'message': 'User not found'})
    return message, 404


@github_blueprint.errorhandler(500)
def server_error(_):
    message = jsonify({'message': 'Server error'})
    return message, 500


@github_blueprint.errorhandler(422)
def unprocessable_request(e):
    message = jsonify({'message': e.description})
    return message, 422


@github_blueprint.route('/repositories/<string:username>', methods=['GET'])
def user_repositories_view(username):
    """
    View to get given user's repositories' names and stars.
    The result is paginated and a page can be specified via
    url parameter e.g ?page=0. Default page is 0.
    Repositories with correct pagination are obtained from
    `GithubApiService` class.

    Result is a json in following format:
    {
        "repositories": [
            {
                "name": "repo-name1",
                "stars": 1
            },
            ...
        ],
        "repositories_count": 3,
        "username": "given-username",
    }

    If given user does not exist, response with 404 code is sent.
    If the request cannot be correctly processed by `GithubApiService`,
        then response with 422 code and specific message is sent.
    If there are problems with github api token e.g bad token or token
        with exceeded api calls limit, then response with 500 code is sent.
    """

    api = GithubApiService(
        github_api_token=current_app.config['GITHUB_API_TOKEN']
    )

    try:
        page = int(request.args.get('page') or 0)
    except ValueError:
        # Page is not an instance of an integer.
        page = 0

    try:
        repositories = api.get_user_repositories(username, page)
    except UserNotFoundServiceException:
        abort(404)
    except BadCredentialsServiceException:
        # Problem with token.
        abort(500)
    except ApiRateLimitExceededServiceException:
        # Exceeded api calls limit.
        abort(500)
    except UnprocessableEntityServiceException as e:
        # Api could not process the request correctly.
        abort(422, str(e))

    return {
        'repositories': repositories,
        'repositories_count': len(repositories),
        'username': username
    }
