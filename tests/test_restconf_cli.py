#!/usr/bin/env python

from click.testing import CliRunner
import unittest
import requests
from restconf_cli import restconf_cli


# Disable InsecureRequestWarning: Unverified HTTPS request is being made.
requests.packages.urllib3.disable_warnings()
password = 'C1sco12345'


class RestconfCliRestconfGetTests(unittest.TestCase):

    def test_a_restconf_get(self):
        runner = CliRunner()
        result = runner.invoke(restconf_cli,
                               ['GET',
                                '--username', 'developer',
                                '--hostname', 'sandbox-iosxe-latest-1.cisco.com',
                                '--path', 'Cisco-IOS-XE-native:native/version',
                                ], input=f'{password}\n')

        print(result.output)
        # breakpoint()
        # assert result.exit_code == 0
        assert not result.exception
        assert 'Request Failed' not in result.output
        self.assertTrue(result.exit_code == 0)
        # self.assertEqual(result.exit_code, 0)

    def test_b_restconf_post(self):
        runner = CliRunner()
        result = runner.invoke(restconf_cli,
                               ['POST',
                                '--username', 'developer',
                                '--hostname', 'sandbox-iosxe-latest-1.cisco.com',
                                '--path', 'ietf-interfaces:interfaces',
                                '--data', '''{
                                    "interface":[
                                        {
                                            "name":"Loopback10000",
                                            "description":"created by python click - POST",
                                            "type":"iana-if-type:softwareLoopback",
                                            "enabled":true,
                                            "ietf-ip:ipv4":{
                                                "address":[
                                                {
                                                    "ip":"10.0.2.10",
                                                    "netmask":"255.255.255.255"
                                                }
                                                ]
                                            }
                                        }
                                    ]
                                    }'''
                                ], input=f'{password}\n')

        print(result.output)
        assert not result.exception
        assert 'Request Failed' not in result.output
        self.assertTrue(result.exit_code == 0)

    def test_c_restconf_put(self):
        runner = CliRunner()
        result = runner.invoke(restconf_cli,
                               ['PUT',
                                '--username', 'developer',
                                '--hostname', 'sandbox-iosxe-latest-1.cisco.com',
                                '--path', 'ietf-interfaces:interfaces/interface=Loopback10000',
                                '--data', '''{
                                    "interface":[
                                        {
                                            "name":"Loopback10000",
                                            "description":"created by python click - PUT",
                                            "type":"iana-if-type:softwareLoopback",
                                            "enabled":true,
                                            "ietf-ip:ipv4":{
                                                "address":[
                                                {
                                                    "ip":"10.0.2.10",
                                                    "netmask":"255.255.255.255"
                                                }
                                                ]
                                            }
                                        }
                                    ]
                                    }'''
                                ], input=f'{password}\n')

        print(result.output)
        assert not result.exception
        assert 'Request Failed' not in result.output
        self.assertTrue(result.exit_code == 0)

    def test_d_restconf_patch(self):
        runner = CliRunner()
        result = runner.invoke(restconf_cli,
                               ['PATCH',
                                '--username', 'developer',
                                '--hostname', 'sandbox-iosxe-latest-1.cisco.com',
                                '--path', 'ietf-interfaces:interfaces/interface=Loopback10000',
                                '--data', '''{
                                    "interface":[
                                        {
                                            "name":"Loopback10000",
                                            "description":"created by python click - PATCH",
                                            "type":"iana-if-type:softwareLoopback",
                                            "enabled":true,
                                            "ietf-ip:ipv4":{
                                                "address":[
                                                {
                                                    "ip":"10.0.2.10",
                                                    "netmask":"255.255.255.255"
                                                }
                                                ]
                                            }
                                        }
                                    ]
                                    }'''
                                ], input=f'{password}\n')

        print(result.output)
        assert not result.exception
        assert 'Request Failed' not in result.output
        self.assertTrue(result.exit_code == 0)

    def test_e_restconf_delete(self):
        runner = CliRunner()
        result = runner.invoke(restconf_cli,
                               ['DELETE',
                                '--username', 'developer',
                                '--hostname', 'sandbox-iosxe-latest-1.cisco.com',
                                '--path', 'ietf-interfaces:interfaces/interface=Loopback10000',
                                ], input=f'{password}\n')

        print(result.output)
        assert not result.exception
        assert 'Request Failed' not in result.output
        self.assertTrue(result.exit_code == 0)


if __name__ == '__main__':
    unittest.main(failfast=True)
