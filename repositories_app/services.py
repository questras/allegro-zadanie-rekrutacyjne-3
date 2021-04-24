"""
Module providing integration with 3rd party services.
"""

from typing import Dict, List, Any

import github

from .exceptions import (
    UserNotFoundServiceException,
    ApiRateLimitExceededServiceException,
    BadCredentialsServiceException,
    UnprocessableEntityServiceException
)


class GithubApiService:
    """
    Class providing integration with 
    github api (https://docs.github.com/en/rest) through
    PyGithub package (https://github.com/PyGithub/PyGithub)
    and its `Github` object.
    Communication with Github API is based on a token. If
    no token is provided to class, then there is a limit
    of 60 requests per hour. Other limits can be found in
    github api documentation.
    """

    _DEFAULT_PER_PAGE_COUNT = 50

    def __init__(self, github_api_token: str = None):
        self.github_api = github.Github(
            login_or_token=github_api_token,
            per_page=GithubApiService._DEFAULT_PER_PAGE_COUNT
        )

    def get_user_repositories(self, username: str,
                              page: int = 0) -> List[Dict[str, Any]]:
        """
        For a given username, return a list of this user's repositories' 
        names with number of stars. Result is paginated with at most 
        `_DEFAULT_PER_PAGE_COUNT` objects on one page. Page number is 
        specified by `page` variable (first page is number 0).

        Args:
            username(str): user, whose repositories will be returned,
            page(int, default=0): number of page of paginated result.

        Returns:
            `list`: list of repositories with following format:
            [
                {
                    "name": "repo-name1",
                    "stars": 5
                },
                {
                    "name": "repo-name2",
                    "stars": 42
                },
                ...
            ]

        Raises:
            `BadCredentialsServiceException`: when bad token is provided.
            `UserNotFoundServiceException`: when desired user is not found.
            `ApiRateLimitExceededServiceException`: when api calls limit was
                exceeded for current token.
        """

        # Set page to 0 if given page number is negative.
        page = max(0, page)

        try:
            repositories = [
                {'name': repository.name, 'stars': repository.stargazers_count}
                for repository in self.github_api.get_user(username).get_repos().get_page(page)
            ]
        except github.BadCredentialsException:
            raise BadCredentialsServiceException()
        except github.UnknownObjectException:
            raise UserNotFoundServiceException()
        except github.RateLimitExceededException:
            raise ApiRateLimitExceededServiceException()
        except github.GithubException as e:
            if e.status == 422:
                # Catch unprocessable entity errors from api and propagate
                # further e.g pagination page exceeded limit.
                raise UnprocessableEntityServiceException(e.data.get('message'))
            else:
                raise e

        return repositories

    def get_user_stars(self, username: str) -> int:
        """
        For a given username, return sum of stars of
        this user's repositories.

        Args:
            username(str): user, whose repositories' sum of stars
                will be returned.

        Returns:
            `int`: sum of stars in all user's repositories.

        Raises:
            `BadCredentialsServiceException`: when bad token is provided.
            `UserNotFoundServiceException`: when desired user is not found.
            `ApiRateLimitExceededServiceException`: when api calls limit was
                exceeded for given token.
        """

        result = 0
        try:
            for repository in self.github_api.get_user(username).get_repos():
                result += repository.stargazers_count
        except github.BadCredentialsException:
            raise BadCredentialsServiceException
        except github.UnknownObjectException:
            raise UserNotFoundServiceException
        except github.RateLimitExceededException:
            raise ApiRateLimitExceededServiceException

        return result
