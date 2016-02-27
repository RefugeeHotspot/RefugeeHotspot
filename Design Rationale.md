# Introduction

This document describes the design choices that were made during the development of the Refugee Hotspot. 

# Objective

The objective was to create a reliable and affordable device which can be used to provide refugees with a wifi connection using 3G or 4G. Preferably the device can resist power outages, is mobile, and sturdy. 

# Hardware

Several hardware option were considered and discussed as listed below:

1. 
4g USB modem/dongle + RPi + antenna
(in which RPi functions as router)
(cheapest but depends on most config of RPi)

2. 
4g dongle + router TPLink + RPi 
(in which RPi functions for extra services)
(a bit more expensive but with less config and dedicated hardware (RPi doesn't do networking)

3. 
4g router&modem DLink + RPi
(in which RPi functions for extra services)
(most expensive but with integrated dongle, modem and router (RPi doesn't do networking)

4. 
4g dongle + netaidkit [0][1] + RPi
(in which services run on RPi)

5. 
4g dongle + netaidkit [0][1]
(in which services run on netaidkit)

The options with the commercial routers did not give us the level of adaptability that we wanted. For instance it was hard to setup a landing page and do traffic shaping, as well as running a VPN. There were also security concerns. Finally the computing power of the commercial solutions was not very impressive. Of course there would have been the option of installing OpenWRT on the commercial routers, but working in a full Unix environment (like on the Raspberry Pi) seemed easier. The Netaidkit presented a lot of impressive features but unfortunately the hardware limitations did not allow us to use this for many users. Also the threat model for Netaidkit user is different than for the Refugee Hotspot user. In the Netaidkit Tor is mostly used for cirumvention, not for end-point security. 
Another reason to go with the option in which the Raspberry Pi functioned as a router and server (option 1) is because it's the cheapest option. It is expected that with all hardware included (including battery pack, casing, WiFi antenna, MicroSC card, cables) the device should not costs more than 100 euros. 

# Software and services
The minimal viable product image will enable people to connect to an open WiFi hotspot, where they'll encounter a landingpage informing them they're connecting to a refugee hotspot to: 

	(a) create awareness about the project 
	(b) inform people that this device has limited bandwith 
	(c) instruct users about the policies on the device vis a vis traffic shaping 
	(d) inform users on how to increase their digital security

When users click 'OK' they'll subsequently will be able to browse the Internet. Services that are included in the devices setup to make this happen are: DNS, DHCP, openVPN, Traffic Shaping, webserver, 

# Traffic Shaping policies
Because it's nearly impossible to have a 3G or 4G Internet connection without datacaps (even the so-called 'unlimited data plans' cap at 20 GB / month, or at least significantly reduce connection speed), it seemed reasonable to work on limiting bandwith to dissuade users from torrenting or streaming. One way to do this was informing users with the landing page, but it can be reasonably expected that users will not voluntarily limit their data usage, which would result in less connectivity (potentially for the rest of the month) for the whole group. 

We discussed different traffic shaping and quality of service options such as limiting maximum peak bandwith for the whole device, rate limiting per user, a data cap per user per session, and set a maximum session time. Currently we chose to go for rate limiting per user at 50 kb/s per MAC address. We'll evaluate this choice based on beta testing in the field.

# Security
We want to provide the most secure option for the users, especially because the envisioned target group is a senstive one. At the same time we want the device to be easy to use, so there might be conflicts there.

Currently we're using a open WiFi access point, so the connections to the device are not encrypted. We've discussed the option where the device would accept any credentials for WPA2 as it is implemented in the CCC conference network setup, but it is not expected that users will directly understand that every credential will be accepted, this might unwanteldly limit the use of the device. 

Therefore we currently implemented an open WiFi, but with a warning on the landing page and instructions on improving end-point security by using Tor or a VPN to protect against sniffing.

## On the wire Surveillance
To protect against surveillance on the network we implemented a VPN solution via OpenVPN

## Device updates
To keep the Debian Stable installation up-to-date we're running an auto-update on daily basis. The report of this will be sent to the admin e-mail address which is currently hotspots@refugeehotspot.net

## Administration 
Admin access is provided by SSH over a Tor hidden service. Currently is only accepts SSH authentication via certificate authoritzation.

## Privacy
MAC adresses will not be stored in a database, but they will need to be stored in order to let users naviage past the landingpage. MAC adresses will be stored in IPtables, but when the power is pulled, the MAC adresses  will be removed removed. So the current implementation of the device is technically stateless. 

[0] https://netaidkit.net/

[1] https://github.com/radicallyopensecurity/NetAidKit


