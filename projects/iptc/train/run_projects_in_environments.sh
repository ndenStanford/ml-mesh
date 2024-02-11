#!/bin/bash

# Define your environments
declare -a environments=("IPTC-00" "IPTC-02" "IPTC-03")

for env in "${environments[@]}"; do
    make projects.start/"${PROJECT_NAME}" COMPONENT=train MODEL_ID="$env"
done
