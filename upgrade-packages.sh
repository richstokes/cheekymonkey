#!/bin/bash
# Helper script for me, you shouldn't need to run this
pip install --upgrade arcade
pip install --upgrade pymunk
pip install pigar || true
pigar
git add requirements.txt
git commit -m 'Updating packages'
