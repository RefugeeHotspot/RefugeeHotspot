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
ETH=eth0
GSM=eth1

function switch_nat()
{
    DEV=$1

    # we only need to update if we are not using these rules already
    iptables --list-rules | egrep -q " -[io] $DEV "
    if [ $? -ne 0 ]
    then
        # announce our intentions
        logger -- "updating iptables to use $DEV for traffic"

        # wipe any existing NAT rules
        iptables -t nat -F
        # remove our forwarding rules (if any)
        iptables -D FORWARD -i $TUN -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
        iptables -D FORWARD -i wlan0 -o $TUN -j ACCEPT
        iptables -D FORWARD -i $ETH -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
        iptables -D FORWARD -i wlan0 -o $ETH -j ACCEPT
        iptables -D FORWARD -i $GSM -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
        iptables -D FORWARD -i wlan0 -o $GSM -j ACCEPT
        # add our necessary NAT rules
        iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 172.27.1.1
        iptables -t nat -A PREROUTING -p tcp --dport 443 -j DNAT --to-destination 172.27.1.1
        iptables -t nat -A POSTROUTING -o $DEV -j MASQUERADE
        # and add our forwarding rules
        iptables -A FORWARD -i $DEV -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
        iptables -A FORWARD -i wlan0 -o $DEV -j ACCEPT
    fi
}

while /bin/true
do
    # check tunnel and Ethernet status
    ip link show $TUN 2>/dev/null | grep -q ",UP,"
    TUN_UP=$?
    ip link show $ETH 2>/dev/null | grep -q ",UP,"
    ETH_UP=$?

    # tunnel is up
    if [ $TUN_UP -eq 0 ]
    then
        switch_nat $TUN
    # tunnel is down, but we have cable connection
    elif [ $ETH_UP -eq 0 ]
    then
        switch_nat $ETH
    # otherwise try GSM
    else
        switch_nat $GSM
    fi
    # wait a bit before our next check
    sleep 17
done
