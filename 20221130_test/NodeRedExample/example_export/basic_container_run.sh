#!/bin/bash

CONTAINER_NAME=node_red_dg
IMAGE_NAME=node_red_dg

# Load the docker image from the .tar file if it hasn't been loaded already
if [ $(sudo docker images | grep -c $IMAGE_NAME) -ge 1 ]; then
    echo image found
else
    echo image not found, loading .tar file
    sudo docker load -i ./node_red_dg.tar
fi

# Take down the existing container if one is running
if [ $(sudo docker ps -a -q --filter "name=$CONTAINER_NAME") ]; then
    echo container found, removing container
    sudo docker rm $(sudo docker stop $CONTAINER_NAME)
else
    echo container not found
fi

# Start the docker image in a container
sudo docker run -it -d --name=$CONTAINER_NAME --network=host --restart=unless-stopped -v /etc/localtime:/etc/localtime:ro $IMAGE_NAME
