#!/bin/bash

container_id=`sudo docker ps -a | grep "oil" | cut -d " " -f 1`

sudo docker cp $container_id:/var/xinetd.log - | tail -c +400
