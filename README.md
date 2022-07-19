# RESTCONF Command Line Interface

## Introduction
restconf-cli is a command line interface application which interacts with the restconf enabled devices (i.e. iosxe, nxos, nso). This module uses Python `Click` module and built on top of Python `requests` library. Here are the key information for this modules. 

- Base URL used 'https://<hostname/ip>:<port>/restconf/data/'
- Default port used for the Restconf API 443
- Default Headers used for Accept and Content-Type are the following.

Accept: application/yang-data+json

Content-Type: application/yang-data+json

Since default headers are using 'application/yang-data+json', therefore, the output will be in following formats for the below type of devices unless specified in the table below.
  
  | Device Type             | IOSXE  | NXOS  |  NSO  |
  | :---------------------: | :----: | :---: | :---: |
  | Default Output Format   |  JSON  |  XML  | JSON  |
  | Defaul Content-Type     |  JSON  |  XML  | JSON  |
  
Same for the POST, PUT and PATCH operations, if you do not specify the header fields, it assumes that you are sending the data in the formats mentioned above.
  
- Currently tested/supported on Python 3.9 and 3.10 

__Disclaimer:__ This module uses Insecure Requests which is not recommended, use
certificates where possible.

## Installation

You can download this module from PyPi repository via PIP
To install a module, simply type:
```bash
pip install restconf-cli
```

Note: It is also recommended that use the virtual environment for any package you are testing. 

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install restconf-cli
```

## Usage

Once you have installed the `restconf-cli` package, you can test this against any Cisco IOSXE, NXOS and NSO device. I have not tested any other devices, but if you come across any other devices where this is working or not, feel free to raise an issue or send a pull request. 

For the sake of testing, I am going to use Cisco Always-on IOSXE device `sandbox-iosxe-latest-1.cisco.com` which uses the `443` default port for Restconf and both Accept and Content-type headers are `application/yang-data+json`, which makes our CLI command earsier. 

$ restconf-cli GET -u developer -n sandbox-iosxe-latest-1.cisco.com -p Cisco-IOS-XE-native:native/interface





