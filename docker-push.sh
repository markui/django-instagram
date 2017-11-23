#!/usr/bin/env bash
docker build -t base -f Dockerfile.base .
docker tag base viking617/base
docker push viking617/base