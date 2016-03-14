# Introduction

This document serves to describe in some detail the setup for the
Refugee Hotspot.

# Base Setup

Before starting, a few pieces of hardware will be necessary:

  1. Raspberry Pi 2
  2. Powered USB hub
  3. ALFA AWUS036AC USB 802.11 WiFi dongle
  4. Huawei E303 USB 4G dongle
  5. microSD card (and a way to write to it)
  6. USB cables to connect everything

During the setup, you'll need some way to connect the Raspberry Pi 2
to the Internet. The easiest way is via an Ethernet cable, but
alternatively you can use a WiFi setup or even something fancier. You
may also want a USB keyboard and HDMI-capable monitor, but you can
also log in via SSH from some other computer.

## Download and Write Raspbian Jessie Lite Image

The latest Raspbian Jessie Lite image can be found here:

https://www.raspberrypi.org/downloads/raspbian/

You'll get a ZIP file that you need to unzip and copy to a microSD
card. Many laptops have a SD reader, and you can easily get a microSD
to SD adapter (many microSD include one when you buy them).

If you want to use the command line to write the image, you need to
know what device to write to. The `dmesg` command will usually display
information about what the device name is. This is usually
`/dev/mmcblk0` or `/dev/sdc` or something like that.

This is what I used:

    $ unzip 2016-02-09-raspbian-jessie-lite.zip
    $ dd if=2016-02-09-raspbian-jessie-lite.img of=/dev/mmcblk0 bs=64K

This will probably take more than 5 minutes, and may take much longer
if you have a slow microSD card.

Once you have written the image, you probably want to re-size the root
partition. I used `gparted` for this.

## Updating the System

The next step is to update the system. You need to login, using the
default user name and password:

    username: pi
    password: raspberry

Update the base system:

    $ sudo apt update
    $ sudo apt upgrade

A reboot may be necessary.

## Installing Handy Stuff (optional)

If you want, it might be helpful to install a few utilities.

    $ sudo apt install vim
    $ sudo apt install screen
    $ sudo apt install mtr-tiny
    $ sudo apt install tcpdump
    $ sudo apt install telnet
    $ sudo apt install dnsutils
    $ sudo apt install lsof

## Renaming the Device

By default the device calls itself "raspberrypi". We should rename
this to something that we like. Change "raspberrypi" to "nomad" in:

* `/etc/hosts`
* `/etc/hostname`

## Adding a User and Removing Default User

We want to create a new user and remove the default one.

    $ sudo adduser nomad

I used the `pwgen` program to make a random password, but you can use
what you want.

You also need to add this user to some administration groups:

    $ sudo usermod -a -G adm,sudo nomad

You should also set this user up to not need a password for the `sudo`
command:

    $ sudo sudoedit /etc/sudoers

Make the last line:

    nomad ALL=(ALL) NOPASSWD: ALL

You can put an SSH public key in `~nomad/.ssh/authorized_keys`, and
then the password is no longer necessary.

Finally, log in as the `nomad` user and remove the default `pi` user:

    $ sudo deluser --remove-all-files pi

# Picking Private IP Addresses

We need to decide which IP addresses to use when people connect. This
is almost always done using RFC 1918 addresses. Most commonly this
looks like `192.168.1.15` or `10.1.1.177`. Because these addresses are
not registered anywhere, it is possible that they will collide. In
order to avoid this, we will use somewhat unusual ones,
`172.27.1.0/24`. This does not guarantee that there will be no
collisions, but the chances are small.

# WiFi Setup as Host Access Point (hostapd)

Once we have our wireless drivers, we can set up the host as an
access point. The usual way is with the hostapd program.

hostapd is a package:

    $ sudo apt install hostapd

Remove `wlan0` and `wlan1` from `/etc/network/interfaces`, but then
add the following:

```
allow-hotplug wlan0
iface wlan0 inet static
        address 172.27.1.1
        netmask 255.255.255.0
        pre-up tc qdisc add dev wlan0 root fq_codel
        post-down tc qdisc del dev wlan0 root fq_codel
```

Create `/etc/hostap/hostapd.conf`:

```
interface=wlan0
driver=nl80211

hw_mode=g
channel=1
max_num_sta=8

ieee80211n=1
wmm_enabled=1

# country limitations
country_code=NL
ieee80211d=1
ieee80211h=1

logger_stdout=-1
logger_stdout_level=2

ssid=nomad
```

Finally, update `/etc/default/hostapd` and set:

```
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```

Reboot, and we should be advertising the wireless network. We can't
connect to it yet, but the WiFi is now working.

# DHCP Server Setup

We need to give out IP addresses. The DHCP protocol performs this. The
ISC DHCP server is packaged in Debian:

    $ sudo apt install isc-dhcp-server

We need to configure it:

    $ sudo mv /etc/dhcp/dhcpd.conf /etc/dhcp/dhcpd.conf.bak
    $ sudo vi /etc/dhcp/dhcpd.conf

It should look like this:

```
ddns-update-style none;
option domain-name-servers 172.27.1.1;

default-lease-time 600;
max-lease-time 1800;

authoritative;

subnet 172.27.1.0 netmask 255.255.255.0 {
    range 172.27.1.33 172.27.1.222;
    option routers 172.27.1.1;
}
```

You can now start the DHCP server via:

    $ sudo /etc/init.d/isc-dhcp-server start

At this point it is possible to connect to the WiFi, although you
of course cannot get to the Internet.

# Remote Administration Setup

We want to be able to administer the AP remotely. While in the long
run this is probably not a good idea, for now it is reasonable.

## Disable Password Logins

Ideally we will change to login only using public/private keys. Update
`/etc/ssh/sshd_config` and change `PasswordAuthentication` to "no":

```
PasswordAuthentication no
```

Restart SSH for this to take effect:

    $ sudo /etc/init.d/ssh restart

## Tor Hidden Service for SSH

We will add a Tor hidden service. This is beneficial mostly because it
provides a stable end-point for us to connect to no matter what IP
address our ISP gives us. It is slow, but perfectly usable for simple
administration.

A good HOWTO is here:

http://mancoosi.org/~abate/hidden-ssh-service-tor

We base our setup on that.

First, install the Tor software:

    $ sudo apt install tor

Now tell Tor to set up an SSH hidden service:

    $ sudo vim /etc/tor/torrc

It needs to include:

```
HiddenServiceDir /var/lib/tor/ssh
HiddenServicePort 22 127.0.0.1:22
```

Restart Tor for this to take effect:

    $ sudo /etc/init.d/tor restart

You can find the hostname to connect to via:

    $ sudo cat /var/lib/tor/ssh/hostname

You can update `~/.ssh/config` on your client to use Tor for `.onion`
like this:

```
Host *.onion
ProxyCommand connect -a none -R remote -5 -S 127.0.0.1:9050 %h %p
```

You need to have the `connect` program installed. In Debian or
Debian-derived distributions (like Ubuntu or Linux Mint) then this
is in the `connect-proxy` package.

Then you can log in via ssh using the `.onion` name.

## Enable 4G Network

We turn our Huawei E303 into a modem though magic commands. This is
all documented:

http://www.linux-hardware-guide.com/2014-05-11-huawei-e303-wireless-mobile-broadband-modem-umts-gsm-microsd-usb-2-0

We need to install "USB modeswitch" utilities:

    $ sudo apt install usb-modeswitch

Then we can update the udev rules to turn the USB dongle into a modem
by creating `/etc/udev/rules.d/70-usb-modeswitch.rules` so that it
looks like this:

```
ACTION=="add", SUBSYSTEM=="usb", ATTRS{idVendor}=="12d1", ATTRS{idProduct}=="1f01", RUN+="/usr/sbin/usb_modeswitch -v 12d1 -p 1f01 -M '55534243123456780000000000000a11062000000000000100000000000000'"
```

Add the following to `/etc/network/interfaces`:

```
iface eth1 inet manual
        pre-up tc qdisc add dev eth1 root fq_codel
        post-down tc qdisc del dev eth1 root fq_codel
```

Go ahead and set up `eth0` to also use the `fq_codel` scheme:

```
iface eth0 inet manual
        pre-up tc qdisc add dev eth0 root fq_codel
        post-down tc qdisc del dev eth0 root fq_codel
```


A reboot should bring the dongle up as the `eth1` interface.


# VPN Setup

We prefer to tunnel traffic via a VPN. We have a VPN set up at
GreenHost:

    $ sudo apt install openvpn
    $ sudo mkdir /etc/openvpn/greenhost
    $ sudo cp ca.crt niels.* /etc/openvpn/greenhost
    $ sudo cp greenhost.ovpn /etc/openvpn/greenhost.conf
    $ sudo vim /etc/openvpn/greenhost.conf # set paths to /etc/openvpn/greenhost
    ...
    ca /etc/openvpn/greenhost/ca.crt
    cert /etc/openvpn/greenhost/niels.crt
    key /etc/openvpn/greenhost/niels.key
    ...

# Setting up IP Forwarding

We need to enable forwarding from the WiFi network to the Internet.

Modify `/etc/sysctl.conf` to support IPv4 packet forwarding:

```
net.ipv4.ip_forward=1
```

Now set up the low-level NAT functionality:

    $ sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 172.27.1.1
    $ sudo iptables -t nat -A PREROUTING -p tcp --dport 443 -j DNAT --to-destination 172.27.1.1
    $ sudo iptables -t nat -A POSTROUTING -o tun0 -j MASQUERADE
    $ sudo iptables -A FORWARD -i tun0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
    $ sudo iptables -A FORWARD -i wlan0 -o tun0 -j ACCEPT

Now make it persistent:

    $ sudo apt install iptables-persistent

Save the current IPv4 table rules. The IPv6 can be saved, but we are
not (yet) setting up IPv6.

If you change the rules later you can save them via:

    $ sudo dpkg-reconfigure iptables-persistent

But be careful not to make any MAC addresses that have been authorized
to connect to the Internet persistent. If in doubt, don't save the
iptables rules!

# Add a DNS Resolver

We could forward DNS queries to the 4G ISP's network, but it makes
sense to keep a local caching resolver on the access point. Soon the
Knot Resolver will probably be the best choice, since it provides a
static cache that can be recovered on restart. But for now the Unbound
resolver is probably the best option, as it is fast and stable.

    $ sudo apt install unbound

Set up `/etc/unbound/unbound.conf`:

```
include: "/etc/unbound/unbound.conf.d/*.conf"

server:
  prefetch: yes
  prefetch-key: yes
  minimal-responses: yes
  harden-referral-path: yes

  interface: 0.0.0.0
  access-control: 172.27.1.0/24 allow
```

# Disable Unneeded Services

By default Raspbian starts a few services that we don't care about.
Lets disable those:

    $ sudo systemctl stop avahi-daemon
    $ sudo systemctl disable avahi-daemon
    $ sudo systemctl stop triggerhappy
    $ sudo systemctl disable triggerhappy


# Script to Unblock IP from Landing Page

We need a way that when a user acknowledges the landing page that we
remove them from the `iptables` rules. The following script,
`/usr/local/bin/iptables-open`, should work:

```bash
#! /bin/bash

# This script opens the iptables rules for a given IP address so that
# it can connect to the Internet without getting traffic redirected to
# the landing page.
#
# It works by looking for the IP address in the ARP table and then
# inserting a rule for the MAC address found into the iptables to
# allow traffic.
# 
# For debugging, you can use "-v" and it will log what it is doing
# using syslog. DO NOT USE "-v" IN NORMAL OPERATION. It will then log
# all MAC addresses to syslog which may be recovered later, and we
# prefer not to log anything that can be used to identify users.
#
# It could be improved by:
# * adding help (for example if run without arguemnts)
# * deleting any old rules for the MAC address found (in case run
#   multiple times)
# * checking the result of the iptables run
# * providing output (so if something goes wrong we can return a code
#   to the user)

# This script looks in the ARP table and finds the MAC 

# if we've run with verbose, then log everything
if [ "$1" == "-v" ]; then
  LOG="logger --"
  PROC_NAME=`readlink --canonicalize $0`
  $LOG $PROC_NAME running with arguments '"'$*'"'
  shift
else
  LOG=true
fi

# the IP address should be passed as the first argument
IP=$1
$LOG looking for IP address $IP in ARP table

# look for this IP address in our ARP table
MAC=`awk '/^'$1'/{ print $4 }' /proc/net/arp`

# confirm that we got something that looks like a MAC address
echo $MAC | egrep -q '^([a-f0-9]{2}:){5}[a-f0-9]{2}$'
if [ $? -ne 0 ]; then
  $LOG got '"'"$MAC"'"', which does not look like a mac address
  exit 1
fi

# we found this MAC address
$LOG $IP using MAC address $MAC

# open up our iptables for this MAC address
$LOG iptables -t nat -I PREROUTING -p tcp --dport 80 -m mac --mac-source $MAC -j ACCEPT
iptables -t nat -I PREROUTING -p tcp --dport 80 -m mac --mac-source $MAC -j ACCEPT
$LOG iptables -t nat -I PREROUTING -p tcp --dport 443 -m mac --mac-source $MAC -j ACCEPT
iptables -t nat -I PREROUTING -p tcp --dport 443 -m mac --mac-source $MAC -j ACCEPT

# yay, it worked
exit 0
```

We will need to run this script as root.

    $ sudo chmod 755 /usr/local/bin/iptables-open
    $ sudo sudoedit /etc/sudoers
    ...
    www-data ALL = NOPASSWD: /usr/local/bin/iptables-open *
    ...

# Setup Apache

Install the Apache web server:

    $ sudo apt install apache2

Put our awesome landing page in place:

    $ sudo cp index.html /var/www/html/index.html

Set up CGI so that it will run:

    $ cd /etc/apache2/mods-enabled
    $ sudo ln -s ../mods-available/cgi.load .
    $ sudo vim /etc/apache2/mods-available/mime.conf
    ...
        AddHandler cgi-script .cgi
    ...
    $ sudo apachectl restart


nomad@nomad:/var/www/html $ sudo mv button.cgi /usr/lib/cgi-bin/.

--------

_Everything after here is future work or random notes_

TODO: rate limiting  
TODO: e-mail for sending    
TODO: cron-apt    
TODO: upnp  
TODO: IPv6  
TODO: strip out unused stuff to speed boot (for example)  
TODO: restore access to 192.168.8.1 (admin page)  

Current development unit is at: 

    ssh -v nomad@w4mtwfeuz3ul4zdz.onion
