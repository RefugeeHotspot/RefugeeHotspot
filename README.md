# Refugee Hotspot

A mobile device to remove the obstacles that refugees face when it comes to access the internet is being developed by The Internet Society Netherlands (ISOC-NL) in dialogue with refugee collectives in the Netherlands, Belgium and Germany. This devices will provide connectivity in each of the collectives physical locations and thanks to its battery will keep providing connectivity in the situation in which a collective is being evicted from their location. 

The device can be taken into demonstrations, marches or specific actions. It will be possible to distribute files, images, statements and flyers wireless using the landingpage.

We're aiming to deploy this device as wide as possible, starting with collectives in the Netherlands, Germany and Belgium. Currently we are in the testing phase, if you would like to test the technology, please feel free to do so. If you would like to contribute code or ideas, we're also very open to that. 

The goal is to implement a critical and conscious use of technology tailored to the needs of the refugee and migrant collectives involved. The platform aims to use values of the free software and open source movements, as they resonate as necessary for the struggle towards a free and open society, and a free Internet available for everyone. 

# Device Specs

    Raspberry Pi 3
    3G / HSPA USB modem/dongle (Huawei E303)
    8 GB Micro SD card
    Powered USB hub (which we aim to replace with USB Y cables)
    Battery pack
    Short USB cables

# Schematic Drawing

             +---------------+---------------------+
             |               |    +-------------+  |
             |               |    |             |  |
             |       +-------+----+---+         |  |
             |       |                |         |  |
             |       |                |   +-----+--+---+
           +-+----+  |                |   |            |
           |      |  |                |   |            |
           |      |  |                |   |            |
           |      |  | Raspberry Pi 3 |   |Battery Pack|
           |   3G |  |                |   |20.000 mAh  |
           |Dongle|  |                |   |            |
           |      |  |                |   |            |
           |      |  |                |   |            |
           |      |  |                |   |            |
           |      |  |                |   |            |
           |      |  |                |   |            |
           |      |  |                |   |            |
           +-+---++  +------+---+-----+   +------------+
             |SIM|          |SD |
             +---+          +---+

# Want to test?

Have a look at the device setup here: 
https://github.com/RefugeeHotspot/RefugeeHotspot/blob/master/Hotspot-Setup-Travelogue.md 

We'll have a bootable beta image up soon!

# Casing

We're working on a reproducible lasercut casing with Waag Society. We hope to have photos, instructions and the svg files up here soon. 

# Questions? Comments? More information?:

Feel free to sign up to the mailinglist at https://lists.ghserv.net/mailman/listinfo/list and share your question, suggestion, or concern or leave an issue in the GitHub issue tracker.



