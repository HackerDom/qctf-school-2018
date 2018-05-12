#!/bin/bash

cid=`sudo docker ps | grep "oil" | cut -d " " -f 1`

if [ "$cid" == "" ]; then
    echo "No such container!"
    exit
fi

sudo docker exec -it $cid bash
