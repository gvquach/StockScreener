#!/bin/bash
imageName=myimage
containerName=mycontainer

docker build -t $imageName .

echo Delete old container...
docker rm -f $containerName

echo Run new container...
docker run -d --name $containerName -p 80:80 $imageName