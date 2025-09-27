#!/bin/bash
# Helper script for me, you shouldn't need to run this
pipenv update
pipenv graph
git add Pipfile.lock
git commit -m 'Updating packages'
