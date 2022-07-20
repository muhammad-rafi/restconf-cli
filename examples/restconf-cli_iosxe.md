#### Task description 
In this example, we will be configuring the `loopback interface 10000`, first we will see what interfaces are available on the device via GET command and save the output on a file in the current directory, then make some change in to that file to create a new loopback interface via POST method. 

Once the loopback 10000 is created we will change the description twice to see how PUT and PATCH commands come into the play. 

Finally, we will remove the delete the interface by using the DELETE command as it always good to clean up after the exercise. 

I am going to be using the Cisco Always-on IOSXE Sandbox (sandbox-iosxe-latest-1.cisco.com) as this publicly available and you can run through the same example. See this [link](https://devnetsandbox.cisco.com/RM/Diagram/Index/7b4d4209-a17c-4bc3-9b38-f15184e53a94?diagramType=Topology) for the IOSXE Sandbox information. 

__Note__: As RESTCONF uses structured data (XML or JSON) and YANG to provide a REST-like APIs, enabling you to programmatically access different network devices. RESTCONF APIs use HTTPs methods. YANG—A data modelling language that is used to model configuration and operational features. I am assuming you are familiar with the YANG Data Models as this is out of scope for this example.

Let's pull the current interface configured on the device. 

$ restconf-cli GET -u developer -n sandbox-iosxe-latest-1.cisco.com -p Cisco-IOS-XE-native:native/interface

```bash
(.venv) expert@expert-cws:~$ restconf-cli GET -u developer -n sandbox-iosxe-latest-1.cisco.com -p Cisco-IOS-XE-native:native/interface
Password: 
{
  "Cisco-IOS-XE-native:interface": {
    "GigabitEthernet": [
      {
        "name": "1",
        "description": "MANAGEMENT INTERFACE - DON'T TOUCH ME",
        "ip": {
          "address": {
            "primary": {
              "address": "10.10.20.48",
              "mask": "255.255.255.0"
            }
          }
        },
        "mop": {
          "enabled": false,
          "sysid": false
        },
        "Cisco-IOS-XE-ethernet:negotiation": {
          "auto": true
        }
      },
      {
        "name": "2",
        "description": "Network Interface",
        "shutdown": ,
        "mpls": {
          "Cisco-IOS-XE-mpls:ip": 
        },
        "mop": {
          "enabled": false,
          "sysid": false
        },
        "Cisco-IOS-XE-ethernet:negotiation": {
          "auto": true
        }
      },
      {
        "name": "3",
        "description": "Network Interface",
        "shutdown": ,
        "mop": {
          "enabled": false,
          "sysid": false
        },
        "Cisco-IOS-XE-ethernet:negotiation": {
          "auto": true
        }
      }
    ],
    "Loopback": [
      {
        "name": 1,
        "description": "del test",
        "ip": {
          "address": {
            "primary": {
              "address": "1.9.9.9",
              "mask": "255.255.255.255"
            }
          }
        }
      },
      {
        "name": 2,
        "description": "del test",
        "ip": {
          "address": {
            "primary": {
              "address": "2.9.9.9",
              "mask": "255.255.255.0"
            }
          }
        }
      }
    ]
  }
}


(.venv) expert@expert-cws:~$ 
```

As you can see there two interfaces available on the device, check the list object `Loopback[]` above. 

We wil now pull the loopback1 configuration and save it on a file `loopback-interface.json` with `-o` or `--output` option. 

$ restconf-cli GET -u developer -n sandbox-iosxe-latest-1.cisco.com -p ietf-interfaces:interfaces/interface=Loopback1 -o loopback-interface.json

```bash
(.venv) expert@expert-cws:~$ restconf-cli GET -u developer -n sandbox-iosxe-latest-1.cisco.com -p ietf-interfaces:interfaces/interface=Loopback1 -o loopback-interface.json
Password: 
{
  "ietf-interfaces:interface": {
    "name": "Loopback1",
    "description": "del test",
    "type": "iana-if-type:softwareLoopback",
    "enabled": true,
    "ietf-ip:ipv4": {
      "address": [
        {
          "ip": "1.9.9.9",
          "netmask": "255.255.255.255"
        }
      ]
    },
    "ietf-ip:ipv6": {
    }
  }
}


(.venv) expert@expert-cws:~$ ls -l | grep loopback
-rw-rw-r-- 1 expert expert  334 Jul 20 15:26 loopback-interface.json
(.venv) expert@expert-cws:~$ 
```
As you can see the file `loopback-interface.json` is available in the current directory, lets open a file and make some change for our new `loopback interface 10000`. in the above output for Loopback1 interaface, we will change `name`, `description` and `ip` which should be enough to create new loopback interface. 

You can use your favourite editor, I am using `vi`

```
(.venv) expert@expert-cws:~$ vi loopback-interface.json
{
  "ietf-interfaces:interface": {
    "name": "Loopback10000",
    "description": "created by restconf-cli with POST command",
    "type": "iana-if-type:softwareLoopback",
    "enabled": true,
    "ietf-ip:ipv4": {
      "address": [
        {
          "ip": "10.100.1.1",
          "netmask": "255.255.255.255"
        }
      ]
    },
    "ietf-ip:ipv6": {
    }
  }
}
```
Once you updated the file with required changes, save and close `:wq` if you are using `vi`.

Now lets configure new `loopback interface 10000` with the file using `-ff` or `--from-file` flag we have updated. 

$ restconf-cli POST -u developer -n sandbox-iosxe-latest-1.cisco.com -p  ietf-interfaces:interfaces -ff loopback-interface.json

```bash
(.venv) expert@expert-cws:~$ restconf-cli POST -u developer -n sandbox-iosxe-latest-1.cisco.com -p  ietf-interfaces:interfaces -ff loopback-interface.json
Password: 

Post operational has been successful: 201 OK

(.venv) expert@expert-cws:~$ 
```

You can see we have `201 OK` success message back from the API, which means we successfully created new loopback interface, if you do not trust lets verify it via GET command. 

```bash
(.venv) expert@expert-cws:~$ restconf-cli GET -u developer -n sandbox-iosxe-latest-1.cisco.com -p ietf-interfaces:interfaces/interface=Loopback10000
Password: 
{
  "ietf-interfaces:interface": {
    "name": "Loopback10000",
    "description": "created by restconf-cli with POST command",
    "type": "iana-if-type:softwareLoopback",
    "enabled": true,
    "ietf-ip:ipv4": {
      "address": [
        {
          "ip": "10.100.1.1",
          "netmask": "255.255.255.255"
        }
      ]
    },
    "ietf-ip:ipv6": {
    }
  }
}


(.venv) expert@expert-cws:~$ 
```

There you go, you have successfully created new loopback inteface by running couple of commands on the terminal. 

Now, lets update the description in the file and run the PUT or PATCH command to update the description. PUT and PATCH commands do the same fucntion except, PATCH will not create a resource if it doesn't exist. 

I have edited `loopback-interface.json` behind the scene with new description `"description": "updated by restconf-cli with PUT command"`. Now lets run the PUT command with `-ff` or `--from-file`. 

$ restconf-cli PUT -u developer -n sandbox-iosxe-latest-1.cisco.com -p  ietf-interfaces:interfaces/interface=Loopback10000 -ff loopback-interface.json
```bash
(.venv) expert@expert-cws:~$ restconf-cli PUT -u developer -n sandbox-iosxe-latest-1.cisco.com -p  ietf-interfaces:interfaces/interface=Loopback10000 -ff loopback-interface.json
Password: 

Resource has been created/updated successfully: 204 OK

(.venv) expert@expert-cws:~$ 
```

Let's verify the change again via GET command 

$ restconf-cli GET -u developer -n sandbox-iosxe-latest-1.cisco.com -p ietf-interfaces:interfaces/interface=Loopback10000

```
(.venv) expert@expert-cws:~$ restconf-cli GET -u developer -n sandbox-iosxe-latest-1.cisco.com -p ietf-interfaces:interfaces/interface=Loopback10000
Password: 
{
  "ietf-interfaces:interface": {
    "name": "Loopback10000",
    "description": "updated by restconf-cli with PUT command",
    "type": "iana-if-type:softwareLoopback",
    "enabled": true,
    "ietf-ip:ipv4": {
      "address": [
        {
          "ip": "10.100.1.1",
          "netmask": "255.255.255.255"
        }
      ]
    },
    "ietf-ip:ipv6": {
    }
  }
}


(.venv) expert@expert-cws:~$ 
```

Sweet, we have not updated the description successfully :). you can see the description has been changed. 

One thing I wanted to point out the when we did POST command, we had a different URI and for PUT and PATCH we use different, because we should know the target resource URI for PUT, PATCH and DELETE operations. 

Lets finally delete the `loopback interface 10000` by using the DELETE command.

$ restconf-cli DELETE -u developer -n sandbox-iosxe-latest-1.cisco.com -p ietf-interfaces:interfaces/interface=Loopback10000

```bash
(.venv) expert@expert-cws:~$ restconf-cli DELETE -u developer -n sandbox-iosxe-latest-1.cisco.com -p ietf-interfaces:interfaces/interface=Loopback10000
Password: 

Resource has been deleted: 204 OK

(.venv) expert@expert-cws:~$ 
```

All done! we successfully deleted the interface. 

In the above example, you can I have been using `--from-file` option, however you do not have to use this information and you can use `-d` or `--data` option to configure vi commands, see the commands below.

#### POST operation via raw data 

```bash
$ restconf-cli POST --username developer --hostname sandbox-iosxe-latest-1.cisco.com \
--path ietf-interfaces:interfaces \
--data '{
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
```

#### PUT operation via raw data 

```bash
$ restconf-cli PUT --username developer --hostname sandbox-iosxe-latest-1.cisco.com \
--path ietf-interfaces:interfaces/interface=Loopback999 \
--data '{
   "interface":[
      {
         "name":"Loopback999",
         "description":"updated by python click - PUT",
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
```

#### PATCH operation via raw data 

```bash
$ restconf-cli PATCH --username developer --hostname sandbox-iosxe-latest-1.cisco.com \
--path ietf-interfaces:interfaces/interface=Loopback999 \
--data '{
   "interface":[
      {
         "name":"Loopback999",
         "description":"updated by python click - PATCH",
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
```
