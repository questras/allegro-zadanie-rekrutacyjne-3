"""
Module with tests related to `repositories_app.services.GithubApiService`.
"""

from unittest import mock, TestCase
from collections import namedtuple

import github

from repositories_app.services import GithubApiService
from repositories_app.exceptions import (
    UserNotFoundServiceException,
    ApiRateLimitExceededServiceException,
    BadCredentialsServiceException,
    UnprocessableEntityServiceException
)

Repository = namedtuple('Repository', ['name', 'stargazers_count'])
test_data = [Repository('repo1', 1),
             Repository('repo2', 22),
             Repository('repo3', 0)]


class GetUserRepositoriesTests(TestCase):
    """
    Tests for `GithubApiService.get_user_repositories` method.
    """

    def setUp(self) -> None:
        self.data = test_data

    @mock.patch('repositories_app.services.github.Github')
    def test_returns_correct_data(self, service_mock):
        service_mock.return_value.get_user.return_value.get_repos. \
            return_value.get_page.return_value = self.data

        want = [
            {'name': 'repo1', 'stars': 1},
            {'name': 'repo2', 'stars': 22},
            {'name': 'repo3', 'stars': 0}
        ]
        got = GithubApiService('test-token').get_user_repositories('test')

        self.assertEqual(want, got)

    @mock.patch('repositories_app.services.github.Github')
    def test_empty_data_returns_empty_list(self, service_mock):
        service_mock.return_value.get_user.return_value.get_repos. \
            return_value.get_page.return_value = []

        want = []
        got = GithubApiService('test-token').get_user_repositories('test')

        self.assertEqual(want, got)

    @mock.patch('repositories_app.services.github.Github')
    def test_no_user_found_raises_correct_exception(self, service_mock):
        def exception_side_effect(_):
            raise github.UnknownObjectException('test', 'test')

        service_mock.return_value.get_user.side_effect = exception_side_effect

        with self.assertRaises(UserNotFoundServiceException):
            GithubApiService('test-token').get_user_repositories('test')

    @mock.patch('repositories_app.services.github.Github')
    def test_bad_credentials_raises_correct_exception(self, service_mock):
        def exception_side_effect(_):
            raise github.BadCredentialsException('test', 'test')

        service_mock.return_value.get_user.side_effect = exception_side_effect

        with self.assertRaises(BadCredentialsServiceException):
            GithubApiService('test-token').get_user_repositories('test')

    @mock.patch('repositories_app.services.github.Github')
    def test_api_rate_exceeded_raises_correct_exception(self, service_mock):
        def exception_side_effect(_):
            raise github.RateLimitExceededException('test', 'test')

        service_mock.return_value.get_user.side_effect = exception_side_effect

        with self.assertRaises(ApiRateLimitExceededServiceException):
            GithubApiService('test-token').get_user_repositories('test')

    @mock.patch('repositories_app.services.github.Github')
    def test_unprocessable_entity_http_error_raises_correct_exception(self, service_mock):
        def exception_side_effect(_):
            # Error received from github api indicating that response
            # status code was 422: Unprocessable Entity.
            raise github.GithubException(422, {'message': 'test'})

        service_mock.return_value.get_user.side_effect = exception_side_effect

        with self.assertRaises(UnprocessableEntityServiceException):
            GithubApiService('test-token').get_user_repositories('test')

    @mock.patch('repositories_app.services.github.Github')
    def test_unhandled_exception_is_propagated(self, service_mock):
        def exception_side_effect(_):
            raise github.GithubException('unhandled', {'message': 'unhandled'})

        service_mock.return_value.get_user.side_effect = exception_side_effect

        with self.assertRaises(github.GithubException):
            GithubApiService('test-token').get_user_repositories('test')


class GetUserStarsTests(TestCase):
    """
    Tests for `GithubApiService.get_user_stars` method.
    """

    def setUp(self) -> None:
        self.data = test_data

    @mock.patch('repositories_app.services.github.Github')
    def test_returns_correct_data(self, service_mock):
        service_mock.return_value.get_user.return_value. \
            get_repos.return_value = self.data

        want = 23
        got = GithubApiService('test-token').get_user_stars('test')

        self.assertEqual(want, got)

    @mock.patch('repositories_app.services.github.Github')
    def test_empty_data_returns_zero(self, service_mock):
        service_mock.return_value.get_user.return_value. \
            get_repos.return_value = []

        want = 0
        got = GithubApiService('test-token').get_user_stars('test')

        self.assertEqual(want, got)

    @mock.patch('repositories_app.services.github.Github')
    def test_no_user_found_raises_correct_exception(self, service_mock):
        def exception_side_effect(_):
            raise github.UnknownObjectException('test', 'test')

        service_mock.return_value.get_user.side_effect = exception_side_effect

        with self.assertRaises(UserNotFoundServiceException):
            GithubApiService('test-token').get_user_stars('test')

    @mock.patch('repositories_app.services.github.Github')
    def test_bad_credentials_raises_correct_exception(self, service_mock):
        def exception_side_effect(_):
            raise github.BadCredentialsException('test', 'test')

        service_mock.return_value.get_user.side_effect = exception_side_effect

        with self.assertRaises(BadCredentialsServiceException):
            GithubApiService('test-token').get_user_stars('test')

    @mock.patch('repositories_app.services.github.Github')
    def test_api_rate_exceeded_raises_correct_exception(self, service_mock):
        def exception_side_effect(_):
            raise github.RateLimitExceededException('test', 'test')

        service_mock.return_value.get_user.side_effect = exception_side_effect

        with self.assertRaises(ApiRateLimitExceededServiceException):
            GithubApiService('test-token').get_user_stars('test')
