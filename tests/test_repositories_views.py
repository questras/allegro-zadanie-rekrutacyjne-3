"""
Module with tests related to `repositories_app.views`.
"""

from unittest import mock, TestCase

from repositories_app.app import create_app
from repositories_app.exceptions import (
    UserNotFoundServiceException,
    BadCredentialsServiceException,
    ApiRateLimitExceededServiceException,
    UnprocessableEntityServiceException
)

test_data = [
    {'name': 'repo1', 'stars': 1},
    {'name': 'repo2', 'stars': 22},
    {'name': 'repo3', 'stars': 0}
]


class UserRepositoriesViewTests(TestCase):
    """
    Tests for view `repositories_app.views.user_repositories_view`.
    """

    def setUp(self) -> None:
        self.client = create_app().test_client()
        self.data = test_data
        self.url = '/api/v1/github/repositories/test'

    @mock.patch('repositories_app.views.GithubApiService')
    def test_get_correct_data(self, service_mock):
        service_mock.return_value.get_user_repositories.return_value = self.data

        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)

        want = {
            'username': 'test',
            'repositories': self.data,
            'repositories_count': len(self.data)
        }
        got = r.json
        self.assertEqual(want, got)

    @mock.patch('repositories_app.views.GithubApiService')
    def test_empty_data_gives_result_with_empty_list(self, service_mock):
        service_mock.return_value.get_user_repositories.return_value = []

        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)

        want = {
            'username': 'test',
            'repositories': [],
            'repositories_count': 0
        }
        got = r.json
        self.assertEqual(want, got)

    @mock.patch('repositories_app.views.GithubApiService')
    def test_non_numerical_page_argument_is_ignored(self, service_mock):
        service_mock.return_value.get_user_repositories.return_value = self.data

        new_url = self.url + '?page=notanumber'
        r = self.client.get(new_url)
        self.assertEqual(r.status_code, 200)

        want = {
            'username': 'test',
            'repositories': self.data,
            'repositories_count': len(self.data)
        }
        got = r.json
        self.assertEqual(want, got)

    @mock.patch('repositories_app.views.GithubApiService')
    def test_user_not_found_returns_404(self, service_mock):
        def exception_side_effect(*args):
            raise UserNotFoundServiceException()

        service_mock.return_value. \
            get_user_repositories.side_effect = exception_side_effect

        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 404)
        self.assertEqual(r.json['message'], 'User not found')

    @mock.patch('repositories_app.views.GithubApiService')
    def test_bad_credentials_error_returns_500(self, service_mock):
        def exception_side_effect(*args):
            raise BadCredentialsServiceException()

        service_mock.return_value. \
            get_user_repositories.side_effect = exception_side_effect

        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 500)
        self.assertEqual(r.json['message'], 'Server error')

    @mock.patch('repositories_app.views.GithubApiService')
    def test_api_rate_limit_exceeded_error_returns_500(self, service_mock):
        def exception_side_effect(*args):
            raise ApiRateLimitExceededServiceException()

        service_mock.return_value. \
            get_user_repositories.side_effect = exception_side_effect

        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 500)
        self.assertEqual(r.json['message'], 'Server error')

    @mock.patch('repositories_app.views.GithubApiService')
    def test_unprocessable_entity_error_returns_422(self, service_mock):
        def exception_side_effect(*args):
            raise UnprocessableEntityServiceException('test-message')

        service_mock.return_value. \
            get_user_repositories.side_effect = exception_side_effect

        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 422)
        self.assertEqual(r.json['message'], 'test-message')
