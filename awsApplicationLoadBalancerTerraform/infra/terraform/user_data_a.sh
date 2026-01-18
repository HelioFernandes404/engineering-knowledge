#!/bin/bash

sudo su
yum update -y
yum install docker -y
systemctl start docker
systemctl enable docker
docker run -d -p 80:8080 heliofernandes/public-api_a:latest