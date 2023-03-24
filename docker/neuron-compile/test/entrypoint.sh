#!/bin/bash

pytest -m compilation;
# pytest -m inference; # this can be enabled once we have inferentia runners on github actions and the docker make command supports specifying devices at runtime
