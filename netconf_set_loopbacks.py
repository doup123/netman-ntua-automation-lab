#! /usr/bin/env python

# Import libraries
from ncclient import manager
from xml.dom import minidom
import xmltodict
import sys
from time import sleep 


loopback = {"int_name": "Loopback1",
            "description": "Test Building",
            "ip": "1.1.1.1",
            "netmask": "255.255.0.0"}

# Create config template for an interface
config_data = """
<config>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
      <interface>
        <name>{int_name}</name>
        <description>{description}</description>
        <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
	  ianaift:softwareLoopback
        </type>
        <enabled>true</enabled>
        <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
          <address>
            <ip>{ip}</ip>
            <netmask>{netmask}</netmask>
          </address>
        </ipv4>
      </interface>
  </interfaces>
</config>
"""

# Open NETCONF connection to device
with manager.connect(host = 'ROUTER_IP_ADDRESS',
                     port = 830,
                     username = 'USERNAME',
                     password = 'PASSWORD',
                     hostkey_verify = False,allow_agent=False) as m:
    # ADD YOUR CODE HERE FOR MULTIPLE LOOPBACKS
    # Create desired NETCONF config payload and <edit-config>
    config = config_data.format(**loopback)
    r = m.edit_config(target = "running", config = config)
    sleep(2)

    # Print OK status
    print("NETCONF RPC OK: {}".format(r.ok)+" Loopback1 created")
