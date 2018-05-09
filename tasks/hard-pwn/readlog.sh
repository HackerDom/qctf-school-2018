#!/bin/bash

container_id=`sudo docker ps -a | grep hard-pwn | cut -d " " -f 1`

if [ "$container_id" == "" ]; then
    echo "xinetd isn't loaded!"
    exit
fi

sudo docker cp $container_id:/var/xinetd.log - | tail -c +400
