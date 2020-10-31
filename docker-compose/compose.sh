#!/usr/bin/env bash

docker-compose pull
docker-compose up -d --remove-orphans
docker rmi $(docker images -f 'dangling=true' -q) --force