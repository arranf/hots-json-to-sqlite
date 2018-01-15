#!/bin/bash


# export AWS_ACCESS_KEY_ID=YOURACCESSKEYHERE
# export AWS_SECRET_ACCESS_KEY=YOURSECRETACCESKEYHERE
# export AWS_DEFAULT_REGION=eu-west-1

# Create sha.txt of repo
touch upload/sha.txt
cd heroes-talents && git rev-parse --verify HEAD > ../upload/sha.txt

# Sync files to AWS
aws s3 sync ../upload/ s3://data.heroescompanion.com