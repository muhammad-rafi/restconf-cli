[![Build Status](https://github.com/muhammad-rafi/restconf-cli/actions/workflows/main.yaml/badge.svg)](https://github.com/muhammad-rafi/conf_diff/actions)
[![Release Status](https://github.com/muhammad-rafi/restconf-cli/actions/workflows/release.yaml/badge.svg)](https://github.com/muhammad-rafi/conf_diff/actions)
[![Pypi](https://img.shields.io/pypi/v/restconf-cli.svg)](https://pypi.org/project/restconf-cli/) 

# RESTCONF Command Line Interface (restconf-cli)

## Introduction
restconf-cli is a command line interface application which interacts with the restconf enabled devices (i.e. iosxe, nxos, nso). This module uses Python `Click` module for command line interface (CLI) and `rich` module for the colorful output. It is  built on top of Python `requests` library to make Restconf API calls. Here are the key information for this modules. 

- Base URL used 'https://<hostname/ip>:<port>/restconf/data/'
- Default port used for the Restconf API 443
- Default Headers used for Accept and Content-Type are the following.

Accept: application/yang-data+json
Content-Type: application/yang-data+json

Since default headers are using 'application/yang-data+json', therefore, the output will be in following formats for the below type of devices unless specified in the table below.
  
  | Device Type                    | IOSXE  | NXOS  |  NSO  |
  | :----------------------------: | :----: | :---: | :---: |
  | Default Accept  Header          |  application/yang-data+json  |  application/yang-data+json  | application/yang-data+json  |
  | Default Content-Type Header     |  application/yang-data+json  |  application/yang-data+json  | application/yang-data+json  |
  | Default Output Format          |  JSON  |  XML  | JSON  |
  
Same for the POST, PUT and PATCH operations, if you do not specify the header fields, it assumes that you are sending the data in the formats mentioned above.
  
- Currently tested/supported on Python 3.8, 3.9 and 3.10 

__Disclaimer:__ This module uses Insecure Requests which is not recommended, use
certificates where possible.

## Installation
You can download this module from PyPi repository via PIP

To install a module, simply type

```bash
pip install restconf-cli
```

__Note:__ It is also recommended that use the virtual environment for any package you are testing. 

```bash
(main) expert@expert-cws:~/venvs$ python -m venv .venv
(main) expert@expert-cws:~/venvs$ source .venv/bin/activate
(.venv) expert@expert-cws:~/venvs$ pip install restconf-cli 
```

## Usage
Once you have installed the `restconf-cli` package, you can test this against any Cisco IOSXE, NXOS and NSO device. I have not tested for any other devices, but if you come across any device where this is working or not, feel free to raise an issue or send a pull request. 

Let's first explore the documentation 

Run `restconf-cli --help` on the terminal for help text 

```bash
(.venv) expert@expert-cws:~$ restconf-cli --help
Usage: restconf-cli [OPTIONS] COMMAND [ARGS]...

  CLI tool to interact with the restconf APIs currently supported for IOSXE,
  NXOS and NSO.

  This library uses the following root URL for the restconf with port 443 as default port.
  https://<hostname/ip>:<port>/restconf/data/

  Default Headers for Accept and Content-Type are the following.

  Accept: application/yang-data+json
  Content-Type: application/yang-data+json
  
  Since default headers are using 'application/yang-data+json',
  therefore, you will retrieve the output in following formats
  for the below type of devices unless specified for the GET operation.
  
    | Device Type           |            IOSXE             |              NXOS            |             NSO             |
    | :-------------------: | :--------------------------: | :--------------------------: | :-------------------------: |
    | Default Accept        |  application/yang-data+json  |  application/yang-data+json  | application/yang-data+json  |
    | Default Content-Type  |  application/yang-data+json  |  application/yang-data+json  | application/yang-data+json  |
    | Default Output Format |            JSON              |              XML             |             JSON            |
  
  Same for the POST, PUT and PATCH operation if you do not specify the
  header fields, it assumes you are sending the data in the formats
  mentioned above.
  
  Disclaimer: This module uses Insecure Requests which is not recommended, use
  certificates where possible.

Options:
  --help  Show this message and exit.

Commands:
  DELETE  Method to delete the target resource Example: $ restconf-cli...
  GET     Method to retrieve operational or config data from the devices.
  PATCH   same as PUT, except if the resource does not exist, the devices...
  POST    Sends data to the devices to create a new data resource.
  PUT     Send data to the devices to create or update the data resource.
```

You can read all the above information, but this is more or less same info which already exist in this readme file. The important key of information here, are the commands, as you can see there are about 5 commands available which are basically CRUD operation for the Restconf API. We can again `-h` or `--help` flag to see the information inside each of these commands. Let's check each of them and see what command options are available.

For GET operation command options, simply run `restconf-cli GET --help` or `restconf-cli GET -h`

```bash
(.venv) expert@expert-cws:~$ restconf-cli GET --help
Usage: restconf-cli GET [OPTIONS]

  Method to retrieve operational or config data from the devices.

  Default header for the requests are 'application/yang-data+json'

  Example:

  # Display output on the terminal 
  $ restconf-cli GET -u developer -n sandbox-iosxe-latest-1.cisco.com \ 
  -p Cisco-IOS-XE-native:native/version \ 
  -a application/yang-data+json \ 
  -c application/yang-data+json 
  
  # Display output on the terminal and save the output on a file defined with --output or -o flag 
  $ restconf-cli GET -u developer -n sandbox-iosxe-latest-1.cisco.com \ 
  -p Cisco-IOS-XE-native:native/interface \ 
  -o output.json

Options:
  -o, --output FILENAME    Output will be written to a file
  -c, --content-type TEXT  Content-Type hearder for restconf api, default is
                           application/yang-data+json

  -a, --accept TEXT        Accept hearder for restconf api, default is
                           application/yang-data+json

  -pn, --port INTEGER      Port number for restconf api, default is 443
  -p, --path TEXT          Path for restconf api call  [required]
  --password TEXT          Password for restconf api
  -u, --username TEXT      Username for restconf api  [required]
  -n, --hostname TEXT      Device hostname or IP address for the restconf API
                           [required]

  -h, --help               Show this message and exit.
```

For POST operation command options, run `restconf-cli POST --help` or `restconf-cli POST -h`

```bash
(.venv) expert@expert-cws:~$ restconf-cli POST -h
Usage: restconf-cli POST [OPTIONS]

  Sends data to the devices to create a new data resource.

  Example:
  
  # Configure via raw data for POST operation
  $ restconf-cli POST -u developer -n sandbox-iosxe-latest-1.cisco.com \ 
  -p ietf-interfaces:interfaces \ 
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
  
  # Configure from file for POST operation
  $ restconf-cli POST -u developer \ 
  -n sandbox-iosxe-latest-1.cisco.com \ 
  -p ietf-interfaces:interfaces -ff interface.json

Options:
  -ff, --from-file FILENAME  Read the playload from file for POST operation
  -d, --data TEXT            Playload to be sent for POST, PUT and PATCH
                             methods

  -c, --content-type TEXT    Content-Type hearder for restconf api, default is
                             application/yang-data+json

  -a, --accept TEXT          Accept hearder for restconf api, default is
                             application/yang-data+json

  -pn, --port INTEGER        Port number for restconf api, default is 443
  -p, --path TEXT            Path for restconf api call  [required]
  --password TEXT            Password for restconf api
  -u, --username TEXT        Username for restconf api  [required]
  -n, --hostname TEXT        Device hostname or IP address for the restconf
                             API  [required]

  -h, --help                 Show this message and exit.
```

For PUT operation command options, run `restconf-cli PUT --help` or `restconf-cli PUT -h`

```bash
(.venv) expert@expert-cws:~$ restconf-cli PUT -h
Usage: restconf-cli PUT [OPTIONS]

  Send data to the devices to create or update the data resource.

  Example:
  
  # Configure via raw data for PUT operation
  $ restconf-cli PUT -u developer -n sandbox-iosxe-latest-1.cisco.com \ 
  -p ietf-interfaces:interfaces \ 
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
  
  # Configure from file for PUT operation
  $ restconf-cli PUT -u developer \ 
  -n sandbox-iosxe-latest-1.cisco.com \ 
  -p ietf-interfaces:interfaces/interface=Loopback999 -ff interface.json

Options:
  -ff, --from-file FILENAME  Read the playload from file for PUT operation
  -d, --data TEXT            Playload to be sent for POST, PUT and PATCH
                             methods

  -c, --content-type TEXT    Content-Type hearder for restconf api, default is
                             application/yang-data+json

  -a, --accept TEXT          Accept hearder for restconf api, default is
                             application/yang-data+json

  -pn, --port INTEGER        Port number for restconf api, default is 443
  -p, --path TEXT            Path for restconf api call  [required]
  --password TEXT            Password for restconf api
  -u, --username TEXT        Username for restconf api  [required]
  -n, --hostname TEXT        Device hostname or IP address for the restconf
                             API  [required]

  -h, --help                 Show this message and exit.
```

For PATCH operation command options, run `restconf-cli PATCH --help` or `restconf-cli PATCH -h`

```bash
(.venv) expert@expert-cws:~$ restconf-cli PATCH -h
Usage: restconf-cli PATCH [OPTIONS]

  same as PUT, except if the resource does not exist, the devices MUST NOT
  create one.

  Example:
  
  # Configure via raw data for PATCH operation
  $ restconf-cli PATCH -u developer -n sandbox-iosxe-latest-1.cisco.com \ 
  -p ietf-interfaces:interfaces \ 
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
  
  # Configure from file for PATCH operation
  $ restconf-cli PATCH -u developer \ 
  -n sandbox-iosxe-latest-1.cisco.com \ 
  -p ietf-interfaces:interfaces/interface=Loopback999 -ff interface.json

Options:
  -ff, --from-file FILENAME  Read the playload from file for PATCH operation
  -d, --data TEXT            Playload to be sent for POST, PUT and PATCH
                             methods

  -c, --content-type TEXT    Content-Type hearder for restconf api, default is
                             application/yang-data+json

  -a, --accept TEXT          Accept hearder for restconf api, default is
                             application/yang-data+json

  -pn, --port INTEGER        Port number for restconf api, default is 443
  -p, --path TEXT            Path for restconf api call  [required]
  --password TEXT            Password for restconf api
  -u, --username TEXT        Username for restconf api  [required]
  -n, --hostname TEXT        Device hostname or IP address for the restconf
                             API  [required]

  -h, --help                 Show this message and exit.
```

For DELETE operation command options, run `restconf-cli DELETE --help` or `restconf-cli DELETE -h`

```bash
(.venv) expert@expert-cws:~$ restconf-cli DELETE -h
Usage: restconf-cli DELETE [OPTIONS]

  Method to delete the target resource

  Example:
  
  $ restconf-cli DELETE -u developer -n sandbox-iosxe-latest-1.cisco.com \ 
  -p ietf-interfaces:interfaces/interface=Loopback999

Options:
  -n, --hostname TEXT      Device hostname or IP address for the restconf API
                           [required]

  -u, --username TEXT      Username for restconf api  [required]
  --password TEXT          Password for restconf api
  -p, --path TEXT          Path for restconf api call  [required]
  -pn, --port INTEGER      Port number for restconf api, default is 443
  -a, --accept TEXT        Accept hearder for restconf api, default is
                           application/yang-data+json

  -c, --content-type TEXT  Content-Type hearder for restconf api, default is
                           application/yang-data+json

  -h, --help               Show this message and exit.
```

Notice there are some examples mentioned in the above output for every command, we will explore these in the next section. 

## Examples
For the sake of testing, I am going to use Cisco Always-on IOSXE device `sandbox-iosxe-latest-1.cisco.com` which uses the `443` default port for Restconf and both Accept and Content-type headers are `application/yang-data+json`, which makes our CLI command earsier as these options are default for `restconf-cli`.

```
restconf-cli GET -u developer -n sandbox-iosxe-latest-1.cisco.com -p Cisco-IOS-XE-native:native/version
```

```bash
(.venv) expert@expert-cws:~$ restconf-cli GET -u developer -n sandbox-iosxe-latest-1.cisco.com -p Cisco-IOS-XE-native:native/version
Password: 
{
  "Cisco-IOS-XE-native:version": "17.3"
}


Status: 200 OK

```
The output will be colorful as `restconf-cli` cli uses the rich module to print colorful output.

For more examples, please check the [examples](examples) folder. 

## Issues
Please raise an issue or pull request if you find something wrong with this module.

## Authors
[Muhammad Rafi](https://www.linkedin.com/in/muhammad-rafi-0a37a248/)

## References
https://click.palletsprojects.com/en/8.1.x/

https://click.palletsprojects.com/en/7.x/changelog/#version-7-1-2
