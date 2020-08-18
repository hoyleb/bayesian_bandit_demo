#!/bin/bash

docker build --tag hoyleb/bandit:v0.0.1 .

docker run  -p 8080:8080 -it hoyleb/bandit:v0.0.1
