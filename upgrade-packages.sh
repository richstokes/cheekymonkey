#!/bin/bash
# Helper script for me, you shouldn't need to run this
pip3 install --upgrade arcade
pip3 install --upgrade pymunk
pip3 install pigar || true
pigar
git add requirements.txt
git commit -m 'Updating packages'
