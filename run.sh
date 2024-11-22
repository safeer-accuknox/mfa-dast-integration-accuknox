#!/bin/bash

echo "$(date)" > time
docker stop juiceshop && docker rm juiceshop
docker run --name juiceshop -d -p 3000:3000 bkimminich/juice-shop
ddocker run -d -it --rm -v $(pwd):/wrk/:rw python:3.11-slim /bin/bash -c "pip install --no-cache-dir pyotp && python /wrk/scripts/mfa-gen.py"
docker run --rm --cpus="8" --memory="8g" -v $(pwd):/zap/wrk/:rw -u zap -i ghcr.io/zaproxy/zaproxy:stable zap.sh -addoninstall communityScripts -addoninstall jython -loglevel debug -cmd -autorun /zap/wrk/config.yaml
echo "$(date)" >> time