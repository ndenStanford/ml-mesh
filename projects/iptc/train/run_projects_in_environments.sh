#!/bin/bash

# Define your environments
declare -a environments=("IPTC-00000" "IPTC-10000" "IPTC-20000")

for env in "${environments[@]}"; do
    make projects.start/"${PROJECT_NAME}" COMPONENT=train ENV_FILE="$env"
done
