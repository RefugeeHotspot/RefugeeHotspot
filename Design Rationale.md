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

	- Resource sharing
	 	-> Maximum peak bandwith
		-> rate limiting per users
			50kb/s per MAC
		-> data cap per user per session 
			more 20 MB 
		-> session time
			2 hours

# Security
Surveillance
	VPN

Device updates
	Audo update every day 

Administration 
	Tor Hidden Service

Privacy
	Mac adresses will not be stored in a database. MAC adresses will be stored in IPtables, but when the power is pulled it is removed. So the device is stateless. 




[0] https://netaidkit.net/

[1] https://github.com/radicallyopensecurity/NetAidKit

