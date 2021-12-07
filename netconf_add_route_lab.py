#! /usr/bin/env python

# Import libraries
from ncclient import manager
from xml.dom import minidom
import xmltodict
import sys

# New Loopback Details
route = {"destination_prefix": "PREFIX/MASK",  #e.g. 1.1.1.1/32
            "next_hop_address": "IP_ADDRESS"}  #e.g. 2.2.2.2 

config_data="""
<config>
   <routing xmlns="urn:ietf:params:xml:ns:yang:ietf-routing">
      <routing-instance>
         <name>default</name>
         <description>default-vrf [read-only]</description>
         <interfaces/>
         <routing-protocols>
            <routing-protocol>
               <type>static</type>
               <name>1</name>
               <static-routes>
                  <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ipv4-unicast-routing">
                     <route>
                        <destination-prefix>{destination_prefix}</destination-prefix>
                        <next-hop>
                           <next-hop-address>{next_hop_address}</next-hop-address>
                        </next-hop>
                     </route>
                  </ipv4>
               </static-routes>
            </routing-protocol>
         </routing-protocols>
      </routing-instance>
   </routing>
</config>
"""

# Open NETCONF connection to device
with manager.connect(host = 'ROUTER_IP_ADDRESS',
                     port = 830,
                     username = 'USERNAME',
                     password = 'PASSWORD',
                     hostkey_verify = False,allow_agent=False) as m:

    # Create desired NETCONF config payload and <edit-config>
    config = config_data.format(**route)
    r = m.edit_config(target = "running", config = config)

    # Print OK status
    print("NETCONF RPC OK: {}".format(r.ok))

