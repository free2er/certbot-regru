"""Tests for certbot_regru.dns."""

import os
import unittest

import json
import mock
import requests

from certbot import errors
from certbot.plugins import dns_test_common
from certbot.plugins.dns_test_common import DOMAIN
from certbot.tests import util as test_util

USERNAME = 'foo'
PASSWORD = 'bar'

HTTP_ERROR = requests.exceptions.RequestException()


class AuthenticatorTest(test_util.TempDirTestCase, dns_test_common.BaseAuthenticatorTest):

    def setUp(self):
        from certbot_regru.dns import Authenticator

        super(AuthenticatorTest, self).setUp()

        path = os.path.join(self.tempdir, 'file.ini')
        dns_test_common.write({"regru_username": USERNAME, "regru_password": PASSWORD}, path)

        self.config = mock.MagicMock(regru_credentials=path, regru_propagation_seconds=0)  # don't wait during tests

        self.auth = Authenticator(self.config, "regru")

        self.mock_client = mock.MagicMock()
        # _get_regru_client | pylint: disable=protected-access
        self.auth._get_regru_client = mock.MagicMock(return_value=self.mock_client)

    def test_perform(self):
        self.auth.perform([self.achall])

        expected = [mock.call.add_txt_record('_acme-challenge.' + DOMAIN, mock.ANY)]
        self.assertEqual(expected, self.mock_client.mock_calls)

    def test_cleanup(self):
        # _attempt_cleanup | pylint: disable=protected-access
        self.auth._attempt_cleanup = True
        self.auth.cleanup([self.achall])

        expected = [mock.call.del_txt_record('_acme-challenge.' + DOMAIN, mock.ANY)]
        self.assertEqual(expected, self.mock_client.mock_calls)


class RegRuClientTest(unittest.TestCase):

    record_prefix = "_acme-challenge"
    record_name = record_prefix + "." + DOMAIN
    record_content = "test"

    def setUp(self):
        from certbot_regru.dns import _RegRuClient

        self.client = _RegRuClient(USERNAME, PASSWORD)

        self.http = mock.MagicMock()
        self.client.http = self.http

    def test_add_txt_record(self):
        self.http.send.return_value = {'result': 'success'}
        self.client.add_txt_record(self.record_name, self.record_content)

        self.http.send.assert_called_with('https://api.reg.ru/api/regru2/zone/add_txt', {
            'username': USERNAME,
            'password': PASSWORD,
            'io_encoding': 'utf8',
            'show_input_params': 1,
            'output_format': 'json',
            'input_format': 'json',
            'input_data': json.dumps({
                'text': self.record_content,
                'subdomain': self.record_prefix,
                'domains': [{'dname': DOMAIN}]
            })
        })

    def test_add_txt_record_subdomain(self):
        self.http.send.return_value = {'result': 'success'}
        self.client.add_txt_record(self.record_prefix + '.subdomain.' + DOMAIN, self.record_content)

        self.http.send.assert_called_with('https://api.reg.ru/api/regru2/zone/add_txt', {
            'username': USERNAME,
            'password': PASSWORD,
            'io_encoding': 'utf8',
            'show_input_params': 1,
            'output_format': 'json',
            'input_format': 'json',
            'input_data': json.dumps({
                'text': self.record_content,
                'subdomain': self.record_prefix + '.subdomain',
                'domains': [{'dname': DOMAIN}]
            })
        })

    def test_add_txt_record_error_failed_result(self):
        self.http.send.return_value = {'result': 'failed'}
        self.assertRaises(errors.PluginError, self.client.add_txt_record, self.record_name, self.record_content)

    def test_add_txt_record_error_no_result(self):
        self.http.send.return_value = {}
        self.assertRaises(errors.PluginError, self.client.add_txt_record, self.record_name, self.record_content)

    def test_add_txt_record_error_send_request(self):
        self.http.send.side_effect = HTTP_ERROR
        self.assertRaises(errors.PluginError, self.client.add_txt_record, self.record_name, self.record_content)

    def test_del_txt_record(self):
        self.http.send.return_value = {'result': 'success'}
        self.client.del_txt_record(self.record_name, self.record_content)

        self.http.send.assert_called_with('https://api.reg.ru/api/regru2/zone/remove_record', {
            'username': USERNAME,
            'password': PASSWORD,
            'io_encoding': 'utf8',
            'show_input_params': 1,
            'output_format': 'json',
            'input_format': 'json',
            'input_data': json.dumps({
                'record_type': 'TXT',
                'content': self.record_content,
                'subdomain': self.record_prefix,
                'domains': [{'dname': DOMAIN}]
            })
        })

    def test_del_txt_record_subdomain(self):
        self.http.send.return_value = {'result': 'success'}
        self.client.del_txt_record(self.record_prefix + '.subdomain.' + DOMAIN, self.record_content)

        self.http.send.assert_called_with('https://api.reg.ru/api/regru2/zone/remove_record', {
            'username': USERNAME,
            'password': PASSWORD,
            'io_encoding': 'utf8',
            'show_input_params': 1,
            'output_format': 'json',
            'input_format': 'json',
            'input_data': json.dumps({
                'record_type': 'TXT',
                'content': self.record_content,
                'subdomain': self.record_prefix + '.subdomain',
                'domains': [{'dname': DOMAIN}]
            })
        })

    def test_del_txt_record_error_failed_result(self):
        self.http.send.return_value = {'result': 'failed'}
        self.client.del_txt_record(self.record_name, self.record_content)

    def test_del_txt_record_error_no_result(self):
        self.http.send.return_value = {}
        self.client.del_txt_record(self.record_name, self.record_content)

    def test_del_txt_record_error_send_request(self):
        self.http.send.side_effect = HTTP_ERROR
        self.client.del_txt_record(self.record_name, self.record_content)

if __name__ == "__main__":
    unittest.main()  # pragma: no cover
