#!/usr/bin/env python

import click
import requests
from rich import print


# Disable InsecureRequestWarning: Unverified HTTPS request is being made.
requests.packages.urllib3.disable_warnings()


# Creating click group as parent function for other click commands to be attached with
@click.group()
def restconf_cli():
    """ CLI tool to interact with the restconf APIs currently supported
    for IOSXE, NXOS and NSO.

    \b
    This library uses the following root URL for the restconf with port 443 as default port.
    https://<hostname/ip>:<port>/restconf/data/

    Default Headers for Accept and Content-Type are the following. \n
    \b
    Accept: application/yang-data+json
    Content-Type: application/yang-data+json
    \b
    Since default headers are using 'application/yang-data+json',
    therefore, you will retrieve the output in following formats
    for the below type of devices unless specified for the GET operation.
    \b
    | Device Type           |            IOSXE             |              NXOS            |             NSO             |
    | :-------------------: | :--------------------------: | :--------------------------: | :-------------------------: |
    | Default Accept        |  application/yang-data+json  |  application/yang-data+json  | application/yang-data+json  |
    | Default Content-Type  |  application/yang-data+json  |  application/yang-data+json  | application/yang-data+json  |
    | Default Output Format |            JSON              |              XML             |             JSON            |
    \b
    Same for the POST, PUT and PATCH operation if you do not specify the
    header fields, it assumes you are sending the data in the formats
    mentioned above.
    \b
    Disclaimer: This module uses Insecure Requests which is not recommended, use
    certificates where possible.
    """
    pass


# Click command 'GET'
@click.option("--hostname", "-n", type=str, required=True, help="Device hostname or IP address for the restconf API")
@click.option("--username", "-u", type=str, required=True, help="Username for restconf api")
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=False, help="Password for restconf api")
@click.option("--path", "-p", type=str, required=True, help="Path for restconf api call")
@click.option("--port", "-pn", type=int, required=False, default=443, help="Port number for restconf api, default is 443")
@click.option("--accept", "-a", type=str, required=False, default='application/yang-data+json', help="Accept hearder for restconf api, default is application/yang-data+json")
@click.option("--content-type", "-c", type=str, required=False, default='application/yang-data+json', help="Content-Type hearder for restconf api, default is application/yang-data+json")
@click.option("--output", "-o", type=click.File('w'), required=False, default=None, help="Output will be written to a file")
@click.command(name="GET", context_settings=dict(help_option_names=['-h', '--help']))
def restconf_get(hostname, username, password, path, port, accept, content_type, output):
    """
    Method to retrieve operational or config data from the devices. \n
    Default header for the requests are 'application/yang-data+json'

    Examples:\n
    \b
    # Display output on the terminal \b
    $ restconf-cli GET -u developer -n sandbox-iosxe-latest-1.cisco.com \ \b
    -p Cisco-IOS-XE-native:native/version \ \b
    -a application/yang-data+json \ \b
    -c application/yang-data+json \b
    \b
    # Display output on the terminal and save the output on a file defined with --output or -o flag \b
    $ restconf-cli GET -u developer -n sandbox-iosxe-latest-1.cisco.com \ \b
    -p Cisco-IOS-XE-native:native/interface \ \b
    -o interfaces.json
    """
    try:
        headers = {'Accept': accept, 'Content-Type': content_type}

        url = f"https://{hostname}:{port}/restconf/data/{path}"

        response = requests.get(url,
                                auth=(username, password),
                                headers=headers,
                                verify=False)
        if response.status_code == 200:
            click.echo(print(f'{response.text}'))
            if output:
                click.echo(f'{response.text}', file=output)
        else:
            click.echo(print(f"\nRequest Failed: {response}"))

    except requests.RequestException as e:
        click.echo(print(e))


# Click command 'POST'
@click.option("--hostname", "-n", type=str, required=True, help="Device hostname or IP address for the restconf API")
@click.option("--username", "-u", type=str, required=True, help="Username for restconf api")
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=False, help="Password for restconf api")
@click.option("--path", "-p", type=str, required=True, help="Path for restconf api call")
@click.option("--port", "-pn", type=int, required=False, default=443, help="Port number for restconf api, default is 443")
@click.option("--accept", "-a", type=str, required=False, default='application/yang-data+json', help="Accept hearder for restconf api, default is application/yang-data+json")
@click.option("--content-type", "-c", type=str, required=False, default='application/yang-data+json', help="Content-Type hearder for restconf api, default is application/yang-data+json")
@click.option("--data", "-d", type=str, default='', help="Playload to be sent for POST, PUT and PATCH methods")
@click.option("--from-file", "-ff", type=click.File('r'), required=False, default=None, help="Read the playload from file for POST operation")
@click.command(name="POST", context_settings=dict(help_option_names=['-h', '--help']))
def restconf_post(hostname, username, password, path, port, data, from_file, accept, content_type):
    '''
    Sends data to the devices to create a new data resource.\n

    \b
    Example:
    \b
    # Configure via raw data for POST operation
    $ restconf-cli POST -u developer -n sandbox-iosxe-latest-1.cisco.com \ \b
    -p ietf-interfaces:interfaces \ \b
    -d '{
    "interface":[
        {
            "name":"Loopback999",
            "description":"created by python click - POST",
            "type":"iana-if-type:softwareLoopback",
            "enabled":true,
            "ietf-ip:ipv4":{
                "address":[
                {
                    "ip":"10.0.1.10",
                    "netmask":"255.255.255.255"
                }
              ]
            }
          }
        ]
      }'
    \b
    # Configure from file for POST operation
    $ restconf-cli POST -u developer \ \b
    -n sandbox-iosxe-latest-1.cisco.com \ \b
    -p ietf-interfaces:interfaces -ff interface.json
    '''
    try:
        headers = {'Accept': accept, 'Content-Type': content_type}

        url = f"https://{hostname}:{port}/restconf/data/{path}"

        if from_file:
            payload = from_file.read()
        else:
            payload = data

        response = requests.post(url,
                                 auth=(username, password),
                                 headers=headers,
                                 data=payload,
                                 verify=False)
        if (response.status_code == 201):
            click.echo(print(f"\nPost operational has been successful: {response.status_code} OK"))
        else:
            click.echo(print(f"\nRequest Failed: {response}"))

    except requests.RequestException as e:
        click.echo(print(e))


# Click command 'PUT'
@click.option("--hostname", "-n", type=str, required=True, help="Device hostname or IP address for the restconf API")
@click.option("--username", "-u", type=str, required=True, help="Username for restconf api")
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=False, help="Password for restconf api")
@click.option("--path", "-p", type=str, required=True, help="Path for restconf api call")
@click.option("--port", "-pn", type=int, required=False, default=443, help="Port number for restconf api, default is 443")
@click.option("--accept", "-a", type=str, required=False, default='application/yang-data+json', help="Accept hearder for restconf api, default is application/yang-data+json")
@click.option("--content-type", "-c", type=str, required=False, default='application/yang-data+json', help="Content-Type hearder for restconf api, default is application/yang-data+json")
@click.option("--data", "-d", type=str, default='', help="Playload to be sent for POST, PUT and PATCH methods")
@click.option("--from-file", "-ff", type=click.File('r'), required=False, default=None, help="Read the playload from file for PUT operation")
@click.command(name="PUT", context_settings=dict(help_option_names=['-h', '--help']))
def restconf_put(hostname, username, password, path, port, data, from_file, accept, content_type):
    '''
    Send data to the devices to create or update the data resource.

    \b
    Example:
    \b
    # Configure via raw data for PUT operation
    $ restconf-cli PUT -u developer -n sandbox-iosxe-latest-1.cisco.com \ \b
    -p ietf-interfaces:interfaces \ \b
    -d '{
    "interface":[
        {
            "name":"Loopback999",
            "description":"created by python click - PUT",
            "type":"iana-if-type:softwareLoopback",
            "enabled":true,
            "ietf-ip:ipv4":{
                "address":[
                {
                    "ip":"10.0.1.10",
                    "netmask":"255.255.255.255"
                }
              ]
            }
          }
        ]
      }'
    \b
    # Configure from file for PUT operation
    $ restconf-cli PUT -u developer \ \b
    -n sandbox-iosxe-latest-1.cisco.com \ \b
    -p ietf-interfaces:interfaces/interface=Loopback999 -ff interface.json
    '''
    try:
        headers = {'Accept': accept, 'Content-Type': content_type}

        url = f"https://{hostname}:{port}/restconf/data/{path}"

        if from_file:
            payload = from_file.read()
        else:
            payload = data

        response = requests.put(url,
                                 auth=(username, password),
                                 headers=headers,
                                 data=payload,
                                 verify=False)
        if (response.status_code == 204):
            click.echo(print(f"\nResource has been created/updated successfully: {response.status_code} OK"))
        else:
            click.echo(print(f"\nRequest Failed: {response}"))

    except requests.RequestException as e:
        click.echo(print(e))


# Click command 'PATCH'
@click.option("--hostname", "-n", type=str, required=True, help="Device hostname or IP address for the restconf API")
@click.option("--username", "-u", type=str, required=True, help="Username for restconf api")
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=False, help="Password for restconf api")
@click.option("--path", "-p", type=str, required=True, help="Path for restconf api call")
@click.option("--port", "-pn", type=int, required=False, default=443, help="Port number for restconf api, default is 443")
@click.option("--accept", "-a", type=str, required=False, default='application/yang-data+json', help="Accept hearder for restconf api, default is application/yang-data+json")
@click.option("--content-type", "-c", type=str, required=False, default='application/yang-data+json', help="Content-Type hearder for restconf api, default is application/yang-data+json")
@click.option("--data", "-d", type=str, default='', help="Playload to be sent for POST, PUT and PATCH methods")
@click.option("--from-file", "-ff", type=click.File('r'), required=False, default=None, help="Read the playload from file for PATCH operation")
@click.command(name="PATCH", context_settings=dict(help_option_names=['-h', '--help']))
def restconf_patch(hostname, username, password, path, port, data, from_file, accept, content_type):
    '''
    same as PUT, except if the resource does not exist,
    the devices MUST NOT create one.

    \b
    Example:
    \b
    # Configure via raw data for PATCH operation
    $ restconf-cli PATCH -u developer -n sandbox-iosxe-latest-1.cisco.com \ \b
    -p ietf-interfaces:interfaces \ \b
    -d '{
    "interface":[
        {
            "name":"Loopback999",
            "description":"created by python click - PATCH",
            "type":"iana-if-type:softwareLoopback",
            "enabled":true,
            "ietf-ip:ipv4":{
                "address":[
                {
                    "ip":"10.0.1.10",
                    "netmask":"255.255.255.255"
                }
              ]
            }
          }
        ]
      }'
    \b
    # Configure from file for PATCH operation
    $ restconf-cli PATCH -u developer \ \b
    -n sandbox-iosxe-latest-1.cisco.com \ \b
    -p ietf-interfaces:interfaces/interface=Loopback999 -ff interface.json
    '''
    try:
        headers = {'Accept': accept, 'Content-Type': content_type}

        url = f"https://{hostname}:{port}/restconf/data/{path}"

        if from_file:
            payload = from_file.read()
        else:
            payload = data

        response = requests.patch(url,
                                 auth=(username, password),
                                 headers=headers,
                                 data=payload,
                                 verify=False)
        if (response.status_code == 204):
            click.echo(print(f"\nResource has been updated successfully: {response.status_code} OK"))
        else:
            click.echo(print(f"\nRequest Failed: {response}"))

    except requests.RequestException as e:
        click.echo(print(e))


# Click command 'DELETE'
@click.command(name="DELETE", context_settings=dict(help_option_names=['-h', '--help']))
@click.option("--hostname", "-n", type=str, required=True, help="Device hostname or IP address for the restconf API")
@click.option("--username", "-u", type=str, required=True, help="Username for restconf api")
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=False, help="Password for restconf api")
@click.option("--path", "-p", type=str, required=True, help="Path for restconf api call")
@click.option("--port", "-pn", type=int, required=False, default=443, help="Port number for restconf api, default is 443")
@click.option("--accept", "-a", type=str, required=False, default='application/yang-data+json', help="Accept hearder for restconf api, default is application/yang-data+json")
@click.option("--content-type", "-c", type=str, required=False, default='application/yang-data+json', help="Content-Type hearder for restconf api, default is application/yang-data+json")
def restconf_delete(hostname, username, password, path, port, accept, content_type):
    '''
    Method to delete the target resource

    \b
    Example:
    \b
    $ restconf-cli DELETE -u developer -n sandbox-iosxe-latest-1.cisco.com \ \b
    -p ietf-interfaces:interfaces/interface=Loopback999
    '''
    try:
        headers = {'Accept': accept, 'Content-Type': content_type}

        url = f"https://{hostname}:{port}/restconf/data/{path}"

        response = requests.delete(url,
                                auth=(username, password),
                                headers=headers,
                                verify=False)
        if response.status_code == 204:
            click.echo(print(f"\nResource has been deleted: {response.status_code} OK"))
        else:
            click.echo(print(f"\nRequest Failed: {response}"))

    except requests.RequestException as e:
        click.echo(print(e))


# attach child commands to the parent function
restconf_cli.add_command(restconf_get)
restconf_cli.add_command(restconf_post)
restconf_cli.add_command(restconf_put)
restconf_cli.add_command(restconf_patch)
restconf_cli.add_command(restconf_delete)

if __name__ == '__main__':
    restconf_cli()
