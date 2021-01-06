#!/bin/bash

# Takes a layer arn as an arg, downloads the corresponding zip w/curl

function dl-layer() {
  if [[ -n "$1" ]]; then
    ARN="$1"
  else
    echo -e "\tusage: ${FUNCNAME[0]} <layer ARN>"
    return -1
  fi
  
  # 0  : 1 :   2  :    3    :    4       :  5  :      6      : 7
  # arn:aws:lambda:us-east-1:898466741470:layer:psycopg2-py38:2
  ARN_NAME_ARR=(${ARN//:/ })
  OUTPUT_FILE=${ARN_NAME_ARR[6]}.zip
  
  curl $(aws lambda get-layer-version-by-arn --arn $ARN | grep Location | awk '{print $2}' | tr -d ,\") > $OUTPUT_FILE
}
