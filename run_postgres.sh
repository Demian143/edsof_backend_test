#!/bin/bash

sudo docker stop aws-postgres
sudo docker rm aws-postgres

sudo docker-compose up

