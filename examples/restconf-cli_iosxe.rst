$ restconf-cli GET -u developer -n sandbox-iosxe-latest-1.cisco.com -p Cisco-IOS-XE-native:native/interface

$ restconf-cli GET -u developer -n sandbox-iosxe-latest-1.cisco.com -p ietf-interfaces:interfaces/interface=Loopback999

$ restconf-cli GET -u developer -n sandbox-iosxe-latest-1.cisco.com -p Cisco-IOS-XE-native:native/interface -o output.json

$ restconf-cli DELETE -u developer -n sandbox-iosxe-latest-1.cisco.com -p ietf-interfaces:interfaces/interface=Loopback999

### POST operation via raw data 

'''bash
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
'''

'''
### POST operation via file 

$ restconf-cli POST --username developer --hostname sandbox-iosxe-latest-1.cisco.com \
--path ietf-interfaces:interfaces --from-file output.json
'''

'''bash
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
'''

'''
$ restconf-cli PUT --username developer --hostname sandbox-iosxe-latest-1.cisco.com \
--path ietf-interfaces:interfaces/interface=Loopback100 --from-file output.json
'''

'''bash
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
'''

'''
restconf-cli PATCH --username developer --hostname sandbox-iosxe-latest-1.cisco.com \
--path ietf-interfaces:interfaces/interface=Loopback100 --from-file output.json
'''