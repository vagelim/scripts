#!/bin/bash

ORG=
REPO=

for i in $(curl -s -H "Accept: application/vnd.github+json" \
-H "Authorization: Bearer $GITHUB_TOKEN" \
-H "X-GitHub-Api-Version: 2022-11-28"  \
https://api.github.com/repos/$ORG/$REPO/actions/caches \
| grep id | cut -d ':' -f 2 | tr -d ','); \
do curl -L   -X DELETE   \
-H "Accept: application/vnd.github+json"  \
-H "Authorization: Bearer $GITHUB_TOKEN"  \
-H "X-GitHub-Api-Version: 2022-11-28"   https://api.github.com/repos/$ORG/$REPO/actions/caches/$i; done;
