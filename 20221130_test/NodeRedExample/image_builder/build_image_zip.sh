#!/bin/bash
cd "$(dirname "$0")"
echo "Running from: $PWD"

######################################
# Add some info to the docker container about who built it and when.
######################################
echo "Making builder.txt"
rm -f builder.txt
{
    printf "Date: "
    date
} >> builder.txt
{
    printf "Builder: "
    whoami
} >> builder.txt
{
    printf "Branch: "
    git rev-parse --abbrev-ref HEAD
} >> builder.txt
{
    printf "Hash: "
    git rev-parse --short HEAD
} >> builder.txt
mv builder.txt ../example_export

######################################
# Declaratively copy items into build directory for minimum build context
######################################
echo "Copying necessary artifacts to Docker build context"
cp -rL ../src .

######################################
# Build and save image before generating solution zip
######################################
echo "Docker build"
sudo docker build -t node_red_dg .
echo "Docker save"
sudo docker save example_service | gzip > ../example_export/node_red_dg.tgz
echo "Making Zip"
cd ../example_export
tar --mtime='1970-01-01' -czvf ../node_red_dg.spx *
cd ../image_builder

######################################
# Delete copies in make_image_and_zip for single source of record
######################################
#echo "Cleaning up"
#find . -not \( -name 'Dockerfile' -or -name 'build_image_zip.sh' \) -delete
