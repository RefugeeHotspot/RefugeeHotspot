#! /bin/bash
#
# This script checks the availability of a tunnel, and then uses that
# for NAT traffic if it is there. If not, it uses the 3G interface
# directly.
# 
# TODO: Because our 3G dongle mangles DNS traffic quite badly, we may
#       need to disable our DNS resolver if we are using the 3G 
#       directly.

TUN=tun0
GSM=eth1

while /bin/true
do
    # see if we are using a tunnel now
    egrep -q "^ *$TUN: " /proc/net/dev
    # tunnel is up
    if [ $? -eq 0 ]
    then
        iptables --list-rules | egrep -q " -[io] $TUN "
        # tunnel is up, but we are not using NAT to our tunnel
        if [ $? -ne 0 ]
        then
            # note our status
            logger -- "tunnel up, updating iptables"
            # wipe any existing NAT rules
            iptables -t nat -F
            # remove our forwarding rules (if any)
            iptables -D FORWARD -i $GSM -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
            iptables -D FORWARD -i wlan0 -o $GSM -j ACCEPT
            # add our necessary NAT rules
            iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 172.27.1.1
            iptables -t nat -A PREROUTING -p tcp --dport 443 -j DNAT --to-destination 172.27.1.1
            iptables -t nat -A POSTROUTING -o $TUN -j MASQUERADE
            # and add our forwarding rules
            iptables -A FORWARD -i $TUN -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
            iptables -A FORWARD -i wlan0 -o $TUN -j ACCEPT
        fi
    # tunnel is down
    else
        iptables --list-rules | egrep -q " -[io] $GSM "
        # tunnel is down, but we are not using NAT to 3G interface
        if [ $? -ne 0 ]
        then
            # note our status
            logger -- "tunnel down, updating iptables"
            # wipe any existing NAT rules
            iptables -t nat -F
            # remove our forwarding rules (if any)
            iptables -D FORWARD -i $TUN -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
            iptables -D FORWARD -i wlan0 -o $TUN -j ACCEPT
            # add our necessary NAT rules
            iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 172.27.1.1
            iptables -t nat -A PREROUTING -p tcp --dport 443 -j DNAT --to-destination 172.27.1.1
            iptables -t nat -A POSTROUTING -o $GSM -j MASQUERADE
            # and add our forwarding rules
            iptables -A FORWARD -i $GSM -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
            iptables -A FORWARD -i wlan0 -o $GSM -j ACCEPT
        fi
    fi
    # wait a bit before our next check
    sleep 17
done
