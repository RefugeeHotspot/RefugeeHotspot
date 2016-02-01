# Refugee Hotspot

A mobile device to remove the obstacles that refugees face when it comes to access the internet is being developed by Alternative Learning Tank (ALT) & The Internet Society Netherlands (ISOC-NL) in dialogue with refugee collectives in the Netherlands, Belgium and Germany, this devices will provide connectivity in each of the collectives physical locations and thanks to its batteries will keep providing connectivity in the situation on which a collective is being evicted from their location. 

The device can be taken into demonstrations, marches or specific actions acting as a media center in combination with the rest of the media platform. It will be possible to distribute files, images, statements and flyers wireless while using the device in the collectives locations but also in demonstrations, beyond connectivity  it also functions as a portable digital toolkit and library for the collectives.  

An online campaign will be launched to spread and expand the development and reach of the device, being easy to scale up and distribute to other places. The campaign includes basic user guides accessible for refugees in different languages and an awareness campaign about the refugee struggle and the access to internet as a right for everyone. The campaign could use elements of crowdfunding and it could be open for new partners that will help and support the further diffusion of the device and how-to to as many collectives as possible.

The goal is to implement a critical and conscious use of technology, conceptually consequent with the values of the Forum and the specific situations of the collectives involved. The platform aims to use values of the free software and open source movements, as they resonate as necessary for the struggle towards a free and open society.

# Device Specs

Five setup possibilities to be tested at the hackathon (more info below):
    
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
    # assumption is that this is pretty much a ready-made solution
    
    4. 
    4g dongle + netaidkit [0][1] + RPi
    (in which services run on RPi)

    5.
    4g dongle + netaidkit [0][1]
    (in which services run on netaidkit)




# Hackathon

Will be organized on February 5 and 6 in Amsterdam - sign up here -> http://hackshackers.nl/

We'll be working on the issues mentioned here: https://github.com/nllz/refugeehotspot/issues
as well as other issues you might come up with. Feel free to add them or bring them up at the hackathon.

List hardware that will be available for hacking at hackathon:

    http://www.dlink.com/uk/en/home-solutions/connect/broadband-modems-and-routers/dwr-921-4g-lte-router <--- SIM card slot integrated
    
    Portable Router TP­LINK TL­MR3020 3G/4G Wireless N150 <--- No SIM card slot http://www.amazon.co.uk/gp/product/B00634PLTW?psc=1&redirect=true&ref_=ox_sc_act_title_7&smid=A3P5ROKL5A1OLE
    
    USB 4g dongle+SIM card http://www.amazon.co.uk/Huawei-E398u-1-Rotator-FASTEST-available/dp/B00BPYTX4E/ref=sr_1_1?ie=UTF8&qid=1448723439&sr=8-1&keywords=huawei+4g+dongle+e398u
    
    Battery Pack 20.000mah http://www.amazon.co.uk/Compact-20000mAh-Portable-Anker-PowerCore/dp/B00VJSGT2A/ref=sr_1_3?ie=UTF8&qid=1448723027&sr=8-3&keywords=battery+pack
    
    TTL cable http://www.amazon.co.uk/USB-TTL-Serial-Cable-Raspberry/dp/B00CNUH6QG/ref=sr_1_2?ie=UTF8&qid=1448723791&sr=8-2&keywords=ttl+cable+raspberry+pi
    
    Wifi Antenna USB http://www.amazon.co.uk/Network-AWUS036AC-Long-Range-Dual-Band-Connections/dp/B00MX57AO4/ref=sr_1_10?ie=UTF8&qid=1448723928&sr=8-10&keywords=wifi+antenna+usb
    
    32GB Micro SD card (OS+storage space) http://www.amazon.co.uk/gp/product/B00519BEQY?psc=1&redirect=true&ref_=ox_sc_act_title_4&smid=A1I0WA5OXHTGPB
    
    Case for the device
    
    4 x Raspberry Pi 2 B+ http://www.amazon.co.uk/gp/product/B00T2U7R7I?psc=1&redirect=true&ref_=ox_sc_act_title_3&smid=A3P5ROKL5A1OLE
    
    4 x Netaidkit

Feel free to bring your own hardware! All Raspberry Pi's are welcome :)

# Questions? Comments? More information?:

Feel free to email project [at] digitaldissidents [dot] org or leave an issue in the tracker.



# Project notes
Rpi Zero version:
    Adding Ethernet support in the GPIO:
        http://raspi.tv/2015/ethernet-on-pi-zero-how-to-put-an-ethernet-port-on-your-pi
        
    Adding Wifi module soldered (no USB):
        https://hackaday.com/2015/11/28/first-raspberry-pi-zero-hack-piggy-back-wifi/



[0] https://netaidkit.net/

[1] https://github.com/radicallyopensecurity/NetAidKit
