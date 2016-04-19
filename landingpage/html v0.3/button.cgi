#! /bin/bash

echo "Content-type: text/plain"
echo ""

/usr/bin/sudo /usr/local/bin/iptables-open $REMOTE_ADDR
if [ $? -eq 0 ]; then
    echo "Connected"
else
    echo "NOT Connected"
fi
