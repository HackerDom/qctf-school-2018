#!/bin/bash

container_id=`sudo docker ps | head -2 | tail -1 | cut -d " " -f 1`

sudo docker cp $container_id:/var/xinetd.log - | tail -c +400
