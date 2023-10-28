#!/bin/bash

# Steps taken from https://aws.amazon.com/premiumsupport/knowledge-center/lambda-layer-simulated-docker/

# Change to the desired python runtime
RUNTIME="python3.9"

# Additional compatible runtimes as a space-delimited string
# ADDITIONAL_RUNTIMES="python3.6 python3.7"

ARG="$1"
FILE="requirements.txt"

if [[ "$ARG" == "-h" ]]; then
	echo "$0 <layer-name>"
	exit 0
fi

if [ ! -f $FILE ]; then
    echo "Create a $FILE with the required packages"
	exit 1
fi

# Delete existing folder to avoid adding unintended packages

rm -rf python/

docker run --platform linux/amd64 -v "$PWD":/var/task "public.ecr.aws/sam/build-$RUNTIME" /bin/sh -c "pip install -r requirements.txt -t python/lib/$RUNTIME/site-packages/; exit"
zip -r layer.zip python > /dev/null

# Cleanup
rm -rf python/

if [[ -z "ARG" ]]; then
	exit 0
else
	echo "Publishing $ARG"
	aws lambda publish-layer-version --layer-name $ARG  --zip-file fileb://layer.zip --compatible-runtimes $RUNTIME $ADDITIONAL_RUNTIMES
fi

# Cleanup
rm layer.zip
