#!/bin/bash
docker-compose down
docker rmi waisaa/webnav:latest
docker-compose up --build -d