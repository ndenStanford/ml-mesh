#!/bin/sh

cd "/${HOME}" || exit

pytest tests/core -ra -vv --capture=no
