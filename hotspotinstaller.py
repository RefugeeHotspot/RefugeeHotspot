#! /usr/bin/env python3

import os
import readline
import shutil
import sys
import time

# This program is the installer for the refugee hotspot. It is run
# every time the system boots.

def input_with_default(prompt, default):
    try:
        result = input(prompt).strip()
    except EOFError:
        sys.exit(1)
    if result == '':
        result = default
    return result

def yes_no(prompt):
    while True:
        answer = input_with_default(prompt + " ([Y]/n) ", 'y')
        if answer.lower() in ("n", "no"):
            return "n"
        if answer.lower() in ("y", "yes"):
            return "y"

def wait_for_user():
    input("Press Enter to continue...")
    print()

def interfaces():
    iface_file = open("/proc/net/dev", "r")
    iface_list = []
    # skip first two lines, which are informational
    iface_file.readline()
    iface_file.readline()
    # get the interface name at the start of each line thereafter
    while True:
        line = iface_file.readline()
        if line == '':
            return sorted(iface_list)
        iface_list.append(line.split(':')[0].strip())

class spinner:
    def __init__(self, text=None):
        self.text = text
        if self.text is None:
            self.text = r"/-\|"
        self.ofs = 0
    def update(self):
        print(self.text[self.ofs], end='\x08', flush=True)
        self.ofs = (self.ofs + 1) % len(self.text)

def main():
    # see if we want to run
    want_run = yes_no("Do you want to run the Hotspot Installer?")
    if want_run != "y":
        sys.exit(0)

    # display introduction
    print("""
Welcome to the Refugee Hotspot Admin Setup.

This is probably the first time you're running this device. So we
would like to help you set this up. 

The Refugee Hotspot is aimed at providing Internet connections to
migrants and refugees by using a 3G connection and turning it into a
wireless network that people can access. 

Note: This setup is meant for people who will administer a Refugee
Hotspot.  This means you will need to have at least a basic
understanding of networking and Debian or similar GNU/Linux systems. 

There are eight short steps for this, which should not take you more
than 10 minutes.

Let's get this set up. 
""")
    wait_for_user()

    # alert about information that will be needed
    print("""0. Preparation

You need the following:

* A VPN certificate (.ovpn file)
* Your public SSH key

Make sure that you have either copied these onto this flash card or
have a USB plugged in with these files on it.

If you have no idea what we're talking about, just continue. 
""")
    wait_for_user()

    # remote access (SSH) setup
    print("""1. Remote Access (SSH Login)

You might want to remotely administer this device so you can check
whether it works without having to be physically connected to it.
Remote access is provided via a Tor Hidden Service. 

To be able to get remote access to this device you will need to add
your public SSH key to the file:

     /home/nomad/.ssh/authorized_keys/

There are two approaches to this: 

    Approach 1
    ----------
    Put the SD card into your computer and copy your public SSH key to
    $MOUNT/home/nomad/.ssh/authorized_keys, where $MOUNT is the
    directory you have mounted the SD card.

    Approach 2
    ----------
    Put an USB flash drive with the public SSH key on it into the
    Raspberry Pi and copy the SSH key to
    /home/nomad/.ssh/authorized_keys (you might need to mount the USB
    flash drive first). 
 
If you don't know what an SSH key is, let alone how to generate it,
you might want to search on the Internet, or read the ssh man page
(via "man ssh"), or not use remote administatration at all. :)

This is the Tor Hidden Service address to which you can connect:
""")
    try:
        print("    " + open("/var/lib/tor/ssh/hostname").read())
    except IOError as e:
        print("    [ERROR reading Tor hostname]")
    print("""
The Tor Hidden Service address will also be e-mailed to your
administration e-mail on boot, if you set this up.
""")
    wait_for_user()

    # VPN setup
    print("""2. VPN 

This device works without a VPN connection, but it works better and is
more stable with a VPN connection. A VPN also protects your users from
several kinds of mass surveillance. 

Therefore it is recommended that you purchase you own VPN certificate,
for instance from AirVPN: https://airvpn.org. Alternatively you can
use a VPN certificate provided by us, with no guarantee that it will
keep working. 
""")
    while True:
        vpn_file = input("Name of the ovpn file (empty if none): ")
        if vpn_file == '':
            break
        try:
            shutil.copy(vpn_file, "/etc/openvpn/hotspot.conf")
        except IOError as e:
            print("Error copying ovpn file: " + str(e))
        else:
            break
    if vpn_file:
        print("Starting OpenVPN...", end='', flush=True)
        os.system("systemctl start openvpn")
        spin = spinner()
        while not "tun0" in interfaces(): 
            spin.update()
            time.sleep(0.5)
        print("ready.")
    print()

    # Administrator e-mail setup
    print("""3. Administration notifications by e-mail

As an administrator of this device you might want to receive an email
every time the device does an update and when it reboots. If so,
please enter an email address for these updates.
""")
    admin_email = input("Administrator e-mail: ")
    print()

    # Administrator e-mail setup
    print("""4. Status reporting to ISOC-NL

Do you also want status updates of your device to be sent to ISOC-NL?
This will be used for statistics and might help us troubleshooting.
""")
    want_status_to_isoc = yes_no("Send status updates to ISOC-NL?")
    print()

    # Traffic shaping
    print("""5. Traffic limiting

Since on the mobile Internet bandwidth is a scarce resource we want to
give you the option of limiting the download speed per user.

The value you type will be kilobits/second. If you choose 0, there will
be no limit. The default is 50 kilobits/second.
""")
    while True:
        answer = input_with_default(
                     "Maximum download speed per user (0=no limit, [50]) ",
                                    '50')
        try:
            max_speed = int(answer)
        except ValueError:
            print("Invalid number: " + answer)
        else:
            break
    print()

    # WiFi SSID
    print("""6. WiFi SSID

What do you want the name of the Wireless Network to be (SSID)?
""")
    while True:
        ssid = input("SSID: ")
        if len(ssid) > 32:
            print("Maximum SSID length is 32")
        elif len(ssid) > 0:
            break
    print()

    # Landing page
    print("""7. Landing page

The landing page that is being used is placed in /var/www/html/, feel
free to edit or replace it. 
""")
    wait_for_user()

    # Champagne
    print("""
Your device should be good to go now. Documentation can be found at:

    https://github.com/RefugeeHotspot/RefugeeHotspot

You can leave questions, issues and suggestions in the issue tracker
there.  Discussions and questions can be asked via mail at:

    <list@refugeehotspot.net>

When you press Enter, the device will reboot for final setup.
""")
    wait_for_user()

if __name__ == "__main__":
    main()
